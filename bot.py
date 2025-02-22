import os
import random
import telebot
from flask import Flask, request
from waitress import serve

# Проверяем, что TOKEN задан
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is not set!")

bot = telebot.TeleBot(TOKEN)

prophecies = [
    "Сегодня тебе предложат странный выбор. Сделай вид, что знаешь, что делаешь.",
    "Если кто-то задаст тебе неожиданный вопрос – просто скажи 'Да, но не так, как ты думаешь'.",
    "В ближайшее время ты найдёшь что-то утерянное. Возможно, свою мотивацию. Возможно, просто носок."
]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Мадам Люмина. Хочешь узнать свою судьбу? Введи /predict.")

@bot.message_handler(commands=['predict'])
def send_prophecy(message):
    prophecy = random.choice(prophecies)
    bot.reply_to(message, prophecy)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Bot is running!", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://telegram-bot-ljm6.onrender.com/{TOKEN}")
    return "Webhook set", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
