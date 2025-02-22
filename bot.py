import telebot
import os
from flask import Flask, request

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!", 200

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-прорицатель. Хочешь узнать своё предсказание? Напиши мне!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "🔮 Судьба загадочна... но шоколад всегда помогает!")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
