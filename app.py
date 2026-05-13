import os
import requests
from flask import Flask, request
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
DIFY_API_URL = os.environ.get('DIFY_API_URL')
DIFY_API_KEY = os.environ.get('DIFY_API_KEY')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.from_user.id)
    text = message.text

    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "inputs": {},
        "query": text,
        "response_mode": "blocking",
        "user": user_id
    }

    try:
        response = requests.post(f"{DIFY_API_URL}/chat-messages", json=data, headers=headers)
        res_data = response.json()
        reply = res_data.get('answer', 'Ошибка: Не удалось получить текст ответа.')
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка при запросе к Dify: {str(e)}")

@app.route('/')
def index():
    return "Бот активен", 200
