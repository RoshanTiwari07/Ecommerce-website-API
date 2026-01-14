# FastShip - E-Commerce Shipment Management System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-6+-red.svg)](https://redis.io)

A comprehensive, production-ready FastAPI application for managing e-commerce shipments, products, sellers, and delivery partners with real-time tracking, JWT authentication, email notifications, and RESTful APIs.

## 📋 Table of Contents
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Database Migrations](#-database-migrations)
- [API Endpoints](#-api-endpoints)
- [Development](#-development)
- [Production Deployment](#-production-deployment)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Functionality
- **Shipment Management**: Create, track, and manage shipments with real-time status updates
- **Product Catalog**: Comprehensive product management with inventory tracking
- **Multi-Party System**: Support for Sellers and Delivery Partners
- **Order Fulfillment**: Automated product-shipment association with stock management
- **Timeline Tracking**: Detailed shipment event history with location tracking
- **Delivery Partner Assignment**: Intelligent assignment based on zip codes and capacity

### Technical Features
- **JWT Authentication**: Secure token-based authentication for sellers and delivery partners
- **Email Notifications**: Asynchronous email delivery using FastMail
- **Token Blacklisting**: Redis-based JWT token revocation for secure logout
- **Database Migrations**: Version-controlled schema changes with Alembic
- **Async Operations**: Full async/await support for high performance
- **API Documentation**: Auto-generated interactive docs with Scalar UI
- **Type Safety**: SQLModel for type-safe database operations
- **Relationship Management**: Complex many-to-many relationships handled efficiently

## 🏗️ System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Client    │────────▶│  FastAPI     │────────▶│ PostgreSQL  │
│ Application │         │  Application │         │  Database   │
└─────────────┘         └──────────────┘         └─────────────┘
                              │                           
                              │                           
                         ┌────▼─────┐            ┌─────────────┐
                         │  Redis   │            │  FastMail   │
                         │  Cache   │            │  Service    │
                         └──────────┘            └─────────────┘
```

### Application Layers
1. **API Layer** (`app/api`): Route handlers, request validation, response serialization
2. **Service Layer** (`app/services`): Business logic, data validation, orchestration
3. **Database Layer** (`app/database`): Models, sessions, connections
4. **Core Layer** (`app/core`): Security, authentication, utilities

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI**: Modern, high-performance web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **SQLModel**: SQL databases with Python objects (combines SQLAlchemy + Pydantic)

### Database & Caching
- **PostgreSQL**: Primary relational database with asyncpg driver
- **Redis**: In-memory cache for token blacklisting and session management
- **Alembic**: Database migration tool

### Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication
- **OAuth2 with Password Flow**: Secure login mechanism
- **Passlib with bcrypt**: Password hashing

### Email & Notifications
- **FastMail**: Asynchronous email sending
- **Background Tasks**: Non-blocking email delivery

### Additional Tools
- **Scalar**: Modern API documentation UI
- **python-dotenv**: Environment variable management
- **asyncpg**: Async PostgreSQL driver

## 📦 Prerequisites

Ensure you have the following installed:

| Software    | Version   | Purpose                          |
|-------------|-----------|----------------------------------|
| Python      | 3.10+     | Runtime environment              |
| PostgreSQL  | 13+       | Primary database                 |
| Redis       | 6+        | Token blacklist & caching        |
| pip         | Latest    | Package management               |
| virtualenv  | Latest    | Virtual environment (recommended)|

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB for application + dependencies

## 📁 Project Structure

```
fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Application entry point & lifespan events
│   ├── config.py                  # Settings management (DB, Redis, Email)
│   ├── utils.py                   # Utility functions
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py              # Master router aggregation
│   │   ├── dependencies.py        # Shared dependencies & DI
│   │   │
│   │   ├── routers/               # API route handlers
│   │   │   ├── shipment.py        # Shipment CRUD + assignment
│   │   │   ├── shipment_event.py  # Shipment timeline events
│   │   │   ├── seller.py          # Seller registration & auth
│   │   │   ├── delivery_partner.py# Delivery partner management
│   │   │   └── product.py         # Product catalog management
│   │   │
│   │   └── schemas/               # Pydantic request/response models
│   │       ├── shipment.py
│   │       ├── seller.py
│   │       ├── product.py
│   │       └── delivery_partner.py
│   │
│   ├── core/
│   │   └── security.py            # OAuth2 schemes & token handling
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py              # SQLModel database models
│   │   ├── session.py             # Async database session management
│   │   ├── redis.py               # Redis client & blacklist operations
│   │   └── types.py               # Custom PostgreSQL types (enums)
│   │
│   └── services/                  # Business logic layer
│       ├── base.py                # Base service with common CRUD
│       ├── user.py                # User authentication service
│       ├── seller.py              # Seller-specific logic
│       ├── delivery_partner.py    # Delivery partner logic
│       ├── shipment.py            # Shipment management + validation
│       ├── shipment_event.py      # Timeline event handling
│       ├── product.py             # Product & inventory management
│       └── notification.py        # Email notification service
│
├── migrations/                    # Alembic migration files
│   ├── env.py                     # Migration environment config
│   ├── script.py.mako             # Migration template
│   └── versions/                  # Version-controlled migrations
│       ├── cf35f874f061_initial_migration_with_all_tables.py
│       ├── c4ac17d91caf_add_shipment_product_and_delivery_.py
│       └── 05a5fe893444_add_client_contact_fixed.py
│
├── app.py                         # Standalone email test script
├── alembic.ini                    # Alembic configuration
├── .env                           # Environment variables (DO NOT commit)
├── .env.example                   # Example environment file
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Installation

### Step 1: Clone or Navigate to the Project

```bash
cd c:\Myprojects\fastapi
```

### Step 2: Create a Virtual Environment

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal, indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash
# Upgrade pip (recommended)
python -m pip install --upgrade pip

# Install all dependencies (if requirements.txt exists)
pip install -r requirements.txt
```

**Or install manually:**

```bash
# Core dependencies
pip install fastapi uvicorn[standard]

# Database dependencies
pip install sqlalchemy sqlmodel asyncpg psycopg2-binary alembic

# Authentication
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# Redis
pip install redis

# Settings management
pip install pydantic-settings pydantic[email]

# Email
pip install fastapi-mail

# API documentation
pip install scalar-fastapi

# Other utilities
pip install python-dotenv typing-extensions
```

### Step 4: Save Dependencies (Optional)

To create or update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## ⚙️ Configuration

### Step 1: Environment Variables

Create a `.env` file in the project root directory:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

**.env file content:**
```env
# PostgreSQL Database Configuration
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_USER=postgres
POSTGRES_DB=fastship_db
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT Security Settings
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256

# Email Configuration (for FastMail)
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=noreply@fastship.com
MAIL_FROM_NAME=FastShip Notifications
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USER_CREDENTIALS=True
VALIDATE_CREDENTIALS=True
```

**🔒 Security Best Practices:**
- **Never commit `.env` to version control** (add to `.gitignore`)
- Use strong, randomly generated `JWT_SECRET` (32+ characters)
- Use app-specific passwords for email (not your main password)
- In production, use environment variables or secret management services

**Generate a secure JWT secret:**
```bash
# Python one-liner
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 2: PostgreSQL Setup

**Install PostgreSQL** (if not already installed):
- **Windows:** Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- **macOS:** `brew install postgresql@14`
- **Linux:** `sudo apt-get install postgresql postgresql-contrib`

**Start PostgreSQL:**
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# On Windows: Start via Services or
net start postgresql-x64-14

# On macOS
brew services start postgresql

# On Linux
sudo systemctl start postgresql
```

**Create the Database:**
```bash
# Connect to PostgreSQL
psql -U postgres -h localhost

# Create database
CREATE DATABASE fastship_db;

# Create user (optional, if not using default postgres user)
CREATE USER fastship_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE fastship_db TO fastship_user;

# Exit
\q
```

### Step 3: Redis Setup

**Install Redis:**
- **Windows:** Download from [Redis for Windows](https://github.com/microsoftarchive/redis/releases) or use WSL2
- **macOS:** `brew install redis`
- **Linux:** `sudo apt-get install redis-server`

**Start Redis:**
```bash
# On Windows (if installed via MSI)
redis-server

# On macOS
brew services start redis

# On Linux
sudo systemctl start redis

# Verify Redis is running
redis-cli ping
# Expected response: PONG
```

### Step 4: Email Configuration (Gmail Example)

If using Gmail for email notifications:

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account Settings → Security
   - Select "2-Step Verification" → "App passwords"
   - Generate password for "Mail"
3. Use the generated password in `MAIL_PASSWORD`

For other email providers, adjust `MAIL_SERVER` and `MAIL_PORT` accordingly.

## 🗄️ Database Setup

### Database Models Overview

The application includes the following database models:

1. **User** (base model)
   - Seller (inherits from User)
   - DeliveryPartner (inherits from User)

2. **Shipment** - Core shipment tracking entity
3. **Product** - Product catalog with inventory
4. **ShipmentProduct** - Many-to-many association table
5. **ShipmentEvent** - Timeline tracking for shipments

### Option 1: Automatic Table Creation (Development)

The application automatically creates tables on startup via the lifespan handler:

```python
# In app/main.py
@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()  # Creates all tables
    yield
```

**To use automatic creation:**
```bash
# Simply run the application
uvicorn app.main:app --reload
# Tables will be created automatically
```

### Option 2: Alembic Migrations (Production Recommended)

Alembic provides version-controlled database migrations:

```bash
# View current migration status
alembic current

# Apply all pending migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1

# View migration history
alembic history --verbose
```

**Create a new migration after model changes:**
```bash
alembic revision --autogenerate -m "Add new column to shipment"
```

### Existing Migrations

The project includes these migrations:

1. `cf35f874f061` - Initial migration with all tables
2. `c4ac17d91caf` - Add shipment_product and delivery partner tables
3. `05a5fe893444` - Add client contact fields (email, phone)

### Database Schema Diagram

```
┌─────────────┐
│   Seller    │──┐
└─────────────┘  │
                 │ 1:N
                 ▼
            ┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
            │  Shipment   │◄────►│ ShipmentProduct  │◄────►│   Product   │
            └─────────────┘  N:M  └──────────────────┘  N:M └─────────────┘
                 │ 1:N                                           │
                 │                                               │ N:1
                 ▼                                               ▼
            ┌─────────────┐                                 ┌─────────────┐
            │ShipmentEvent│                                 │   Seller    │
            └─────────────┘                                 └─────────────┘
                                    
            ┌──────────────┐
            │DeliveryPartner│
            └──────────────┘
                 │ 1:N
                 ▼
            ┌─────────────┐
            │  Shipment   │
            └─────────────┘
```

## 🏃 Running the Application

### Development Mode

**Step 1: Activate Virtual Environment**

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**Step 2: Start the Server**

```bash
# With auto-reload (development)
uvicorn app.main:app --reload

# Specify custom host and port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# With more verbose logging
uvicorn app.main:app --reload --log-level debug
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['c:\\Myprojects\\fastapi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Production Mode

```bash
# Without auto-reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using Gunicorn with Uvicorn workers (Linux/macOS)
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Access Points

Once running, the application is available at:

| Service                  | URL                              |
|--------------------------|----------------------------------|
| API Base                 | http://localhost:8000            |
| Swagger UI (Interactive) | http://localhost:8000/docs       |
| Scalar Docs              | http://localhost:8000/scalar     |
| ReDoc                    | http://localhost:8000/redoc      |
| OpenAPI JSON             | http://localhost:8000/openapi.json|

### Health Check

```bash
# Test if the API is running
curl http://localhost:8000/docs

# Or open in browser
start http://localhost:8000/docs  # Windows
open http://localhost:8000/docs   # macOS
```

## 📚 API Documentation

### Interactive Documentation

The FastAPI application provides multiple documentation interfaces:

1. **Swagger UI** - http://localhost:8000/docs
   - Interactive API testing
   - Try endpoints directly from browser
   - View request/response schemas
   - Test authentication flows

2. **Scalar Docs** - http://localhost:8000/scalar
   - Modern, beautiful UI
   - Enhanced developer experience
   - Better code examples
   - Improved navigation

3. **ReDoc** - http://localhost:8000/redoc
   - Clean, responsive design
   - Perfect for API documentation sharing
   - Printable format
   - Deep linking support

### API Base URL

```
http://localhost:8000
```

All endpoints are prefixed as shown in the sections below.

## 🔐 Authentication

The application uses **JWT (JSON Web Tokens)** with OAuth2 Password Flow.

### Authentication Flow

1. **Register** a new seller or delivery partner
2. **Login** to obtain an access token
3. **Use the token** in the `Authorization` header for protected endpoints
4. **Logout** to blacklist the token

### Register a Seller

```http
POST /seller/signup
Content-Type: application/json

{
  "name": "John's Electronics",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "address": "123 Main St",
  "zip_code": 12345
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John's Electronics",
  "email": "john@example.com",
  "email_verified": false,
  "address": "123 Main St",
  "zip_code": 12345,
  "created_at": "2026-01-14T10:30:00"
}
```

### Login

```http
POST /seller/token
Content-Type: application/x-www-form-urlencoded

username=john@example.com&password=SecurePass123!
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the `Authorization` header:

```http
GET /shipment/?id=<shipment-id>
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Logout

```http
POST /seller/logout
Authorization: Bearer <your-token>
```

Tokens are blacklisted in Redis upon logout and cannot be reused.

## 📡 API Endpoints

### Seller Endpoints

| Method | Endpoint            | Description                | Auth Required |
|--------|---------------------|----------------------------|---------------|
| POST   | `/seller/signup`    | Register new seller        | No            |
| POST   | `/seller/token`     | Login and get token        | No            |
| GET    | `/seller/verify`    | Verify email               | No            |
| POST   | `/seller/logout`    | Logout (blacklist token)   | Yes           |

### Product Endpoints

| Method | Endpoint              | Description                    | Auth Required |
|--------|-----------------------|--------------------------------|---------------|
| GET    | `/product/`           | Get product by ID              | No            |
| POST   | `/product/`           | Create new product             | Yes (Seller)  |
| PATCH  | `/product/`           | Update product                 | Yes (Seller)  |
| DELETE | `/product/`           | Delete product                 | Yes (Seller)  |
| GET    | `/product/seller/{id}`| Get all products by seller     | No            |
| GET    | `/product/category/{category}` | Get products by category | No  |

### Shipment Endpoints

| Method | Endpoint                        | Description                      | Auth Required |
|--------|---------------------------------|----------------------------------|---------------|
| GET    | `/shipment/`                    | Get shipment by ID               | No            |
| POST   | `/shipment/`                    | Create new shipment              | Yes (Seller)  |
| PATCH  | `/shipment/`                    | Update shipment                  | Yes (Seller)  |
| DELETE | `/shipment/`                    | Delete shipment                  | Yes (Seller)  |
| GET    | `/shipment/{field}`             | Get specific shipment field      | No            |
| GET    | `/shipment/status/{status}`     | Get shipments by status          | No            |
| PATCH  | `/shipment/{id}/assign-partner` | Assign delivery partner          | Yes (Seller)  |

**Shipment Status Values:**
- `placed`
- `processing`
- `shipped`
- `in_transit`
- `out_for_delivery`
- `delivered`

### Shipment Event Endpoints

| Method | Endpoint                    | Description                        | Auth Required      |
|--------|-----------------------------|------------------------------------|-------------------|
| POST   | `/shipment-event/`          | Create shipment event              | Yes (Delivery Partner) |
| GET    | `/shipment-event/{shipment_id}` | Get timeline for shipment      | No                |

### Delivery Partner Endpoints

| Method | Endpoint                      | Description                    | Auth Required |
|--------|-------------------------------|--------------------------------|---------------|
| POST   | `/delivery-partner/signup`    | Register delivery partner      | No            |
| POST   | `/delivery-partner/token`     | Login and get token            | No            |
| POST   | `/delivery-partner/logout`    | Logout                         | Yes           |
| GET    | `/delivery-partner/`          | Get delivery partner by ID     | No            |
| GET    | `/delivery-partner/available` | Get available partners by zip  | No            |

## 💡 Usage Examples

### Example 1: Create a Product

```bash
# First, login to get token
curl -X POST "http://localhost:8000/seller/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePass123!"

# Create product
curl -X POST "http://localhost:8000/product/" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with 2.4GHz connection",
    "price": 29.99,
    "stock_quantity": 100,
    "category": "Electronics"
  }'
```

### Example 2: Create a Shipment with Products

```bash
curl -X POST "http://localhost:8000/shipment/" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Order #12345",
    "description": "Electronics shipment",
    "price": 99.99,
    "destination": 90210,
    "client_contact_email": "customer@example.com",
    "client_contact_phone": 1234567890,
    "products": [
      {
        "product_id": "550e8400-e29b-41d4-a716-446655440000",
        "quantity": 2
      }
    ]
  }'
```

### Example 3: Track Shipment Status

```bash
# Get all shipments with status "in_transit"
curl -X GET "http://localhost:8000/shipment/status/in_transit"

# Get specific shipment timeline
curl -X GET "http://localhost:8000/shipment-event/<shipment-id>"
```

### Example 4: Update Shipment Event (Delivery Partner)

```bash
curl -X POST "http://localhost:8000/shipment-event/" \
  -H "Authorization: Bearer <delivery-partner-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "shipment_id": "550e8400-e29b-41d4-a716-446655440000",
    "location": "Distribution Center - Los Angeles",
    "zip_code": 90001,
    "status": "in_transit"
  }'
```

## 🔄 Database Migrations

### Alembic Migration Workflow

```bash
# Check current migration version
alembic current

# View migration history
alembic history

# Apply all pending migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade cf35f874f061

# Create new migration after model changes
alembic revision --autogenerate -m "Add new field to model"

# Apply specific migration
alembic upgrade <revision_id>
```

### Creating Migrations

When you modify database models in `app/database/models.py`:

```bash
# 1. Make changes to your models
# 2. Generate migration
alembic revision --autogenerate -m "Descriptive message"

# 3. Review generated migration file in migrations/versions/
# 4. Apply migration
alembic upgrade head
```

### Migration Best Practices

- Always review auto-generated migrations before applying
- Test migrations in development before production
- Keep migrations small and focused
- Write descriptive migration messages
- Never modify applied migrations
- Backup database before running migrations in production

## 🧪 Development

### Project Development Guidelines

#### Code Structure

- **API Layer**: Keep route handlers thin, delegate to services
- **Service Layer**: Implement business logic, validation, and orchestration
- **Database Layer**: Define models and relationships
- **Separation of Concerns**: Each layer has a specific responsibility

#### Adding a New Feature

**Example: Adding a new "Order" entity**

1. **Create Model** (`app/database/models.py`)
```python
class Order(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # ... add fields
```

2. **Create Schema** (`app/api/schemas/order.py`)
```python
class OrderCreate(SQLModel):
    # ... fields for creation

class OrderRead(SQLModel):
    # ... fields for response
```

3. **Create Service** (`app/services/order.py`)
```python
class OrderService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)
    # ... add business logic
```

4. **Create Router** (`app/api/routers/order.py`)
```python
router = APIRouter(prefix="/order", tags=["order"])

@router.post("/")
async def create_order(...):
    # ... endpoint logic
```

5. **Register Router** (`app/api/router.py`)
```python
from .routers import order
master_router.include_router(order.router)
```

6. **Create Migration**
```bash
alembic revision --autogenerate -m "Add Order model"
alembic upgrade head
```

### Development Tools

```bash
# Install development dependencies
pip install pytest pytest-asyncio httpx black flake8 mypy

# Format code with Black
black app/

# Lint with flake8
flake8 app/

# Type checking with mypy
mypy app/

# Run tests
pytest tests/
```

### Environment Setup for Different Environments

**Development (.env.development)**
```env
POSTGRES_DB=fastship_dev
DEBUG=True
```

**Testing (.env.test)**
```env
POSTGRES_DB=fastship_test
TESTING=True
```

**Production (.env.production)**
```env
POSTGRES_DB=fastship_prod
DEBUG=False
```

## 🚀 Production Deployment

### Pre-Deployment Checklist

- [ ] Update `JWT_SECRET` to a strong, random value
- [ ] Configure proper email credentials
- [ ] Set up production PostgreSQL database
- [ ] Set up production Redis instance
- [ ] Configure environment variables
- [ ] Run database migrations
- [ ] Test all critical endpoints
- [ ] Set up logging and monitoring
- [ ] Configure CORS settings
- [ ] Enable HTTPS/SSL
- [ ] Set up backup strategy

### Deployment Options

#### Option 1: Docker Deployment

**Create `Dockerfile`:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_SERVER=db
      - REDIS_HOST=redis
    depends_on:
      - db
      - redis
    env_file:
      - .env

  db:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Deploy:**
```bash
docker-compose up -d
```

#### Option 2: Cloud Deployment (AWS/Azure/GCP)

**Using Gunicorn with Uvicorn Workers:**
```bash
pip install gunicorn

# Run with 4 worker processes
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

**Create `Procfile` for platforms like Heroku:**
```
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

#### Option 3: Systemd Service (Linux)

**Create `/etc/systemd/system/fastship.service`:**
```ini
[Unit]
Description=FastShip API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/fastship
Environment="PATH=/opt/fastship/venv/bin"
ExecStart=/opt/fastship/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable fastship
sudo systemctl start fastship
sudo systemctl status fastship
```

### Nginx Reverse Proxy

**Create `/etc/nginx/sites-available/fastship`:**
```nginx
server {
    listen 80;
    server_name api.fastship.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable and restart:**
```bash
sudo ln -s /etc/nginx/sites-available/fastship /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Performance Optimization

**Database Connection Pooling:**
```python
# In app/database/session.py
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Number of connections
    max_overflow=10,       # Extra connections if needed
    pool_pre_ping=True,    # Verify connections before use
)
```

**Enable Compression:**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**CORS Configuration:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Monitoring & Logging

**Add logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

**Health Check Endpoint:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

## 🧪 Testing

### Running Tests

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_shipment.py

# Run with verbose output
pytest -v
```

### Example Test

**`tests/test_shipment.py`:**
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_shipment():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/shipment/",
            json={
                "name": "Test Shipment",
                "description": "Test",
                "price": 100.0,
                "destination": 12345
            }
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Test Shipment"
```

## 📝 Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Development Team** - Initial work

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- SQLModel for type-safe database operations
- The Python community for amazing tools

## 📞 Support

For support, email support@fastship.com or open an issue in the repository.

## 🔗 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

---

**Built with ❤️ using FastAPI**

# Rollback to specific revision
alembic downgrade <revision_id>

# Upgrade to specific revision
alembic upgrade <revision_id>
```

## Development

### Project Features

- ✅ **Async FastAPI** - High-performance async endpoints
- ✅ **PostgreSQL** - Reliable relational database with async support
- ✅ **SQLModel** - Modern ORM with Pydantic integration
- ✅ **Redis** - Caching and session management
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Alembic Migrations** - Database version control
- ✅ **Pydantic Schemas** - Request/response validation
- ✅ **Service Layer** - Clean architecture pattern
- ✅ **API Documentation** - Auto-generated OpenAPI docs

### Development Workflow

1. **Activate virtual environment**
   ```bash
   venv\Scripts\activate  # Windows
   ```

2. **Make code changes** in the `app/` directory

3. **Run with auto-reload** for development
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Create migrations** after model changes
   ```bash
   alembic revision --autogenerate -m "Add new field"
   alembic upgrade head
   ```

5. **Test endpoints** using Swagger UI at http://localhost:8000/docs

### Adding New Dependencies

```bash
# Install the package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

## Troubleshooting

### Virtual Environment Issues

- **"venv not recognized":** Make sure Python is in your PATH
- **Can't activate venv:** Try `python -m venv venv --clear` to recreate

### Database Connection Issues

- **"Connection refused":** Check if PostgreSQL is running on the correct port
- **"Authentication failed":** Verify credentials in `.env` file
- **"Database doesn't exist":** Create the database using `CREATE DATABASE test;`

### Redis Issues

- **"Connection refused":** Ensure Redis server is running
- **Windows:** Use Redis for Windows or WSL2

### Import Errors

- **"Module not found":** Ensure virtual environment is activated
- **Missing dependencies:** Run `pip install -r requirements.txt`

### Migration Issues

- **"Target database is not up to date":** Run `alembic upgrade head`
- **"Can't locate revision":** Check alembic version table in database

## Common Commands Cheat Sheet

```bash
# Activate venv
venv\Scripts\activate              # Windows
source venv/bin/activate           # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload

# Database migrations
alembic upgrade head               # Apply migrations
alembic revision --autogenerate -m "message"  # Create migration

# Deactivate venv
deactivate
```

## License

This project is for educational/development purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review FastAPI documentation: https://fastapi.tiangolo.com
3. Check SQLModel documentation: https://sqlmodel.tiangolo.com
4. Review Alembic documentation: https://alembic.sqlalchemy.org

---

**Happy Coding! 🚀**
