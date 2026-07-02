# TODO Manager API

A robust REST API service for managing TODO tasks with secure JWT authentication. This project supports multi-user functionality where users can register, authenticate, and manage their private tasks.

## How it works

The application is built around a secure authentication flow. Users first register an account and then log in using their credentials to receive a JWT (JSON Web Token). This access token must be included in the `Authorization: Bearer <token>` header of subsequent requests to identify and authenticate the user. 

Once authenticated, users can create, read, update, and delete their own tasks. The API enforces strict data isolation at the database level, ensuring that users can only access and modify tasks that belong to them.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (Async)
- **Migrations**: Alembic
- **Driver**: asyncpg
- **Authentication**: JWT & Passlib (bcrypt)
- **Testing**: Pytest, pytest-asyncio, aiosqlite (in-memory test DB)
- **Containerization**: Docker & Docker Compose

## How to run

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the PostgreSQL database via Docker:**
   ```bash
   docker-compose up -d
   ```

4. **Apply database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Explore the API:**
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to interact with the API using the automatically generated Swagger UI.
