import os
import re
import subprocess
import tempfile
import shutil
import time
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
from opentube import Video

START_TIME = time.time()
COOKIES_ENV = os.environ.get("COOKIES", "")

app = FastAPI(title="OpenTube API", version="1.0.0")


def clean_url(url: str) -> str:
    url = re.sub(r'[?&](si|feature)=[^&]+', '', url)
    m = re.search(r'(?:v=|youtu\.be/|shorts/)([\w-]{11})', url)
    return m.group(1) if m else url.strip()


def ytdl_args(extra: list[str]) -> list[str]:
    args = ["yt-dlp", "--no-warnings", "--no-playlist",
            "--extractor-args", "youtube:player_client=android,web"]
    if COOKIES_ENV:
        cf = os.path.join(tempfile.gettempdir(), "yt_cookies.txt")
        if not os.path.exists(cf):
            with open(cf, "w") as f:
                f.write(COOKIES_ENV)
        args += ["--cookies", cf]
    return args + extra


@app.get("/")
async def root():
    return {"name": "OpenTube API",
            "version": "1.0.0",
            "endpoints": {
                "/health": "GET",
                "/info": "GET ?url=",
                "/download": "GET ?url=&format=mp4|mp3"
            }}


@app.get("/health")
async def health():
    return {"status": "ok",
            "uptime": int(time.time() - START_TIME),
            "version": "1.0.0"}


@app.get("/info")
async def video_info(url: str = Query(...)):
    video_id = clean_url(url)
    if not re.match(r'^[\w-]{11}$', video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    try:
        v = Video(video_id)
        return v.metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch info: {str(e)}")


@app.get("/download")
async def download(url: str = Query(...), format: str = Query("mp4", regex="^(mp4|mp3)$")):
    video_id = clean_url(url)
    if not re.match(r'^[\w-]{11}$', video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    outdir = tempfile.mkdtemp(prefix="ot_")

    try:
        marker = os.urandom(4).hex()
        output_tpl = os.path.join(outdir, f"{marker}.%(ext)s")

        base = []
        if format == "mp3":
            base += ["-x", "--audio-format", "mp3"]
        else:
            base += ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                     "--merge-output-format", "mp4"]
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

        ext = format if format == "mp4" else "mp3"
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
