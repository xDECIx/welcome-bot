import os
import json
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types

# API_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_TOKEN = '5790682102:AAEzK7u1c8O5hooq9Ae0e8ffH5Wt0Yoi-eA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# FastAPI маршрут для приема webhook событий от Telegram
@app.post("/webhook")
async def process_webhook(update: dict):
    update = types.Update(**update)
    await dp.process_update(update)
    return {"status": "ok"}

# Пример хендлера для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I am your bot!")
