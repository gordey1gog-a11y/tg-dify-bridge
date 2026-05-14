import os
import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Настройка логирования для Render
logging.basicConfig(level=logging.INFO)

# Инициализация переменных из настроек Render
TOKEN = os.getenv("BOT_TOKEN")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv("DIFY_API_URL", "dify.ai")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("ИИ-агент 'Берлога Здоровья' запущен в облаке и готов к работе! Отправьте мне ваш вопрос.")

@dp.message()
async def handle_message(message: types.Message):
    if not message.text:
        return
        
    # Отправляем индикатор "Бот печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": {},
        "query": message.text,
        "response_mode": "blocking",
        "user": f"tg_{message.from_user.id}"
    }
    
    try:
        response = requests.post(f"{DIFY_API_URL}/chat-messages", json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            result = response.json()
            await message.answer(result.get("answer", "Ошибка: Пустой ответ от ИИ."))
        else:
            await message.answer(f"Ошибка связи с мозгом ИИ (Код: {response.status_code})")
    except Exception as e:
        await message.answer("Не удалось получить ответ. Проверьте подключение Dify.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
