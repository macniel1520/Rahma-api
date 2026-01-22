APP_NAME = "Rahma API"
APP_VERSION = "1.0.0"

APP_DESCRIPTION = """
![logo](https://i.ibb.co/hSq8TLD/logo.png)

Ваш путь к Святым местам — **с заботой, верой и технологиями**.

[Контакты](https://t.me/macniel3)
[Компания](https://facex.pro)
[Репозиторий](https://github.com/FaceX-geo/rahma-api)
"""

TAGS_METADATA = [
    {
        "name": "auth",
        "description": "Аутентификация, авторизация, регистрация и сброс пароля",
        "externalDocs": {
            "description": "jwt.io",
            "url": "https://www.jwt.io/",
        },
    },
    {
        "name": "users",
        "description": "Пользователи и профили",
    },
    {
        "name": "countries",
        "description": "Страны и маршруты",
    },
    {
        "name": "routes",
        "description": "Маршруты",
    },
    {
        "name": "amals",
        "description": "Амалы",
    },
    {
        "name": "default",
        "description": "Служебные эндпоинты",
    },
]

SERVERS = [
    {"url": "http://localhost:8000", "description": "Development"},
    {"url": "https://rahma.facex.pro", "description": "Staging"},
]
