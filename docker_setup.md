# 🐳 Docker bilan Tarona Bot

## Docker o'rnatish

### Linux
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### macOS
```bash
brew install docker
```

### Windows
Docker Desktop-ni https://www.docker.com/products/docker-desktop dan yuklab oling

## Bot-ni Docker bilan ishga tushirish

1. **Dockerfile yaratish** (agar bo'lmasa):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "music_bot.py"]
```

2. **Docker image yaratish**:
```bash
docker build -t tarona-bot .
```

3. **Docker konteyner ishga tushirish**:
```bash
docker run -d \
  --name tarona-bot \
  -e BOT_TOKEN=YOUR_BOT_TOKEN \
  -v $(pwd)/downloads:/app/downloads \
  tarona-bot
```

4. **Logs ko'rish**:
```bash
docker logs -f tarona-bot
```

5. **Konteyner to'xtarish**:
```bash
docker stop tarona-bot
```
