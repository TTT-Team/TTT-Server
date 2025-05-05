# TTT-Bank Server

Серверная часть веб-приложения TTT-Bank, разработанная с использованием Django и Django REST Framework.

## Описание

TTT-Bank Server - это бэкенд-приложение, предоставляющее RESTful API для банковского веб-приложения. Проект построен на современном стеке технологий и включает в себя:

- Django 5.2
- Django REST Framework
- Pydantic для валидации данных
- Swagger/OpenAPI документацию через drf-spectacular

## Требования

- Python 3.8+
- pip (менеджер пакетов Python)
- Docker (для запуска через контейнер)

## Установка и запуск

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone [URL репозитория]
cd TTT-Server
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
# Для Windows:
.venv\Scripts\activate
# Для Linux/Mac:
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройка переменных окружения:
```bash
# Скопируйте файл с примером конфигурации
cp .env_example .env
# Отредактируйте .env файл, заполнив необходимые переменные окружения
```

5. Примените миграции:
```bash
python bank_server/manage.py migrate
```

6. Запустите сервер разработки:
```bash
python bank_server/manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

### Запуск через Docker

1. Соберите Docker образ:
```bash
docker build -t ttt-bank-server .
```

2. Запустите контейнер с переменными окружения:
```bash
docker run -d \
  --name ttt-bank-server \
  -p 8000:8000 \
  --env-file .env \
  ttt-bank-server
```

Или используйте docker-compose:
```bash
docker-compose up -d
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## API Документация

После запуска сервера, документация API доступна по адресу:
- Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/
- ReDoc: http://127.0.0.1:8000/api/schema/redoc/
