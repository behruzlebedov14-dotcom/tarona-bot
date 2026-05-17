#!/bin/bash

# Tarona Bot - Global Server Setup Script
# O'zingizning Linux serverida ishlatish uchun

echo "🎵 Tarona Bot - Server Setup"
echo "================================="

# Python 3.9+ o'rnatilganligini tekshirish
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 o'rnatilmagan!"
    echo "Quyidagini ishga tushing:"
    echo "sudo apt-get update"
    echo "sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✅ Python topildi: $(python3 --version)"

# FFmpeg o'rnatilganligini tekshirish (yt-dlp uchun kerak)
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg o'rnatilmagan. O'rnatilmoqda..."
    sudo apt-get update
    sudo apt-get install -y ffmpeg
fi

echo "✅ FFmpeg topildi: $(ffmpeg -version | head -n1)"

# Virtual environment yaratish
echo "📦 Virtual environment yaratilmoqda..."
python3 -m venv venv
source venv/bin/activate

# Paketlarni o'rnatish
echo "📥 Python paketlari o'rnatilmoqda..."
pip install --upgrade pip
pip install -r requirements.txt

# Downloads papkasini yaratish
mkdir -p downloads
chmod 755 downloads

# .env faylini yaratish
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  .env fayli yaratildi!"
    echo "👉 .env faylida BOT_TOKEN-ni o'zingizning tokenga almashting!"
fi

echo ""
echo "================================="
echo "✅ Setup muvaffaqiyatli!"
echo "================================="
echo ""
echo "🚀 Bot-ni ishga tushrish uchun:"
echo "   1. .env faylini o'ching va BOT_TOKEN qo'ying"
echo "   2. source venv/bin/activate"
echo "   3. python3 music_bot.py"
echo ""
