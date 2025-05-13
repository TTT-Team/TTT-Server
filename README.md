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

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Создайте файл `.env` на основе `.env_example`:
```bash
cp bank_server/.env_example bank_server/.env
```

3. Отредактируйте файл `bank_server/.env`, заполнив необходимые переменные окружения:
- `SECRET_KEY` - секретный ключ Django
- `NAME` - имя базы данных
- `USER` - пользователь базы данных
- `PASSWORD` - пароль базы данных
- `HOST` - хост базы данных (по умолчанию localhost)
- `PORT` - порт базы данных (по умолчанию 5432)
- `ACCESS_TOKEN_LIFETIME` - время жизни access токена
- `REFRESH_TOKEN_LIFETIME` - время жизни refresh токена
- `ALGORITHM` - алгоритм шифрования JWT
- `AUTH_HEADER_TYPE` - тип заголовка авторизации

4. Соберите Docker образ:
```bash
docker-compose build
```

5. Запустите проект с помощью Docker Compose:
```bash
docker-compose up -d
```

При первом запуске автоматически будут:
- Применены миграции
- Создана начальная валюта (RUB)
- Собран статический контент
- Запущен веб-сервер

Для просмотра логов:
```bash
docker-compose logs -f
```

Для остановки:
```bash
docker-compose down
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

### Структура Docker-конфигурации

Проект использует следующие Docker-файлы:
- `Dockerfile` - основной файл для сборки образа
- `docker-compose.yml` - конфигурация для запуска контейнеров

## API Документация

После запуска сервера, документация API доступна по адресу:
- Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/
- ReDoc: http://127.0.0.1:8000/api/schema/redoc/
