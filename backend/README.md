# HRMSLite Backend

Production-ready FastAPI backend skeleton for the HRMSLite project.

## Tech Stack

| Layer | Library |
|---|---|
| Web framework | FastAPI 0.111 |
| Async ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL (via asyncpg) |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Settings | pydantic-settings |

## Project Structure

```
backend/
├── alembic/
│   └── env.py            # Async-compatible migration env
├── alembic.ini
├── app/
│   ├── main.py           # Application factory + CORS
│   ├── config.py         # Settings (env vars)
│   ├── database.py       # Async engine, session, Base, get_db
│   ├── models/
│   │   └── base.py       # TimestampMixin (created_at, updated_at)
│   ├── schemas/
│   │   └── health.py     # HealthResponse schema
│   ├── repositories/     # Data-access layer (empty stubs)
│   ├── services/         # Business-logic layer (empty stubs)
│   ├── api/
│   │   └── v1/
│   │       ├── router.py # Aggregated v1 router
│   │       └── health.py # GET /api/v1/health
│   └── exceptions/
│       └── handlers.py   # AppException hierarchy + handler registration
├── requirements.txt
└── .env.example
```

## Getting Started

### 1. Clone & install

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — at minimum set DATABASE_URL
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Health check (pings DB) |
| GET | `/docs` | Interactive Swagger UI |
| GET | `/redoc` | ReDoc documentation |

## Adding a New Feature

1. **Model** → `app/models/<feature>.py` (inherit `Base` + `TimestampMixin`)
2. **Schema** → `app/schemas/<feature>.py` (Pydantic models)
3. **Repository** → `app/repositories/<feature>.py` (DB queries)
4. **Service** → `app/services/<feature>.py` (business logic)
5. **Router** → `app/api/v1/<feature>.py` and register in `app/api/v1/router.py`
6. **Migration** → `alembic revision --autogenerate -m "add <feature>"` then `alembic upgrade head`
