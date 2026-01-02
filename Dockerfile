# Multi-stage Dockerfile для развертывания проекта

# Этап 1: Сборка фронтенда
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Копируем файлы зависимостей
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем исходный код фронтенда
COPY frontend/ .

# Собираем фронтенд для production
RUN npm run build

# Этап 2: Финальный образ с бэкендом и фронтендом
FROM python:3.12-slim

WORKDIR /app

# Копируем requirements и устанавливаем Python зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем бэкенд
COPY backend/ ./backend/

# Копируем собранный фронтенд из предыдущего этапа
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Копируем скрипт запуска сервера
COPY run_server.py .

# Пробрасываем порты
EXPOSE 8000

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Запускаем сервер
CMD ["python", "run_server.py"]

