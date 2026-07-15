# OpenTube API

YouTube metadata + MP3/MP4 download API. Built with [opentube](https://github.com/jnsougata/opentube) + [yt-dlp](https://github.com/yt-dlp/yt-dlp).

**Base URL:** `https://your-service.onrender.com`

---

## Endpoints

### `GET /health`

Server health check.

```bash
curl https://your-service.onrender.com/health
```

```json
{ "status": "ok", "uptime": 3600, "version": "1.0.0" }
```

---

### `GET /info`

Fetch video metadata and available formats.

```
GET /info?url=<youtube_url>
```

| Param | Required | Description |
|-------|----------|-------------|
| `url` | Yes | YouTube URL (`youtu.be/...`, `watch?v=...`, `shorts/...`) |

**Examples:**

```bash
# Short URL
curl "https://your-service.onrender.com/info?url=https://youtu.be/dQw4w9WgXcQ"

# Full URL
curl "https://your-service.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Shorts
curl "https://your-service.onrender.com/info?url=https://youtube.com/shorts/abc123"
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "dQw4w9WgXcQ",
    "title": "Rick Astley - Never Gonna Give You Up",
    "duration": 212,
    "duration_string": "3:32",
    "views": "1500000000",
    "likes": "20000000",
    "comments": "500000",
    "upload_date": "20091025",
    "channel": {
      "name": "Rick Astley",
      "id": "UCuAXFkgsw1L7xaCfnd5JJOw",
      "subscribers": "15M subscribers"
    },
    "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
    "description": "The official video for...",
    "tags": ["music", "pop", "80s"],
    "age_limit": 0,
    "categories": ["Music"],
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "formats": [
      { "format_id": "137", "ext": "mp4", "resolution": "1080p", "filesize": 52000000, "vcodec": "avc1.640028", "acodec": null, "fps": 30 },
      { "format_id": "22",  "ext": "mp4", "resolution": "720p",  "filesize": 8500000,  "vcodec": "avc1.64001F", "acodec": "mp4a.40.2", "fps": 30 },
      { "format_id": "18",  "ext": "mp4", "resolution": "360p",  "filesize": 2500000,  "vcodec": "avc1.42001E", "acodec": "mp4a.40.2", "fps": 30 },
      { "format_id": "140", "ext": "m4a", "resolution": "audio", "filesize": 1500000,  "vcodec": null,          "acodec": "mp4a.40.2", "fps": null }
    ]
  }
}
```

---

### `GET /download`

Download video (MP4) or extract audio (MP3). File streams directly — no server storage.

```
GET /download?url=<youtube_url>&format=<mp4|mp3>
```

| Param  | Required | Default | Description |
|--------|----------|---------|-------------|
| `url`  | Yes      | —       | YouTube video URL |
| `format` | No    | `mp4`   | Output format: `mp4` (video) or `mp3` (audio) |

**Examples:**

```bash
# Download MP4
curl -o video.mp4 "https://your-service.onrender.com/download?url=https://youtu.be/dQw4w9WgXcQ&format=mp4"

# Download MP3
curl -o audio.mp3 "https://your-service.onrender.com/download?url=https://youtu.be/dQw4w9WgXcQ&format=mp3"
```

**Browser:** Paste the URL directly — it will prompt a file download.

---

### `GET /docs`

Interactive Swagger UI to test all endpoints.

```
https://your-service.onrender.com/docs
```

---

## Error Responses

```json
{
  "detail": "Failed to fetch info: [error message]"
}
```

| HTTP Status | Meaning |
|-------------|---------|
| `400` | Invalid URL or failed to fetch info |
| `500` | Download failed (e.g. video unavailable) |

---

## Fix Bot Detection (429 Errors)

If you get `"Sign in to confirm you're not a bot"`:

1. Install a cookies exporter ([Chrome](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/))
2. Go to youtube.com (logged in) → export cookies (Netscape format)
3. Add the content as the `COOKIES` env var in your Render dashboard → redeploy

---

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Install ffmpeg (required)
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# Start server
uvicorn app:app --reload --port 8000
```

Server runs at `http://localhost:8000`. Swagger UI at `http://localhost:8000/docs`.

---

## Deploy on Render

1. Push repo to GitHub
2. Go to [dashboard.render.com](https://dashboard.render.com) → **New +** → **Web Service**
3. Connect your repository
4. Render auto-detects `render.yaml` → click **Apply**
5. Set `COOKIES` env var if needed

---

## Project Structure

```
├── app.py              # FastAPI server (endpoints: /, /health, /info, /download)
├── Dockerfile          # Python 3.11 + ffmpeg + yt-dlp
├── render.yaml         # Render Docker Web Service config
├── requirements.txt    # Python dependencies
└── opentube/           # YouTube metadata library (local copy)
```
