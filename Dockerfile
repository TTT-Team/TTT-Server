FROM python:3.13-slim

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию (название как у корневой папки проекта)
WORKDIR /TTT-Server

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt gunicorn

# Копируем ВЕСЬ проект
COPY . .

# Создаем пользователя и даем права
RUN useradd -m appuser && \
    mkdir -p /TTT-Server/bank_server/staticfiles && \
    chown -R appuser:appuser /TTT-Server
USER appuser
# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bank_server.wsgi:application"]