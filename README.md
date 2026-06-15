# TaskManager API

A production-ready Task Management REST API built with FastAPI, PostgreSQL, and Redis — containerized with Docker and deployed on AWS EC2 with a full CI/CD pipeline.

---

## Live Demo

- **Frontend:** http://13.233.55.106
- **API Docs:** http://13.233.55.106:8000/docs

---

## Tech Stack

**Backend**
- FastAPI + Python 3.11
- SQLAlchemy ORM + Alembic migrations
- PostgreSQL (AWS RDS)
- Redis (Upstash): caching
- JWT authentication (access + refresh tokens)
- BCrypt password hashing
- FastAPI-Mail: email notifications
- SlowAPI: rate limiting

**Frontend**
- React + Vite
- Axios
- React Router

**Infrastructure & DevOps**
- Docker + Docker Compose
- AWS EC2: application hosting
- AWS RDS (PostgreSQL): database
- Docker Hub: container registry
- GitHub Actions: CI/CD pipeline
- Terraform: infrastructure as code

---

## Features

### Authentication
- User registration and login
- JWT access tokens (30 min expiry)
- Refresh token flow (7 day expiry)
- BCrypt password hashing

### Tasks
- Full CRUD (Create, Read, Update, Delete)
- Soft delete — tasks are never permanently removed
- Status tracking: `pending` → `in_progress` → `completed`
- Priority levels: `low`, `medium`, `high`
- Due date support
- Pagination (`skip`, `limit`)
- Filtering by status, priority
- Full-text search on title and description
- Due today / overdue filters

### Performance & Security
- Redis caching on `GET /tasks/`
- Rate limiting on sensitive endpoints (5 req/min on login)
- Email notification on task creation (background task)

### DevOps
- Dockerized frontend and backend
- Automated CI/CD via GitHub Actions:
  - Runs tests on every push
  - Builds and pushes Docker images to Docker Hub
  - Runs Alembic migrations against AWS RDS
  - Deploys to EC2 automatically
- Infrastructure provisioned with Terraform (EC2, RDS, Security Groups)
- 12 automated tests (pytest)

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, get tokens |
| POST | `/auth/refresh` | Refresh access token |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create task |
| GET | `/tasks/` | Get all tasks (with filters) |
| GET | `/tasks/{id}` | Get single task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Soft delete task |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update profile |

---

## Project Structure

```
taskmanager/
├── app/
│   ├── core/
│   │   ├── database.py       # SQLAlchemy engine, session, Base
│   │   ├── security.py       # JWT, password hashing
│   │   ├── email.py          # Email notifications
│   │   ├── cache.py          # Redis caching
│   │   └── limiter.py        # Rate limiting
│   ├── models/
│   │   ├── user.py           # User ORM model
│   │   └── task.py           # Task ORM model
│   ├── schemas/
│   │   ├── user.py           # Pydantic schemas
│   │   └── task.py
│   ├── routers/
│   │   ├── auth.py           # Auth endpoints
│   │   ├── tasks.py          # Task endpoints
│   │   └── users.py          # User endpoints
│   ├── dependencies.py       # get_current_user
│   ├── config.py             # Settings via pydantic-settings
│   └── main.py               # FastAPI app entry point
├── alembic/                  # Database migrations
├── tests/                    # pytest test suite
├── terraform/                # AWS infrastructure as code
├── frontend/                 # React + Vite frontend
├── Dockerfile                # Backend Docker image
├── docker-compose.yml        # Production compose
├── docker-compose.dev.yml    # Local development compose
└── .github/workflows/
    └── deploy.yml            # CI/CD pipeline
```

---

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker Desktop

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/sharanzzgit/taskmanager.git
cd taskmanager

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in your .env values

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Run with Docker

```bash
docker-compose -f docker-compose.dev.yml up --build
```

---

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=rediss://...
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
ALLOWED_ORIGINS=http://localhost:5173
```

---

## CI/CD Pipeline

Every push to `main` triggers:

```
Run Tests (pytest)
       ↓
Build Docker Images
       ↓
Push to Docker Hub
       ↓
Run Alembic Migrations on AWS RDS
       ↓
SSH into EC2
       ↓
Pull latest images
       ↓
Restart containers
```

---

## Infrastructure (Terraform)

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Provisions:
- AWS RDS PostgreSQL instance
- AWS EC2 instance (Ubuntu 22.04)
- Security groups (ports 22, 80, 8000)
- SSH key pair

---

## Running Tests

```bash
pytest -v
```

12 tests covering auth, tasks, and user profile endpoints.

---

## Author

**Sharan** — Backend Engineer  
[GitHub](https://github.com/sharanzzgit) · [LinkedIn](https://linkedin.com/in/yourprofile)
