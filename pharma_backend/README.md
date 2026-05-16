# PharmaManager Backend

Django REST Framework backend for PharmaManager.

## Stack

* Django 5
* Django REST Framework
* PostgreSQL
* JWT Authentication
* drf-spectacular
* django-filter

---

# Backend Structure

```bash
pharma_backend/
│
├── apps/
│   ├── categories/
|   ├── core/
│   ├── medicaments/
│   ├── ventes/
│   └──  users/
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   └── local.py
│
├── requirements.txt
└── .env.example
```

---

# Installation

## 1. Create virtual environment

```bash
python -m venv venv
```

## 2. Activate environment

### Windows

```bash
. venv/Scripts/activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create `.env` file:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DB_NAME=pharma_manager_db
DB_USER=postgres/pharma_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

## 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Run server

```bash
python manage.py runserver
```

Backend available at:

```txt
http://localhost:8000
```

---

# Swagger Documentation

```txt
http://localhost:8000/api/schema/swagger-ui/
```

---

# Main Features

* JWT Authentication
* CRUD Medicaments
* CRUD Categories
* Sales management
* Stock alerts
* Expired medications endpoint
* Soft delete
* Filtering & search
* Pagination

---

# Docker

From project root:

```bash
docker compose up --build
```
