# 🎵 Tarona Bot - O'zingizning Serverida O'rnatish Qo'llanmasi

## 📋 Talablar

- Linux server (Ubuntu 20.04+)
- Python 3.9+
- FFmpeg
- Internet ulanishi
- Telegram Bot Token (@BotFather-dan)

## 🚀 Qo'shma O'rnatish (1-daqiqa)

### 1. Server-da repository klonlash
```bash
cd /home/username
git clone https://github.com/behruzlebedov14-dotcom/tarona-bot.git
cd tarona-bot
```

### 2. Setup script-ni ishga tushirish
```bash
chmod +x server_setup.sh
./server_setup.sh
```

### 3. .env faylini sozlash
```bash
nano .env
```

Quyidagini kiriting:
```
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

**BOT_TOKEN olish:**
1. Telegram-da @BotFather-ni toping
2. `/newbot` buyrugi bilan yangi bot yarating
3. Berilgan tokenni .env-ga qo'ying

### 4. Bot-ni ishga tushirish

**Optsiya 1: Oddiy ishga tushirish**
```bash
source venv/bin/activate
python3 music_bot.py
```

**Optsiya 2: Fonda 24/7 ishga tushirish (nohup)**
```bash
nohup python3 music_bot.py > bot.log 2>&1 &
```

**Optsiya 3: Systemd service sifatida (best)**
```bash
chmod +x systemd_service.sh
./systemd_service.sh
sudo systemctl start tarona-bot
```

## 🔍 Tekshirish

### 1. Bot ishlayotganligini tekshirish
```bash
pgrep -f music_bot.py
```

### 2. Logs ko'rish
```bash
tail -f bot.log
```

### 3. Telegram-da test qilish
- Bot-ni Telegram-da qidiring
- `/start` buyrugi bilan boshlang
- Test musiqasini yuklang

## 🐳 Docker bilan O'rnatish

`docker_setup.md` faylini o'qing

## 🆘 Muammolar va Yechimlar

### "Bot respond bermayapti"
- BOT_TOKEN to'g'ri kiritilganligini tekshiring
- Internet ulanishini tekshiring
- Bot processni qayta ishga tushiring: `pkill -f music_bot.py`

### "FFmpeg topilmadi"
```bash
sudo apt-get install ffmpeg
```

### "Python paketlari o'rnatilmadi"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "Xotira kam"
- Downloads papkasidagi eski fayllarni o'chiring
- Katta musiqalarni download qilmang

## 📊 Performance Monitoring

### CPU va Xotira istifodasi
```bash
top -p $(pgrep -f music_bot.py)
```

### Network trafikni ko'rish
```bash
iftop
```

## 🔐 Xavfsizlik

1. Firewall-da portni ochish (agar kerak bo'lsa)
```bash
sudo ufw allow 8000/tcp
```

2. SSH orqali serverga kirish
```bash
ssh username@server_ip
```

3. `.env` faylni avtomatik backup qilish
```bash
cp .env .env.backup
```

## 📈 Scalability

### Bir necha botni ishga tushirish
```bash
nohup python3 music_bot.py > bot1.log 2>&1 &
nohup python3 music_bot.py > bot2.log 2>&1 &
```

### Load Balancer (nginx)
```nginx
upstream bot_backend {
    server localhost:8000;
    server localhost:8001;
}

server {
    listen 80;
    location / {
        proxy_pass http://bot_backend;
    }
}
```

## 🎯 Global Deploy Checklist

- [ ] Python 3.9+ o'rnatildi
- [ ] FFmpeg o'rnatildi
- [ ] Repository klonlandi
- [ ] Virtual environment yaratildi
- [ ] Paketlar o'rnatildi
- [ ] BOT_TOKEN .env-ga qo'shildi
- [ ] Bot test qilindi (Telegram-da)
- [ ] Logs tekshirildi
- [ ] Firewall sozlandi (agar kerak bo'lsa)
- [ ] Backup sozlandi
- [ ] Monitoring sozlandi

## 📞 Qo'llab-quvvatlash

Muammolar bo'lsa:
- GitHub Issues: https://github.com/behruzlebedov14-dotcom/tarona-bot/issues
- Email: yuboring

---

**Muvaffaqiyat!** 🎉 Bot global bo'lib ishlayti! 🚀
