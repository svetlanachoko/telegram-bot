import random
import telebot
from flask import Flask, request
import os
from waitress import serve

# --- Настройки ---
TOKEN = os.getenv("TOKEN")  # Получаем токен из переменных окружения
bot = telebot.TeleBot(TOKEN)

# --- Пророчества Мадам Люмины ---
prophecies = [
    "Сегодня тебе предложат странный выбор. Сделай вид, что знаешь, что делаешь.",
    "Если кто-то задаст тебе неожиданный вопрос – просто скажи 'Да, но не так, как ты думаешь'.",
    "В ближайшее время ты найдёшь что-то утерянное. Возможно, свою мотивацию. Возможно, просто носок.",
    "Одна из сегодняшних фраз окажется пророческой. Ты поймёшь, какая, когда уже будет поздно.",
    "Некоторые двери лучше не открывать. Особенно холодильник после 23:00.",
]

# --- Архетип дня ---
archetypes = {
    "Герой": "Сегодня твой день, чтобы действовать. Или хотя бы сделать зарядку.",
    "Трикстер": "Ты сегодня непредсказуем. Даже для себя.",
    "Тень": "Будь осторожен: сегодня тебя могут преследовать твои собственные мысли.",
    "Мудрец": "Ты сегодня полон знаний. Или хотя бы умеешь умно молчать.",
    "Шут": "Тебе всё кажется абсурдом? Отлично, ты понял суть жизни.",
}

# --- Обработчики команд ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот Мадам Люмины. Напиши /пророчество или /архетип.")

@bot.message_handler(commands=['пророчество'])
def send_prophecy(message):
    prophecy = random.choice(prophecies)
    bot.reply_to(message, f"🔮 {prophecy}")

@bot.message_handler(commands=['архетип'])
def send_archetype(message):
    archetype, description = random.choice(list(archetypes.items()))
    bot.reply_to(message, f"🎭 Сегодня твой архетип: *{archetype}*\n_{description}_", parse_mode='Markdown')

# --- Flask вебхук ---
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://telegram-bot-ljm6.onrender.com/{TOKEN}')  # ← Твой реальный домен!
    return "Webhook set", 200

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
