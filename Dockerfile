# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY app/ ./app/
COPY .env .

# Открываем порт
EXPOSE 8501

# Запускаем приложение
CMD ["python", "-m", "streamlit", "run", "app/main.py", "--server.address=0.0.0.0"]