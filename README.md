# Blog API -- FastAPI + PostgreSQL + Redis

A modern, asynchronous, and production-ready **Blog Backend API** built
with FastAPI.\
Features include JWT authentication (with HttpOnly refresh tokens),
Docker, Alembic migrations, Redis integration, Pytest (80%+ coverage),
and GitHub Actions CI.

![Tests](https://github.com/ShodmonX/blog-api/workflows/Tests/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)

## 🚀 Features

-   Fully async **FastAPI** backend\
-   **JWT authentication** (access + refresh tokens stored in HttpOnly
    cookies)\
-   **PostgreSQL** with SQLAlchemy 2.0 (async)\
-   **Redis** for refresh token storage & optional caching\
-   Full **CRUD** for Posts & Users\
-   User profile update\
-   **Pydantic v2** schemas\
-   **Alembic** for database migrations\
-   **Docker** & docker-compose (development + production)\
-   **Pytest** with 80%+ coverage (async tests)\
-   **GitHub Actions** CI integration

## 🛠 Tech Stack

-   FastAPI\
-   PostgreSQL + asyncpg\
-   Redis\
-   SQLAlchemy 2.0 (async)\
-   Alembic\
-   Pydantic-settings\
-   JWT (HttpOnly cookies)\
-   Docker / docker-compose\
-   Pytest + httpx\
-   GitHub Actions

## ⚡ Quick Start (Recommended: Docker)

``` bash
git clone https://github.com/ShodmonX/blog-api.git
cd blog-api
cp .env.example .env
docker compose up --build -d
docker compose exec web alembic upgrade head
```

### URLs

-   API Root: http://localhost:8000
-   Swagger UI: http://localhost:8000/docs
-   Health Check: http://localhost:8000/health

## 🔧 Manual Setup (Without Docker)

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## 🔐 Environment Variables (.env)

    PROJECT_NAME=BLOG API
    VERSION=0.1.0
    JWT_SECRET=local-super-secret-key-1234567890-change-in-prod
    JWT_ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_DAYS=7
    DATABASE_URL=postgresql+asyncpg://user:password@db:5433/blogapi
    DEBUG=1
    REDIS_HOST=redis
    REDIS_PORT=6380
    REDIS_DB=7

## 📡 API Endpoints

  Method   Endpoint         Description                Auth
  -------- ---------------- -------------------------- --------
  POST     /auth/register   User registration          --
  POST     /auth/login      Login (returns cookies)    --
  POST     /auth/refresh    Refresh access token       Cookie
  POST     /auth/logout     Logout                     Cookie
  GET      /users/me        Get current user profile   Yes
  PUT      /users/me        Update profile             Yes
  POST     /posts/          Create new post            Yes
  GET      /posts/          Get all posts              --
  GET      /posts/{id}      Get single post            --
  PUT      /posts/{id}      Update post (owner only)   Yes
  DELETE   /posts/{id}      Delete post (owner only)   Yes

## 🧪 Testing

``` bash
pytest
pytest --cov=app
```

## 🚀 Production Deployment

-   Render.com\
-   Railway\
-   Fly.io

### VPS (e.g., Contabo)

``` bash
docker-compose -f docker-compose.yml up -d
```

## 👨‍💻 Author

ShodmonX -- 2025\
GitHub: https://github.com/ShodmonX

## ✨ Contributing

Contributions are welcome!

## 📜 License

[MIT License](LICENCE)