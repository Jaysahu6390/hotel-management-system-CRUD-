# 🏨 Hotel Management System

A full-stack Hotel Management System built with Django and MySQL to manage hotel operations efficiently. The project includes room management, customer management, booking management, authentication, payment management, REST APIs, Docker support, and background task processing with Celery.

---

## 🚀 Features

- User Authentication
- Dashboard
- Room Management (CRUD)
- Customer Management (CRUD)
- Booking Management (CRUD)
- Payment Management
- Django REST Framework API
- Audit Logs
- Email Notifications
- Docker & Docker Compose
- Celery & Redis Integration
- Responsive UI

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Django REST Framework

### Frontend
- HTML
- CSS
- Bootstrap

### Database
- MySQL

### DevOps
- Docker
- Docker Compose
- Gunicorn
- Nginx

### Background Tasks
- Celery
- Redis

---

## 📂 Project Structure

```text
hotel_management/
│
├── accounts/
├── api/
├── audit/
├── bookings/
├── customers/
├── payments/
├── rooms/
├── templates/
├── static/
├── media/
├── hotel_management/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone <repository-url>
cd hotel_management
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and configure:

- SECRET_KEY
- DEBUG
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT

### Apply Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Server

```bash
python manage.py runserver
```

---

## 🐳 Docker

```bash
docker compose up --build
```

---

## 📡 API

Example endpoints:

```
/api/rooms/
/api/customers/
/api/bookings/
/api/payments/
```
---

