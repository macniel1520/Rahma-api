<div align="center">

![logo](https://i.ibb.co/hSq8TLD/logo.png)


**Ваш путь к Святым местам — с заботой, верой и технологиями**

[![Python](https://img.shields.io/badge/Python-000?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-000?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-000?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![LangChain](https://img.shields.io/badge/LangChain-000?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)

</div>

---

## 📋 Содержание

- [Обзор](#-обзор)
- [Ключевые возможности](#-ключевые-возможности)
- [Архитектура](#-архитектура)
- [Технологии](#-технологии)
- [Установка и запуск](#-установка-и-запуск)
- [Переменные окружения](#-переменные-окружения)
- [Структура репозитория](#-структура-репозитория)
- [API и документация](#-api-и-документация)
- [Разработка и деплой](#-разработка-и-деплой)

---

## 🎯 Обзор

**Rahma API** — это комплексная платформа для организации паломнических маршрутов к святым местам.  
Система сочетает **современные веб-технологии** с **искусственным интеллектом** для предоставления пользователям полного спектра услуг: от поиска маршрутов до общения с AI-ассистентом "Ассадик".

Платформа предоставляет:

- **Управление маршрутами** — создание и поиск паломнических маршрутов (Хадж, Умра и др.)
- **Инфраструктура** — отели и рестораны для каждого маршрута
- **Религиозные деяния** — синхронизация и управление амалами
- **AI-ассистент** — интеллектуальный помощник на базе LangChain и DeepSeek AI
- **Административная панель** — управление данными через SQLAdmin

---

## ✨ Ключевые возможности

- 🕌 **Управление маршрутами** — создание, поиск и фильтрация паломнических маршрутов по странам и категориям
- 🏨 **Отели и рестораны** — управление инфраструктурой для маршрутов с рейтингами и фильтрацией
- 📿 **Амалы** — синхронизация религиозных деяний с категориями и иконками
- 🤖 **AI-ассистент "Ассадик"** — интеллектуальный помощник на базе LangChain и DeepSeek AI для помощи паломникам
- 🔐 **JWT-аутентификация** — регистрация, верификация email, сброс пароля с refresh-токенами
- 🌍 **Управление странами и локациями** — географические данные для маршрутов
- 📱 **Интеграция JES** — eSIM сервисы для путешественников
- 🗄️ **Админ-панель** — полнофункциональная панель управления на базе SQLAdmin
- 📦 **Файловое хранилище** — интеграция с SeaweedFS/S3 для изображений и медиа
- 📧 **Email-уведомления** — отправка писем через SMTP для верификации и восстановления пароля
- 📊 **Структурированное логирование** — использование structlog для мониторинга и отладки

---

## 🏗️ Архитектура

```text
┌────────────────────────┐
│   Клиентские запросы   │
│   (Frontend/Mobile)    │
└──────────┬─────────────┘
           │ REST API
┌──────────▼──────────────────────────────────┐
│           FastAPI Backend                   │
│  ┌─────────────────────────────────────────┐│
│  │  API Routes (v1)                        ││
│  │  - /auth, /users                        ││
│  │  - /routes, /amals                      ││
│  │  - /messages (AI Chat)                  ││
│  │  - /countries, /jes                     ││
│  └──────────┬──────────────────────────────┘│
│             │                               │
│  ┌──────────▼─────────────────────────────┐ │
│  │  Services Layer                        │ │
│  │  - Auth, Route, Amal Services          │ │
│  │  - AI Agent Service (LangChain)        │ │
│  └──────────┬─────────────────────────────┘ │
│             │                               │
│  ┌──────────▼─────────────────────────────┐ │
│  │  Repository Layer                      │ │
│  │  (SQLAlchemy Async)                    │ │
│  └──────────┬─────────────────────────────┘ │
└─────────────┼───────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼──────┐      ┌───────▼───────┐
│PostgreSQL│      │  LangChain +  │
│Database  │      │  DeepSeek AI  │
└──────────┘      └───────────────┘
    │
┌───▼──────────┐
│ SeaweedFS/S3 │
│   Storage    │
└──────────────┘
```

---

## 🧰 Технологии

### Backend

- **FastAPI** — современный веб-фреймворк для создания API
- **PostgreSQL** — реляционная база данных (asyncpg для асинхронной работы)
- **SQLAlchemy 2.0** — ORM для работы с базой данных
- **Alembic** — система миграций базы данных
- **LangChain** — фреймворк для работы с LLM
- **DeepSeek AI** — языковая модель для AI-ассистента
- **JWT** — аутентификация и авторизация
- **Pydantic v2** — валидация данных и схемы
- **SeaweedFS/S3** — объектное хранилище для файлов
- **Structlog** — структурированное логирование
- **SQLAdmin** — административная панель
- **Passlib** — хеширование паролей (bcrypt)
- **aiosmtplib** — асинхронная отправка email

### Инфраструктура

- **Docker** — контейнеризация приложения
- **Docker Compose** — оркестрация сервисов
- **Uvicorn** — ASGI-сервер для FastAPI
- **Alembic** — миграции базы данных

---

## 🚀 Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Git
- UV

### Через Docker (рекомендуется)

```bash
# Клонируйте репозиторий
git clone https://github.com/FaceX-geo/rahma-api.git
cd rahma-api

# Скопируйте файл с переменными окружения
cp .env.example .env

# Отредактируйте .env файл и настройте необходимые параметры
# Особенно важно настроить:
# - API_JWT__SECRET
# - API_USER_TOKEN__SECRET
# - API_AI__API_KEY (DeepSeek API ключ)
# - API_SMTP__* (настройки почты)

# Запустите сервисы
docker-compose up --build -d

# Проверьте статус
docker-compose ps

# Просмотрите логи
docker-compose logs -f backend
```

После запуска:

- **Backend API** доступен на: **[http://localhost:8000](http://localhost:8000)**
- **Swagger UI**: **[http://localhost:8000/docs](http://localhost:8000/docs)**
- **ReDoc**: **[http://localhost:8000/redoc](http://localhost:8000/redoc)**
- **Scalar**: **[http://localhost:8000/scalar](http://localhost:8000/scalar)**
- **Админ-панель**: **[http://localhost:8000/admin](http://localhost:8000/admin)**

### Локальная разработка

```bash
uv sync

# Настройте переменные окружения в .env
# Запустите миграции
alembic upgrade head

# Запустите сервер разработки
uv run fastapi dev
```

---

## ⚙️ Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
# Backend
API_PORT=8000

# Database (PostgreSQL)
API_DB__USER=postgres
API_DB__PASSWORD=your_password
API_DB__DATABASE=rahma
API_DB__HOST=db  # или localhost для локальной разработки
API_DB__PORT=5432

# S3/SeaweedFS Storage
API_S3__ENDPOINT="https://s3.geometria.ru/"
API_S3__ACCESS_KEY="your_access_key"
API_S3__SECRET_KEY="your_secret_key"
API_S3__SECURE=True
API_S3__BUCKET="rahma-test"

# SMTP (Email)
API_SMTP__HOST=smtp.yandex.com
API_SMTP__PORT=465
API_SMTP__USERNAME=your_email@yandex.ru
API_SMTP__PASSWORD=your_app_password
API_SMTP__SENDER_EMAIL=your_email@yandex.ru
API_SMTP__USE_TLS=1
API_SMTP__START_TLS=0

# JWT Authentication
API_JWT__SECRET=CHANGE_ME_JWT_SECRET  # Обязательно измените!
API_JWT__LIFETIME_SECONDS=900  # 15 минут

# Refresh Token
API_REFRESH_TOKEN__LIFETIME_SECONDS=2592000  # 30 дней

# User Token
API_USER_TOKEN__SECRET=CHANGE_ME_USER_TOKEN_SECRET  # Обязательно измените!
API_USER_TOKEN__LIFETIME_SECONDS=900

# AI (DeepSeek)
API_AI__API_KEY=your-deepseek-api-key
API_AI__MODEL=deepseek-chat

# JES Integration (eSIM)
API_JES__BASE_URL=https://alpha3.jes.ai
API_JES__API_KEY=your-jes-api-key
API_JES__TIMEOUT_SECONDS=10.0
```

### Важные замечания

- **Обязательно измените** `API_JWT__SECRET` и `API_USER_TOKEN__SECRET` на уникальные значения

---

## 📁 Структура репозитория

```
rahma-api/
├── app/
│   ├── admin/              # Административная панель (SQLAdmin)
│   │   ├── views/          # Представления для админки
│   │   └── admin.py        # Конфигурация админки
│   │
│   ├── api/
│   │   ├── middlewares/    # Middleware (логирование, correlation ID)
│   │   └── v1/
│   │       ├── routers/    # API роутеры
│   │       │   ├── amal_router.py
│   │       │   ├── route_router.py
│   │       │   ├── messages_router.py
│   │       │   ├── country_router.py
│   │       │   └── user/   # Роутеры для пользователей
│   │       ├── schemas/     # Pydantic схемы
│   │       └── deps.py      # Зависимости FastAPI
│   │
│   ├── core/               # Ядро приложения
│   │   ├── config.py       # Настройки приложения
│   │   ├── error.py        # Обработка ошибок
│   │   ├── middleware.py   # Настройка middleware
│   │   └── router.py       # Настройка роутеров
│   │
│   ├── db/
│   │   ├── models/         # SQLAlchemy модели
│   │   │   ├── user.py
│   │   │   ├── route.py
│   │   │   ├── amal.py
│   │   │   └── ...
│   │   ├── cruds/          # Репозитории (CRUD операции)
│   │   └── engine.py       # Настройка подключения к БД
│   │
│   ├── docs/               # Документация API
│   │   ├── openapi.py      # OpenAPI конфигурация
│   │   └── scalar.py       # Scalar UI настройки
│   │
│   ├── seeds/              # Сиды для базы данных
│   │   ├── seed_db.py      # Главный скрипт сидов
│   │   ├── factories.py    # Фабрики для тестовых данных
│   │   └── seed/           # Данные для сидов
│   │
│   ├── services/           # Бизнес-логика
│   │   ├── auth/           # Сервисы аутентификации
│   │   ├── route/          # Сервисы маршрутов
│   │   ├── amal/           # Сервисы амалов
│   │   ├── assadik/        # AI-ассистент сервисы
│   │   └── ...
│   │
│   ├── utils/              # Утилиты
│   │   ├── crypto.py       # Криптография
│   │   ├── emailer.py      # Отправка email
│   │   ├── s3.py           # Работа с S3
│   │   └── structlog_config.py  # Настройка логирования
│   │
│   └── main.py             # Точка входа приложения
│
├── alembic/                # Миграции базы данных
│   ├── versions/           # Файлы миграций
│   └── env.py              # Конфигурация Alembic
│
├── .devcontainer/          # Конфигурация Dev Container
├── docker-compose.yaml     # Docker Compose конфигурация
├── Dockerfile              # Docker образ приложения
├── pyproject.toml          # Зависимости проекта
├── alembic.ini             # Конфигурация Alembic
└── README.md               # Этот файл
```

---

## 🌐 API и документация

### Документация API

После запуска приложения доступны следующие интерфейсы документации:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Scalar**: [http://localhost:8000/scalar](http://localhost:8000/scalar)
- **Elements**: [http://localhost:8000/elements](http://localhost:8000/elements)

### Основные API endpoints

| Категория   | Endpoint                          | Описание                                    |
| ----------- | --------------------------------- | ------------------------------------------- |
| **Auth**    | `POST /api/v1/auth/register`     | Регистрация нового пользователя             |
|             | `POST /api/v1/auth/login`         | Вход в систему                              |
|             | `POST /api/v1/auth/verify`       | Верификация email                           |
|             | `POST /api/v1/auth/reset`        | Сброс пароля                                |
| **Users**   | `GET /api/v1/users/me`           | Получить текущего пользователя              |
|             | `PUT /api/v1/users/me`           | Обновить профиль                            |
| **Routes**  | `GET /api/v1/routes`             | Список маршрутов (с пагинацией)             |
|             | `GET /api/v1/routes/{id}`         | Детали маршрута                             |
|             | `GET /api/v1/routes/{id}/hotels`  | Отели маршрута                              |
|             | `GET /api/v1/routes/{id}/restaurants` | Рестораны маршрута                      |
| **Amals**   | `GET /api/v1/amals/sync`         | Получить все амалы пользователя             |
|             | `POST /api/v1/amals/sync`        | Синхронизировать амалы                      |
| **Messages**| `POST /api/v1/messages`          | Отправить сообщение AI-ассистенту           |
| **Countries**| `GET /api/v1/countries`          | Список стран                                |
| **JES**     | `GET /api/v1/jes/*`              | Интеграция с JES (eSIM)                     |
| **Health**  | `GET /health`                     | Проверка состояния сервиса                  |

### Примеры запросов

#### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password",
    "firstName": "Имя",
    "lastName": "Фамилия"
  }'
```

#### Получение маршрутов

```bash
curl -X GET "http://localhost:8000/api/v1/routes?limit=20&offset=0&category=HAJJ" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Отправка сообщения AI-ассистенту

```bash
curl -X POST "http://localhost:8000/api/v1/messages" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Расскажи о маршрутах в Мекку"
  }'
```

---

## 🧑‍💻 Разработка и деплой

### Команды Docker

```bash
# Запуск всех сервисов
docker-compose up -d

# Пересборка и запуск
docker-compose up --build -d

# Остановка сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f db

# Выполнение команд в контейнере
docker-compose exec backend bash

# Перезапуск сервиса
docker-compose restart backend
```

### Миграции базы данных

```bash
# Создание новой миграции
docker-compose exec backend alembic revision --autogenerate -m "описание изменений"

# Применение миграций
docker-compose exec backend alembic upgrade head

# Откат миграции
docker-compose exec backend alembic downgrade -1
```

### Заполнение базы данных (Seeds)

```bash
# Запуск сидов
docker-compose exec backend python -m app.seeds.seed_db
```

### Форматирование кода

```bash
# Проверка стиля кода
ruff check .

# Автоисправление
ruff check --fix .

# Форматирование
ruff format .
```


## 📚 Полезные ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [DeepSeek Platform](https://platform.deepseek.com/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 🤝 Контакты и поддержка

- **Контакты**: [Telegram](https://t.me/macniel3)
- **Компания**: [FaceX](https://facex.pro)
- **Репозиторий**: [GitHub](https://github.com/FaceX-geo/rahma-api)

---

<div align="center">

**Создано с ❤️ командой FaceX**

[![Python](https://img.shields.io/badge/Python-000?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-000?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-000?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

</div>
