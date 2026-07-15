import os
import re
import json
import subprocess
import tempfile
import shutil
import time
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from opentube import Video

START_TIME = time.time()
COOKIES_ENV = os.environ.get("COOKIES", "")

app = FastAPI(title="OpenTube API", version="1.0.0", docs_url="/docs")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def clean_url(url: str) -> str:
    url = re.sub(r'[?&](si|feature)=[^&]+', '', url)
    m = re.search(r'(?:v=|youtu\.be/|shorts/)([\w-]{11})', url)
    return m.group(1) if m else url.strip()


def ytdl_args(extra: list[str]) -> list[str]:
    args = ["yt-dlp", "--no-warnings", "--no-playlist",
            "--geo-bypass",
            "--extractor-args", "youtube:player_client=android,web"]
    if COOKIES_ENV:
        cf = os.path.join(tempfile.gettempdir(), "yt_cookies.txt")
        if not os.path.exists(cf):
            with open(cf, "w") as f:
                f.write(COOKIES_ENV)
        args += ["--cookies", cf]
    return args + extra


def run_ytdlp_json(url: str) -> dict:
    proc = subprocess.run(
        ytdl_args(["-j", "--no-download", url]),
        capture_output=True, text=True, timeout=30,
    )
    if proc.returncode != 0:
        raise Exception(proc.stderr.strip())
    return json.loads(proc.stdout)


FORMAT_ORDER = {"2160p": 0, "1440p": 1, "1080p": 2, "720p": 3, "480p": 4, "360p": 5, "240p": 6, "144p": 7, "audio": 8}


def sort_key(f):
    res = f.get("resolution", "audio")
    return FORMAT_ORDER.get(res, 99)


@app.get("/")
async def root():
    return {
        "name": "OpenTube API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "GET  → Server health status",
            "/info":   "GET ?url=  → Video metadata + formats",
            "/download": "GET ?url=&format=mp4|mp3  → Download file",
            "/docs":   "GET  → Swagger UI",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok", "uptime": int(time.time() - START_TIME), "version": "1.0.0"}


@app.get("/info")
async def video_info(url: str = Query(..., description="YouTube video URL")):
    video_id = clean_url(url)
    if not re.match(r'^[\w-]{11}$', video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        # yt-dlp for rich metadata + formats
        raw = run_ytdlp_json(f"https://www.youtube.com/watch?v={video_id}")

        # opentube for structured metadata
        ot = Video(video_id)
        ot_meta = ot.metadata

        formats = []
        for f in raw.get("formats", []):
            formats.append({
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "resolution": f.get("resolution") or (f"{f['height']}p" if f.get("height") else "audio"),
                "filesize": f.get("filesize") or f.get("filesize_approx"),
                "vcodec": f.get("vcodec"),
                "acodec": f.get("acodec"),
                "fps": f.get("fps"),
            })
        formats.sort(key=sort_key)

        return {
            "success": True,
            "data": {
                "id": video_id,
                "title": raw.get("title"),
                "duration": raw.get("duration"),
                "duration_string": f"{raw.get('duration', 0) // 60}:{raw.get('duration', 0) % 60:02d}",
                "views": ot_meta.get("views"),
                "likes": ot_meta.get("likes"),
                "comments": ot_meta.get("comments"),
                "upload_date": raw.get("upload_date"),
                "channel": {
                    "name": ot_meta.get("owner", {}).get("title"),
                    "id": ot_meta.get("owner", {}).get("id"),
                    "subscribers": ot_meta.get("owner", {}).get("subscribers"),
                },
                "thumbnail": raw.get("thumbnail") or ot_meta.get("thumbnail"),
                "description": (raw.get("description") or "")[:500],
                "tags": raw.get("tags", [])[:10],
                "age_limit": raw.get("age_limit"),
                "categories": raw.get("categories", []),
                "formats": formats,
                "url": f"https://www.youtube.com/watch?v={video_id}",
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch info: {str(e)}")


@app.get("/download")
async def download(
    url: str = Query(..., description="YouTube video URL"),
    format: str = Query("mp4", regex="^(mp4|mp3)$", description="Output format"),
):
    video_id = clean_url(url)
    if not re.match(r'^[\w-]{11}$', video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    outdir = tempfile.mkdtemp(prefix="ot_")
    try:
        marker = os.urandom(4).hex()
        output_tpl = os.path.join(outdir, f"{marker}.%(ext)s")

        if format == "mp3":
            base = ["-f", "bestaudio", "-x", "--audio-format", "mp3"]
        else:
            base = ["-f", "best", "--remux-video", "mp4"]
        base += ["-o", output_tpl, f"https://www.youtube.com/watch?v={video_id}"]

        proc = subprocess.run(ytdl_args(base), capture_output=True, text=True, timeout=300)
        if proc.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Download failed: {proc.stderr.strip()}")

        files = list(Path(outdir).iterdir())
        if not files:
            raise HTTPException(status_code=500, detail="No output file produced")

        filepath = str(files[0])
        filesize = os.path.getsize(filepath)
        if filesize == 0:
            raise HTTPException(status_code=500, detail="Output file is empty")

        safe_title = "video"
        try:
            v = Video(video_id)
            safe_title = re.sub(r'[\\/*?:"<>|]', '', v.metadata.get("title", "video")).strip() or "video"
        except Exception:
            pass

        ext = format
        filename = f"{safe_title}.{ext}"
        media_type = "video/mp4" if format == "mp4" else "audio/mpeg"

        def generate():
            try:
                with open(filepath, "rb") as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        yield chunk
            finally:
                shutil.rmtree(outdir, ignore_errors=True)

        return StreamingResponse(
            generate(),
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(filesize),
            },
        )

    except HTTPException:
        shutil.rmtree(outdir, ignore_errors=True)
        raise
    except Exception as e:
        shutil.rmtree(outdir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
