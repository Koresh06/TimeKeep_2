# TimeKeep

Система учёта переработок и отгулов для сотрудников МЧС Республики Беларусь.

---

## О проекте

TimeKeep — веб-приложение для автоматизации учёта сверхурочной работы сотрудников МЧС. Сотрудник фиксирует переработки, накапливает часы и подаёт заявку на отгул. Руководитель отдела модерирует заявки через отдельный интерфейс. Администратор управляет составом подразделения.

### Бизнес-логика

- Сотрудник вносит переработку: дата, временной промежуток, описание
- Переработки накапливаются; для отгула нужен минимальный порог часов
- Заявка на отгул уходит на модерацию; списание идёт по принципу FIFO
- После подтверждения сотрудник скачивает рапорт в формате `.docx`

**Режимы работы:**
- `daily` — ежедневный, порог **8 часов** на один отгул
- `shift` — сменный, порог **24 часа** на один отгул

---

## Стек технологий

| Слой | Технологии |
|---|---|
| Backend | FastAPI, Uvicorn, Python 3.12 |
| База данных | PostgreSQL 16, SQLAlchemy 2.0 async, Alembic |
| Кеширование | Redis 7 |
| DI контейнер | Dishka |
| Авторизация | JWT (python-jose), bcrypt (passlib) |
| Мониторинг | Sentry |
| Конфигурация | pydantic-settings |
| Пакетный менеджер | uv |
| Frontend | React 19, Vite, React Router 7, Tailwind CSS 4 |
| HTTP-клиент | Axios |
| Деплой | Docker, Docker Compose, Nginx |

---

## Архитектура Backend

Чистая архитектура с CQRS через паттерн Mediator:

```
src/
  core/           # конфигурация, логирование
  domain/         # сущности, value objects, интерфейсы, перечисления
  application/    # use cases, mediator, DTO
  infrastructure/ # SQLAlchemy репозитории, Redis кеш, JWT, bcrypt
  presentation/   # FastAPI роутеры, Dishka DI, Pydantic-схемы
```

- **Domain** не зависит от инфраструктуры и HTTP
- **Use cases** оформлены как Command/Query, диспетчеризация через Mediator
- **Redis** кеширует справочники (организации, подразделения)
- **Rate limiting** — 300 запросов в минуту на IP

---

## Роли пользователей

| Роль | Доступ |
|---|---|
| `user` | свои переработки, отгулы, статистика, профиль |
| `moderator` | + переработки и отгулы отдела, модерация заявок |
| `admin` | + данные организации, управление режимами работы сотрудников |
| `super_admin` | + все данные, смена ролей, активация/деактивация пользователей |

Роли иерархические — каждая включает права предыдущей. Роль закодирована в JWT и декодируется на фронтенде для ролевой маршрутизации.

---

## Структура организации

```
Организация
  └── Подразделение (отдел)
        └── Сотрудник
```

---

## API

Интерактивная документация: `http://localhost:8000/docs`

### Auth (публичные)
| Метод | Путь | Описание |
|---|---|---|
| `POST` | `/auth/register` | Регистрация нового пользователя |
| `POST` | `/auth/login` | Вход, получение JWT |
| `GET` | `/auth/organizations` | Список организаций для регистрации |
| `GET` | `/auth/departments` | Список подразделений (фильтр по `organization_id`) |

### Переработки
| Метод | Путь | Роль |
|---|---|---|
| `POST` | `/overtimes` | user+ |
| `DELETE` | `/overtimes/{id}` | user+ |
| `GET` | `/overtimes/me` | user+ |
| `GET` | `/overtimes/current-department` | moderator+ |
| `GET` | `/overtimes/current-organization` | admin+ |
| `GET` | `/overtimes` | super_admin |

Все GET-эндпоинты поддерживают `?offset=0&limit=20`.

### Отгулы
| Метод | Путь | Роль |
|---|---|---|
| `POST` | `/day-offs` | user+ |
| `GET` | `/day-offs/me` | user+ |
| `GET` | `/day-offs/current-department` | moderator+ |
| `GET` | `/day-offs/current-organization` | admin+ |
| `GET` | `/day-offs` | super_admin |
| `PATCH` | `/day-offs/{id}/moderate?is_approved=true` | moderator+ |
| `GET` | `/day-offs/{id}/report` | user+ |

Фильтр по статусу: `?status=pending|approved|rejected`. Пагинация: `?offset=0&limit=20`.

### Статистика
| Метод | Путь | Роль |
|---|---|---|
| `GET` | `/statistics/me` | user+ |
| `GET` | `/statistics/current-department` | moderator+ |
| `GET` | `/statistics/current-organization` | admin+ |
| `GET` | `/statistics` | super_admin |

Возвращает: количество переработок, суммарные/доступные часы, распределение отгулов по статусам, помесячная разбивка переработок.

### Пользователи
| Метод | Путь | Роль |
|---|---|---|
| `GET` | `/users/me` | user+ |
| `GET` | `/users/current-department` | moderator+ |
| `GET` | `/users/current-organization` | admin+ |
| `GET` | `/users` | super_admin |
| `PATCH` | `/users/{id}/work-mode` | admin+ |
| `PATCH` | `/users/{id}/role` | super_admin |
| `PATCH` | `/users/{id}/activate` | super_admin |

### Справочники
| Метод | Путь | Роль |
|---|---|---|
| `POST` | `/organizations` | super_admin |
| `GET` | `/organizations/{id}` | admin+ |
| `GET` | `/organizations` | super_admin |
| `POST` | `/departments` | admin+ |
| `GET` | `/departments/{id}` | moderator+ |
| `GET` | `/departments/organization/{id}` | admin+ |

---

## Frontend

Адаптивный SPA на React 19. Дизайн в стилистике МЧС Беларуси — тёмная тема с синей навигацией и красным акцентом.

### Страницы

| Страница | Путь | Доступ |
|---|---|---|
| Вход | `/login` | публичная |
| Регистрация | `/register` | публичная |
| Главная | `/dashboard` | user+ |
| Переработки | `/overtimes` | user+ |
| Отгулы | `/day-offs` | user+ |
| Статистика | `/statistics` | user+ |
| Отдел | `/moderation` | moderator+ |
| Управление | `/admin` | admin+ |
| Профиль | `/profile` | user+ |

### Ключевые возможности

- **Регистрация** — 3-шаговый wizard: учётные данные → личные данные → выбор организации/подразделения
- **Статистика** — SVG-графики: столбчатый (часы по месяцам), кольцевой (статусы отгулов); переключение scope по роли
- **Страница отдела** (moderator+) — вкладки: отгулы с кнопками одобрить/отклонить, переработки, список сотрудников
- **Управление** (admin+) — inline-смена режима работы и роли, активация/деактивация
- **Пагинация** — offset/limit на всех таблицах
- **Фильтрация** — статус на отгулах (все / ожидает / одобрен / отклонён)
- **Роль в JWT** — декодируется на клиенте, управляет видимостью маршрутов и пунктов навигации

---

## Запуск через Docker Compose

```bash
git clone <repo>
cd TimeKeep_2

# Настроить переменные окружения
cp backend/.env.example backend/.env
cp backend/.env.db.example backend/.env.db
# Отредактировать backend/.env и backend/.env.db

docker compose up -d --build
```

Сервисы:
- **Frontend** → `http://localhost:80`
- **Backend API** → `http://localhost:8000`
- **Swagger UI** → `http://localhost:8000/docs`

### Переменные окружения (`backend/.env`)

```env
APP_CONFIG__DB__NAME=timekeep
APP_CONFIG__DB__USER=my_user
APP_CONFIG__DB__PASSWORD=your_password
APP_CONFIG__DB__HOST=db
APP_CONFIG__DB__PORT=5432

APP_CONFIG__REDIS__HOST=redis
APP_CONFIG__REDIS__PORT=6379

APP_CONFIG__SECURITY__SECRET_KEY=your_secret_key
APP_CONFIG__SECURITY__ALGORITHM=HS256
APP_CONFIG__SECURITY__ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_CONFIG__SECURITY__REFRESH_TOKEN_EXPIRE_MINUTES=60

APP_CONFIG__APP__ALLOWED_ORIGINS=["http://localhost","http://localhost:5173"]
APP_CONFIG__APP__SENTRY_DSN=  # опционально
```

```env
# backend/.env.db
POSTGRES_DB=timekeep
POSTGRES_USER=my_user
POSTGRES_PASSWORD=your_password
```

### Первый запуск

Миграции применяются автоматически при старте контейнера `app`. Создайте первого пользователя через API:

```bash
# Зарегистрировать суперадмина (требуется хотя бы одна организация и подразделение в БД)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","password":"...","surname":"...","first_name":"...","patronymic":"...","position":"...","rank":"полковник внутренней службы","work_mode":"daily","organization_id":1,"department_id":1}'

# Вручную повысить роль через psql
docker exec -it timekeep_db psql -U my_user -d timekeep \
  -c "UPDATE users SET role='SUPER_ADMIN' WHERE login='admin';"
```

---

## Локальная разработка (без Docker)

**Требования:** Python 3.12+, PostgreSQL 16, Redis, uv, Node.js 18+

```bash
# Backend
cd backend
uv sync
alembic upgrade head
uvicorn src.presentation.app:create_app --host 0.0.0.0 --port 8000 --factory --reload

# Frontend (в отдельном терминале)
cd frontend
npm install
npm run dev   # http://localhost:5173
```

---

## Тесты

```bash
cd backend
uv run pytest tests/ -v
```

Интеграционные тесты используют in-memory репозитории — БД не требуется.
