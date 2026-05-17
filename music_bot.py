#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import yt_dlp
import os
import subprocess
from dotenv import load_dotenv
import logging
from datetime import datetime

# .env fayldan token yuklash
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylda topilmadi!")

bot = telebot.TeleBot(BOT_TOKEN)

# Logging sozlamasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

print("🎵 Tarona Bot ishga tushdi!")
logger.info("Bot boshlandi")

# ============== BOSH MENYU ==============
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    logger.info(f"Yangi foydalanuvchi: {user_name} ({chat_id})")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🎵 YouTube'dan yuklash")
    btn2 = types.KeyboardButton("🔍 Qidirish")
    btn3 = types.KeyboardButton("📋 Playlist")
    btn4 = types.KeyboardButton("ℹ️ Ma'lumot")
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        f"🎶 Assalomu aleykum, {user_name}!\n\n"
        "Tarona Global Music Bot-ga xush kelibsiz!\n\n"
        "Quyidagi xizmatlardan foydalaning:\n"
        "🎵 YouTube-dan musiqalarni yuklash\n"
        "🔍 Musiqalarni qidirish\n"
        "📋 Playlist yaratish\n\n"
        "Menyu-dan birini tanlang:"
    )
    
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

# ============== YOUTUBE'DAN YUKLASH ==============
@bot.message_handler(func=lambda message: "YouTube'dan" in message.text or "youtube" in message.text.lower())
def youtube_download(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔗 YouTube linkini yuboring:\n\nMisol: https://www.youtube.com/watch?v=...")
    bot.register_next_step_handler(message, process_youtube_link)

def process_youtube_link(message):
    chat_id = message.chat.id
    url = message.text.strip()
    
    if not url.startswith('http'):
        bot.send_message(chat_id, "❌ To'g'ri link kiriting!")
        return
    
    try:
        loading_msg = bot.send_message(chat_id, "⏳ Yuklanmoqda... Iltimos kuting!")
        logger.info(f"YouTube yuklash boshlandi: {url}")
        
        # yt-dlp bilan musiqani yuklash
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
            bot.delete_message(chat_id, loading_msg.message_id)
            
            # Musiqani jo'natish
            with open(audio_file, 'rb') as audio:
                bot.send_audio(
                    chat_id,
                    audio,
                    title=info.get('title', 'Noma\'lum'),
                    performer=info.get('uploader', 'Noma\'lum'),
                    caption=f"✅ Muvaffaqiyatli yuklandi!\n🎵 {info.get('title', 'Noma\'lum')}\n👤 {info.get('uploader', 'Noma\'lum')}"
                )
            
            # Faylni o'chirish (server joy tejash uchun)
            os.remove(audio_file)
            logger.info(f"Musiqа muvaffaqiyatli yuklandi: {info.get('title')}")
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ Xato: {str(e)[:100]}")
        logger.error(f"YouTube yuklashda xato: {str(e)}")

# ============== QIDIRISH ==============
@bot.message_handler(func=lambda message: "🔍" in message.text or "qidirish" in message.text.lower())
def search_music(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔍 Qidirish so'zini yuboring:\n\nMisol: Adele - Hello")
    bot.register_next_step_handler(message, process_search)

def process_search(message):
    chat_id = message.chat.id
    query = message.text.strip()
    
    try:
        loading_msg = bot.send_message(chat_id, f"🔍 '{query}' qidirilmoqda...")
        logger.info(f"Qidirish: {query}")
        
        # YouTube-da qidirish
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'skip_download': True,
        }
        
        search_url = f"ytsearch5:{query}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(search_url, download=False)
            
            if not results['entries']:
                bot.edit_message_text(
                    "❌ Hech narsa topilmadi!",
                    chat_id,
                    loading_msg.message_id
                )
                return
            
            response_text = "🎵 **Qidirish natijalari:**\n\n"
            markup = types.InlineKeyboardMarkup()
            
            for idx, video in enumerate(results['entries'][:5], 1):
                title = video['title'][:50]
                url = video['url']
                response_text += f"{idx}. {title}\n"
                markup.add(types.InlineKeyboardButton(
                    f"{idx}. {title[:30]}...",
                    callback_data=f"download_{url}"
                ))
            
            bot.edit_message_text(
                response_text + "\n👇 Birorini tanlang:",
                chat_id,
                loading_msg.message_id,
                reply_markup=markup
            )
            logger.info(f"5 ta natija topildi: {query}")
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ Qidirish xatosi: {str(e)[:100]}")
        logger.error(f"Qidirish xatosi: {str(e)}")

# ============== CALLBACK HANDLER (Qidiruv natijalari uchun) ==============
@bot.callback_query_handler(func=lambda call: call.data.startswith('download_'))
def download_from_search(call):
    chat_id = call.message.chat.id
    url = call.data.replace('download_', '')
    bot.answer_callback_query(call.id, "⏳ Yuklanmoqda...")
    process_youtube_link_from_callback(call.message, url)

def process_youtube_link_from_callback(message, url):
    chat_id = message.chat.id
    
    try:
        loading_msg = bot.send_message(chat_id, "⏳ Musiqа yuklanmoqda... Iltimos kuting!")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
            bot.delete_message(chat_id, loading_msg.message_id)
            
            with open(audio_file, 'rb') as audio:
                bot.send_audio(
                    chat_id,
                    audio,
                    title=info.get('title', 'Noma\'lum'),
                    performer=info.get('uploader', 'Noma\'lum'),
                    caption=f"✅ Muvaffaqiyatli yuklandi!\n🎵 {info.get('title', 'Noma\'lum')}"
                )
            
            os.remove(audio_file)
            logger.info(f"Qidiruv natijasidan yuklandi: {info.get('title')}")
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ Xato: {str(e)[:100]}")
        logger.error(f"Callback download xatosi: {str(e)}")

# ============== PLAYLIST ==============
@bot.message_handler(func=lambda message: "📋" in message.text or "playlist" in message.text.lower())
def playlist(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "📋 **Playlist haqida:**\n\n"
        "Playlist funksiyasi tez orada qo'shiladi!\n\n"
        "Hozircha siz:\n"
        "✅ YouTube-dan musiqalarni yuklashingiz mumkin\n"
        "✅ Musiqalarni qidirshingiz mumkin\n\n"
        "🔄 Yangi versiyani kuting!"
    )

# ============== MA'LUMOT ==============
@bot.message_handler(func=lambda message: "ℹ️" in message.text or "ma'lumot" in message.text.lower())
def info(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "ℹ️ **Tarona Global Music Bot**\n\n"
        "🌍 **Global Xizmat**\n"
        "Butun dunyodagi foydalanuvchilar uchun\n\n"
        "🎵 **Xususiyatlar:**\n"
        "✅ YouTube-dan musiqalarni MP3 formatda yuklash\n"
        "✅ Musiqalarni tezda qidirish\n"
        "✅ Yuqori sifatdagi audio\n"
        "✅ 24/7 ishlash\n\n"
        "👨‍💻 **Dastur muallifi:**\n"
        "Behruz Lebedov\n"
        "GitHub: @behruzlebedov14-dotcom\n\n"
        "📅 **Versiya:** 1.0.0\n"
        "🚀 **Status:** Global Active"
    )

# ============== BOSHQA XABARLAR ==============
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "😊 Afsus, bu buyrugni tushunmadim.\n\n"
        "/start-ni bosing yoki menyu-dan birini tanlang."
    )

# ============== BOT ISHGA TUSHIRISH ==============
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎵 TARONA GLOBAL MUSIC BOT")
    print("="*50)
    print(f"📅 Boshlanish vaqti: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🤖 Bot ishga tushdi va tayyor!")
    print("📡 Serverni o'lchang...")
    print("="*50 + "\n")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n🛑 Bot to'xtatildi.")
        logger.info("Bot to'xtadi")
    except Exception as e:
        print(f"❌ Xato: {e}")
        logger.error(f"Bot xatosi: {e}")
