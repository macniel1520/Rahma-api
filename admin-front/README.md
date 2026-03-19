# Admin Front

Новая админка Rahma на `React + Vite`.

Назначение:

- заменить SQLAdmin удобной отдельной панелью
- работать с той же БД и тем же `/api/v1`
- получать метаданные ресурсов из `panel-api`
- автоматически подключать новые публичные API-методы в универсальном разделе `API методы`

Основные каталоги:

- `src/` — React приложение
- `index.html` — Vite entry
- `vite.config.js` — сборка фронтенда для раздачи через FastAPI на `/panel`

Запуск локальной разработки:

```bash
cd /Users/facex/Desktop/проекты/rahma-api/admin-front
npm install
npm run dev
```

Production build в контейнере собирается через `Dockerfile` и кладётся в `admin-front/dist`.
