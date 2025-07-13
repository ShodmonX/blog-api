# 📝 Blog REST API

Blog REST API is a modern, secure backend API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, and Docker. It provides user authentication via JWT and CRUD operations for blog posts.

## 🚀 Technologies Used

- 🔧 **FastAPI** — High-performance web framework
- 🐘 **PostgreSQL** — Advanced relational database
- ⚙️ **SQLAlchemy** — ORM for database operations
- 🧪 **Alembic** — Database migration tool
- 🐳 **Docker** — Containerization platform
- 🔐 **JWT Authentication** — Secure access via tokens
- 🧪 **Pytest** — For testing

---

## 📁 API Endpoints

### 👤 Users

| Endpoint        | Method | Auth Required | Description         |
|-----------------|--------|---------------|---------------------|
| `/users/`       | POST   | ❌            | Register new user   |
| `/users/me`     | GET    | ✅            | Get current user    |

### 🔐 Authentication

| Endpoint        | Method | Auth Required | Description     |
|-----------------|--------|---------------|-----------------|
| `/login`        | POST   | ❌            | Login and get token |

### 📝 Posts

| Endpoint             | Method | Auth Required | Description        |
|----------------------|--------|---------------|--------------------|
| `/posts/`            | GET    | ❌            | Get all posts      |
| `/posts/`            | POST   | ✅            | Create new post    |
| `/posts/{post_id}`   | GET    | ❌            | Get post by ID     |
| `/posts/{post_id}`   | PUT    | ✅            | Update post        |
| `/posts/{post_id}`   | DELETE | ✅            | Delete post        |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository:

```bash
git clone https://github.com/your-username/blog-api.git
cd blog-api
```

### 2️⃣ Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/blogdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=blogdb
SECRET_KEY=myjwtsecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Running with Docker

### 3️⃣ Build and run the containers:

```bash
docker-compose up --build
```

Visit: `http://localhost:8000`

### 4️⃣ Run Alembic migrations:

```bash
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"
docker-compose exec backend alembic upgrade head
```

---

## 🧪 Run Tests

```bash
pytest
```

---

## 🔐 JWT Authentication

- Use `/login` with `username` (email) and `password` to get an access token.
- Add the token in `Authorization: Bearer <token>` header for protected endpoints.

---

## 🧠 Swagger & Redoc

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📂 Project Structure

```text
blog-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── dependencies.py
│   ├── auth.py
│   ├── utils.py
│   ├── routers/
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── auth.py
│   └── config.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── test_users.py
│   ├── test_posts.py
│   └── conftest.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ✨ Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

---

## 📜 License

This project is licensed under the MIT License.