FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей (если нужны)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY docker/python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Команда запуска (переопределяется в docker-compose)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000