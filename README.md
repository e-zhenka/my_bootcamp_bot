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

3. Создайте файл конфигурации:
cp .env.example .env

4. Если необходимо настройте переменные окружения в файле .env:

5. Запустите приложение:
docker-compose up --build

6. Откройте приложение в браузере:
[  [ http://localhost:7860/ ](http://localhost:8501/) ](http://localhost:8501/)
