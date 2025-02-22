import random
import telebot
from flask import Flask, request
import os
from waitress import serve

TOKEN = os.getenv("TOKEN")
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

# --- Загадки для алхимии ---
alchemy_riddles = {
    "Я белый, но не снег. Меня добавляют в тесто, но не всегда сладкое. Что я?": "Мука",
    "Меня можно жевать, но я не жвачка. Меня можно пить, но я не вода. Что я?": "Шоколад",
    "Если смешать солнце и море, что получится?": "Соль",
    "Я твёрдый, но во рту исчезаю. Кто я?": "Сахар",
}

# --- Обработчики команд ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот Мадам Люмины. Напиши /пророчество, /архетип или /загадка.")

@bot.message_handler(commands=['пророчество'])
def send_prophecy(message):
    prophecy = random.choice(prophecies)
    bot.reply_to(message, f"🔮 {prophecy}")

@bot.message_handler(commands=['архетип'])
def send_archetype(message):
    archetype, description = random.choice(list(archetypes.items()))
    bot.reply_to(message, f"🎭 Сегодня твой архетип: *{archetype}*\n_{description}_", parse_mode='Markdown')

@bot.message_handler(commands=['загадка'])
def send_riddle(message):
    riddle, answer = random.choice(list(alchemy_riddles.items()))
    bot.reply_to(message, f"🧪 Загадка: {riddle}\nОтвет напиши в чат!")

@bot.message_handler(func=lambda message: message.text in alchemy_riddles.values())
def check_answer(message):
    bot.reply_to(message, "🎉 Верно! Ты получил ингредиент для алхимии!")

# --- Flask вебхук ---
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://yourappname.onrender.com/{TOKEN}')  # Убедись, что URL правильный
    return "Webhook set", 200

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

   
