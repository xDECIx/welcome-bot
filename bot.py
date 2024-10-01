import os
import time
import subprocess
import requests

# Переменные среды
# NGROK_TOKEN = os.getenv("NGROK_TOKEN")
# GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")  # URL вашего Google Apps Script
NGROK_TOKEN = '2Pe7GQGQSAaFdYL9jwRPMmjP8t1_6oTLRJ6AAhTKfDf9L7mb4'
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyf0z2ACcf4i98WeFfMcKt7to0gLPyfwLVEuyJHgZySPFeeLNg1ZGXLPSZeEyzZFKQD/exec'

# Функция для запуска ngrok и получения динамического URL
def start_ngrok():
    # Запускаем ngrok
    subprocess.Popen(["ngrok", "http", "8000"])
    time.sleep(2)  # Ждем пока ngrok поднимется

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
    data = ngrok_url
    response = requests.post(full_url, data=data)
    print(f"Google Script Response: {response.text}")

if __name__ == "__main__":
    # Запускаем ngrok и получаем его URL
    ngrok_url = start_ngrok()
    print("@@@@@@@@s",ngrok_url)
    if ngrok_url:
        # Отправляем URL ngrok в Google Apps Script
        send_ngrok_url_to_google_script(ngrok_url)
    else:
        print("Failed to retrieve ngrok URL")

