# 🤖 Llama-3 Chat Bot

Чат-бот на основе модели Llama-3 с сохранением истории диалогов в PostgreSQL. Проект использует Streamlit для веб-интерфейса и Docker для развертывания.

## 🌟 Возможности

- 💬 Диалог с использованием модели Llama-3
- 💾 Сохранение истории диалогов в PostgreSQL
- 🔑 Безопасное хранение API ключей
- 🧹 Возможность очистки истории диалогов

## 🛠 Технологии

- Python 3.9
- Streamlit
- LangChain
- PostgreSQL
- Docker & Docker Compose

## 📋 Требования

- Docker
- Docker Compose

## 🚀 Установка и запуск

1. Клонируйте репозиторий:
git clone https://github.com/e-zhenka/my_bootcamp_bot.git
cd my_bootcamp_bot

2. Создайте файл конфигурации:
cp .env.example .env

3. Если необходимо настройте переменные окружения в файле .env:
# Database settings
POSTGRES_DB=chatbot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# API settings
OPENAI_BASE_URL=https://llama3gpu.neuraldeep.tech/v1
OPENAI_MODEL=llama-3-8b-instruct-8k

4. Запустите приложение:
docker-compose up --build

5. Откройте приложение в браузере:
   http://localhost:7860/ 
