# Используем Python образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . /app

# Обновляем пакеты и устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip

# Устанавливаем ngrok
RUN wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz && \
    tar -xvf ngrok-v3-stable-linux-amd64.tgz && \
    mv ngrok /usr/local/bin/ngrok && \
    rm ngrok-v3-stable-linux-amd64.tgz

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения
ENV NGROK_TOKEN=2Pe7GQGQSAaFdYL9jwRPMmjP8t1_6oTLRJ6AAhTKfDf9L7mb4
ENV TELEGRAM_TOKEN=5790682102:AAEzK7u1c8O5hooq9Ae0e8ffH5Wt0Yoi-eA
ENV GOOGLE_SCRIPT_URL=https://script.google.com/macros/s/AKfycbyf0z2ACcf4i98WeFfMcKt7to0gLPyfwLVEuyJHgZySPFeeLNg1ZGXLPSZeEyzZFKQD/exec

# Запускаем бот и ngrok
CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
