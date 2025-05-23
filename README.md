# 🍽️ Restaurant Table Reservation API

This project is a REST API service for managing table reservations in a restaurant.  
Built with **FastAPI**, **SQLModel**, **PostgreSQL**, and **Docker**.

---

## 🚀 Features

- Manage restaurant tables (create/list/delete)
- Create, view, and delete reservations
- Prevent time conflicts for overlapping reservations
- Modular project structure
- Includes Alembic migrations
- Dockerized setup

---

## 📦 Stack

- FastAPI
- SQLModel
- PostgreSQL
- Alembic
- Docker & docker-compose
- Poetry for dependency management

---

## ⚙️ Getting Started

### 1. After cloning the repository install dependencies:

```
poetry install
```

### 2. Create .env file
```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/restaurant
```

### 3. Start the project
```
docker-compose up --build
```

### 4. Run Alembic migrations
In a separate terminal:

```
docker-compose exec web alembic upgrade head
```

## 🧪 API Docs

Once the app is running, visit:

Swagger UI: http://localhost:8000/docs <br>
ReDoc: http://localhost:8000/redoc

## ✅ Example Requests

### Create Table
```
POST /tables/
{
  "name": "Table 1",
  "seats": 4,
  "location": "Window"
} 
```

### Create Reservation
```
POST /reservations/
{
  "customer_name": "John Doe",
  "table_id": 1,
  "reservation_time": "2025-04-09T19:00:00",
  "duration_minutes": 60
}
```

## 🧠 Tests

Checking reservation basic function and conflicts (same table, overlapping time)
```
poetry run pytest
```

## 🗒 Notes 

Migrations must be run after first start<br>
.env file required
