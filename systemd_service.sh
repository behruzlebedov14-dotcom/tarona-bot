#!/bin/bash

# Tarona Bot-ni systemd service sifatida o'rnatish
# Bu bot serverda restart bo'lganda avtomatik ishga tushradi

echo "🔧 Tarona Bot systemd service o'rnatilmoqda..."

# Bot folderining absolute path-i
BOT_PATH=$(pwd)
USER=$(whoami)

# Service fayli yaratish
sudo tee /etc/systemd/system/tarona-bot.service > /dev/null <<EOF
[Unit]
Description=Tarona Global Music Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_PATH
ExecStart=$BOT_PATH/venv/bin/python3 $BOT_PATH/music_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service fayli yaratildi!"
echo ""
echo "🚀 Service-ni ishga tushirish uchun:"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable tarona-bot"
echo "   sudo systemctl start tarona-bot"
echo ""
echo "📋 Status tekshirish uchun:"
echo "   sudo systemctl status tarona-bot"
echo ""
echo "🛑 Service-ni to'xtarish uchun:"
echo "   sudo systemctl stop tarona-bot"
echo ""
