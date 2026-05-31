# TimeKeep

Система учёта переработок и отгулов для сотрудников МЧС Республики Беларусь.

---

## О проекте

TimeKeep — серверное приложение для автоматизации учёта переработок сотрудников МЧС. Система позволяет сотрудникам фиксировать отработанное сверхурочное время, формировать заявки на отгул и получать готовый рапорт по установленному шаблону МЧС.

### Бизнес-логика

Сотрудник накапливает переработки, указывая дату, временной промежуток и описание (например, "работа по жилью"). Когда накоплено достаточно часов, он подаёт заявку на отгул. Заявка уходит на модерацию руководителю отдела. После подтверждения сотруднику становится доступен рапорт в формате .docx по официальному шаблону МЧС.

**Два режима работы:**
- Ежедневник (8-часовой) — для получения отгула нужно накопить 8 часов
- Трёхсменник (24-часовой) — для получения отгула нужно накопить 24 часа

**Списание переработок** происходит по принципу FIFO — самые ранние переработки списываются первыми. Последняя переработка в очереди может списаться частично — остаток сохраняется для следующего отгула.

---

## Стек технологий

| Слой | Технологии |
|---|---|
| Фреймворк | FastAPI, Uvicorn |
| База данных | PostgreSQL, SQLAlchemy 2.0 async, Alembic |
| Кеширование | Redis |
| DI контейнер | Dishka |
| Авторизация | JWT (python-jose), bcrypt (passlib) |
| Генерация документов | python-docx |
| Мониторинг | Sentry |
| Тесты | pytest, pytest-asyncio |
| Конфигурация | pydantic-settings |
| Пакетный менеджер | uv |
| Деплой | Docker, Docker Compose |

---

## Архитектура

Проект построен на принципах **чистой архитектуры** с разделением на слои:

```
src/
  core/           # энумы, исключения, конфигурация
  domain/         # бизнес-сущности, value objects, интерфейсы
  application/    # use cases, mediator, DTO
  infrastructure/ # SQLAlchemy репозитории, Redis кеш, сервисы
  presentation/   # FastAPI роутеры, Dishka DI, схемы
```

**Принцип зависимостей:** `infrastructure` и `presentation` зависят от `domain` и `application`, но не наоборот. Доменный слой не знает ни о базе данных, ни о HTTP.

**CQRS через Mediator:** все операции оформлены как команды (`Command`) или запросы (`Query`). Роутер отправляет команду в медиатор, медиатор находит нужный хэндлер.

**Кеширование:** организации, департаменты и профили пользователей кешируются в Redis. При изменении данных кеш инвалидируется автоматически.

---

## Роли пользователей

| Роль | Доступ |
|---|---|
| `USER` | свои переработки и отгулы |
| `MODERATOR` | переработки и отгулы своего департамента, модерация заявок |
| `ADMIN` | вся организация, управление пользователями |
| `SUPER_ADMIN` | вся система |

Роли иерархические — каждая роль включает права предыдущей.

---

## Структура организации

```
Организация (отдел МЧС в городе/районе)
  └── Департамент (подразделение: инспекция, пожаротушение и т.д.)
        └── Сотрудник
```

---

## API

Полная документация доступна по адресу `/docs` после запуска.

**Auth**
- `POST /auth/register` — регистрация пользователя (ADMIN+)
- `POST /auth/login` — вход, получение JWT токена

**Переработки**
- `POST /overtimes` — внести переработку (USER+)
- `DELETE /overtimes/{id}` — удалить переработку (USER+)
- `GET /overtimes/me` — свои переработки (USER+)
- `GET /overtimes/department` — переработки департамента (MODERATOR+)
- `GET /overtimes/organization` — переработки организации (ADMIN+)
- `GET /overtimes` — все переработки (SUPER_ADMIN)

**Отгулы**
- `POST /day-offs` — взять отгул (USER+)
- `GET /day-offs/me` — свои отгулы (USER+)
- `GET /day-offs/department` — отгулы департамента (MODERATOR+)
- `GET /day-offs/organization` — отгулы организации (ADMIN+)
- `GET /day-offs` — все отгулы (SUPER_ADMIN)
- `PATCH /day-offs/{id}/moderate` — подтвердить/отклонить (MODERATOR+)
- `GET /day-offs/{id}/report` — скачать рапорт .docx (USER+)

**Пользователи**
- `GET /users/me` — свой профиль (USER+)
- `GET /users/department` — пользователи департамента (MODERATOR+)
- `GET /users/organization` — пользователи организации (ADMIN+)
- `GET /users` — все пользователи (SUPER_ADMIN)
- `PATCH /users/{id}/role` — изменить роль (ADMIN+)
- `PATCH /users/{id}/work-mode` — изменить режим работы (ADMIN+)
- `PATCH /users/{id}/activate` — активировать/деактивировать (ADMIN+)

**Организации**
- `POST /organizations` — создать организацию (SUPER_ADMIN)
- `GET /organizations/{id}` — получить организацию (ADMIN+)
- `GET /organizations` — все организации (SUPER_ADMIN)

**Департаменты**
- `POST /departments` — создать департамент (ADMIN+)
- `GET /departments/{id}` — получить департамент (MODERATOR+)
- `GET /departments/organization/{id}` — департаменты организации (ADMIN+)

---

## Запуск через Docker

```bash
# клонировать репозиторий
git clone https://github.com/your/timekeep.git
cd timekeep

# создать .env файлы
cp .env.example .env
cp .env.db.example .env.db

# запустить
make build

# создать суперадмина
make super-user
```

### Управление через Makefile

```bash
make up          # запустить
make down        # остановить
make build       # пересобрать и запустить
make logs        # логи
make migrate     # применить миграции
make super-user  # создать суперадмина
make test        # запустить тесты
```

---

## Запуск локально

### Требования
- Python 3.12+
- PostgreSQL 16
- Redis
- uv

### Установка

```bash
uv sync
cp .env.example .env
alembic upgrade head
python -m src.scripts.create_super_user
uvicorn src.presentation.app:create_app --host 0.0.0.0 --port 8000 --factory --reload
```

### Настройка `.env`

```env
APP_CONFIG__DB__NAME=timekeep
APP_CONFIG__DB__USER=my_user
APP_CONFIG__DB__PASSWORD=12345
APP_CONFIG__DB__HOST=localhost
APP_CONFIG__DB__PORT=5432
APP_CONFIG__REDIS__HOST=localhost
APP_CONFIG__REDIS__PORT=6379
APP_CONFIG__SECURITY__SECRET_KEY=your_secret_key_here
APP_CONFIG__SECURITY__ALGORITHM=HS256
APP_CONFIG__SECURITY__ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_CONFIG__SECURITY__REFRESH_TOKEN_EXPIRE_MINUTES=60
APP_CONFIG__APP__SENTRY_DSN=your_sentry_dsn
```

---

## Тесты

```bash
make test
pytest tests/unit/ -v
pytest tests/integration/ -v
```

Интеграционные тесты используют in-memory репозитории — база данных не нужна.

---

## Рапорт

После подтверждения отгула модератором сотрудник может скачать рапорт в формате .docx по официальному шаблону МЧС РБ.

Пример рапорта:
```
Начальнику Невского РОЧС
полковнику внутренней службы
Иванову И.И.

20.09.2024
Рапорт

Прошу предоставить мне выходной день 21.09.2024, за ранее
отработанное время: 20.04.2024 – работа по жилью (4 ч.);
21.04.2024 – работа по жилью (2 ч.).

Инспектор СНиП Невского РОЧС
лейтенант внутренней службы        А.А.Корец
```