import os
import time
import subprocess
import requests
import telebot
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

API_TOKEN = os.getenv('TELEGRAM_TOKEN') 
bot = telebot.TeleBot(API_TOKEN)

GOOGLE_SCRIPT_URL = os.getenv('GOOGLE_SCRIPT_URL')
NGROK_TOKEN = os.getenv('NGROK_TOKEN')


def start_ngrok():
    subprocess.run(["ngrok", "authtoken", NGROK_TOKEN])
    subprocess.Popen(["ngrok", "http", "8000"])
    time.sleep(2)  

    # Получаем публичный URL из ngrok API
    response = requests.get("http://localhost:4040/api/tunnels")
    tunnels = response.json().get('tunnels')
    if tunnels:
        public_url = tunnels[0]['public_url']
        print(f"NGROK URL: {public_url}")
        return public_url
    else:
        print("No tunnels found. Please check ngrok status.")
        return None



# Функция для отправки ngrok URL в Google Apps Script
def send_ngrok_url_to_google_script(ngrok_url):
    full_url = f"{GOOGLE_SCRIPT_URL}?get_data=ngrok"
    response = requests.post(full_url, data=ngrok_url)
    print(f"Google Script Response: {response.text}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Привет! Как тебя зовут?")
    bot.register_next_step_handler(message, process_name)


def process_name(message):
    user_name = message.text  # Сохраняем введенное имя
    bot.reply_to(message, f"Рад знакомству, {user_name}!")
    ruble_rate = get_ruble_exchange_rate()
    if ruble_rate is not None:
        bot.reply_to(message, f"Курс доллара сегодня = {ruble_rate}р.")
    else:
        bot.reply_to(
            message, "Извините, на данный момент я не смог узнать обменный курс.")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/webhook")
async def webhook(request: Request):
    json_data = await request.json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return JSONResponse(content={"status": "ok"})

@bot.message_handler(func=lambda message: True)  
def echo_message(message):
    bot.reply_to(message, message.text)  


def get_ruble_exchange_rate():
    try:
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        ruble_rate = data['rates']['RUB']
        return ruble_rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None


ngrok_url = start_ngrok()
if ngrok_url:
    send_ngrok_url_to_google_script(ngrok_url)

bot.remove_webhook()
bot.set_webhook(url=f"{ngrok_url}/webhook")
