import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-прорицатель. Хочешь узнать своё предсказание? Напиши мне!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "🎩 Судьба загадочна... но шоколад всегда помогает!")

bot.infinity_polling()

