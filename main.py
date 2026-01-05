import os
import telebot
from yt_dlp import YoutubeDL

# حط التوكن بتاعك هنا مكان الكلمة اللي بين القوسين
API_TOKEN = '8249071787:AAF2pvdmzYZmbujiGtJXDU4ncjjdZbUxWms'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! ابعتلي لينك الفيديو من (يوتيوب، فيسبوك، تيك توك، انستجرام) وهنزلهولك.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.reply_to(message, "جاري التحميل... انتظر ثواني ⏳")
    
    try:
        # إعدادات التحميل
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'max_filesize': 45000000, # تحديد الحجم عشان تيليجرام آخره 50 ميجا للبوتات المجانية
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إرسال الفيديو للمستخدم
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        # مسح الفيديو من السيرفر بعد الإرسال لتوفير المساحة
        os.remove('video.mp4')
        
    except Exception as e:
        bot.reply_to(message, f"حصلت مشكلة: {str(e)}")

bot.polling()
