# OpenTube API

YouTube metadata + download API powered by [opentube](https://github.com/jnsougata/opentube) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Deploy on Render

1. Push to GitHub
2. On Render → **New Web Service** → connect repo
3. Render auto-detects `render.yaml` — click **Apply**
4. Add `COOKIES` env var if you get bot errors

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /info?url=` | Video metadata (title, views, likes, etc.) |
| `GET /download?url=&format=mp4\|mp3` | Download MP4 or MP3 |

```bash
curl http://localhost:8000/info?url=https://youtu.be/dQw4w9WgXcQ
curl -o video.mp4 "http://localhost:8000/download?url=https://youtu.be/dQw4w9WgXcQ&format=mp4"
```

## Local dev

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
