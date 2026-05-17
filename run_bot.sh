#!/bin/bash

# Bot-ni fonda ishga tushirish (24/7 uchun)
# Qo'llanish: ./run_bot.sh yoki nohup ./run_bot.sh &

echo "🎵 Tarona Bot ishga tushmoqda..."

# Virtual environment faollashtrirish
source venv/bin/activate

# Bot-ni ishga tushirish
python3 music_bot.py
