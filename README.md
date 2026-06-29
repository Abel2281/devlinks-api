# DevLinks API 🔗

![DevLinks API Swagger UI](https://via.placeholder.com/800x400/0078D4/FFFFFF?text=DevLinks+API+Swagger+UI)

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-24.0%2B-2496ED.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%2B-336791.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.2%2B-DC382D.svg)](https://redis.io/)

A production-ready link management API built with Clean Architecture, dual-token JWT authentication, and background task processing.

## ✨ Core Features

- **Clean Architecture & Service Layer** - Separation of concerns with dedicated service classes for business logic
- **Dual-Token JWT Authentication** - Secure access/refresh token system with Redis-backed token invalidation
- **Background Task Analytics** - Asynchronous click tracking with FastAPI BackgroundTasks
- **Redis Caching with TTL** - Optimized performance with time-to-live cache management
- **Rate Limiting** - Protection against brute force attacks on authentication endpoints
- **Comprehensive API Testing** - Postman collection and detailed testing guide included
- **Dockerized Development** - Full stack with PostgreSQL, Redis, and FastAPI in containers

## 🛠️ Tech Stack

**Backend Framework**
- FastAPI with Uvicorn ASGI server
- Pydantic for data validation
- SQLAlchemy 2.0 (async) with Alembic migrations

**Database & Cache**
- PostgreSQL 16 for relational data
- Redis 7.2 for caching and token management

**Authentication & Security**
- JWT with PyJWT
- Password hashing with Passlib
- OWASP security headers

**Infrastructure**
- Docker & Docker Compose
- Python 3.11 type hints
- Pytest for testing

**API Documentation**
- Swagger UI at `/docs`
- ReDoc at `/redoc`
- OpenAPI 3.0 specification

## 🚀 Local Setup & Installation

### Prerequisites
- Docker 24.0+
- Docker Compose v2+
- 4GB RAM minimum (for PostgreSQL + Redis containers)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/devlinks-api.git
   cd devlinks-api
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration (or use defaults for development)

3. **Start the development stack**
   ```bash
   docker-compose up -d
   ```
   This will start:
   - FastAPI API server on `http://localhost:8000`
   - PostgreSQL database on `localhost:5432`
   - Redis cache on `localhost:6379`

4. **Initialize the database**
   ```bash
   # First time setup - generate initial migrations
   docker-compose exec api alembic revision --autogenerate -m "initial"

   # Apply migrations to database
   docker-compose exec api alembic upgrade head
   ```

5. **Access the API**
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### Development Workflow

- **Run tests**:
  ```bash
  docker-compose exec api pytest
  ```

- **Run migrations**:
  ```bash
  # Create new migration
  docker-compose exec api alembic revision --autogenerate -m "description"

  # Apply migrations
  docker-compose exec api alembic upgrade head
  ```

- **Rebuild containers**:
  ```bash
  docker-compose up -d --build
  ```

## 📖 API Reference

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/health` | GET | Health check endpoint | ❌ None |
| `/api/auth/register` | POST | Register new user | ❌ None |
| `/api/auth/login` | POST | Authenticate user | ❌ None |
| `/api/auth/refresh` | POST | Refresh access token | ❌ None |
| `/api/auth/logout` | POST | Invalidate refresh token | ❌ None |
| `/api/links` | GET | List all user links | ✅ Bearer Token |
| `/api/links` | POST | Create new link | ✅ Bearer Token |
| `/api/links/{link_id}` | PUT | Update existing link | ✅ Bearer Token |
| `/api/links/{link_id}` | DELETE | Delete link | ✅ Bearer Token |
| `/api/profile/{username}` | GET | Get public profile | ❌ None |
| `/api/analytics/click` | POST | Record link click | ❌ None |
| `/api/analytics` | GET | Get user analytics | ✅ Bearer Token |

### Postman Collection

The repository includes a comprehensive Postman collection:
- **File**: `DevLinks_API_Collection.postman_collection.json`
- **Features**: All endpoints with environment variables, sample requests, and response examples
- **Testing Guide**: `API_TESTING_GUIDE.md` with step-by-step testing procedures

## 🧪 Testing

### Running Tests

```bash
# Run all tests
docker-compose exec api pytest

# Run tests with coverage
docker-compose exec api pytest --cov=app --cov-report=term-missing

# Run specific test file
docker-compose exec api pytest tests/test_auth.py
```

### Test Coverage
- Unit tests for service layer
- Integration tests for API endpoints
- Authentication flow tests
- Rate limiting tests
- Database transaction tests

## 📁 Project Structure

```
devlinks-api/
├── app/                  # Main application
│   ├── core/             # Core configurations and utilities
│   ├── models/           # Database models
│   ├── routers/          # API route handlers
│   ├── schemas/          # Pydantic models
│   ├── services/         # Business logic layer
│   └── main.py           # FastAPI application
├── migrations/           # Alembic migration scripts
├── tests/                # Test suite
├── docker-compose.yml    # Docker configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── postman_collection.json  # Postman collection
└── API_TESTING_GUIDE.md  # Comprehensive testing guide
```

## 🔒 Security Features

- **JWT Token Security**: Dual-token system with short-lived access tokens and long-lived refresh tokens
- **Token Invalidation**: Redis-backed refresh token invalidation on logout
- **Password Security**: Bcrypt hashing with work factor 12
- **Rate Limiting**: 5 requests per minute for login endpoint
- **CORS**: Configurable CORS origins
- **Input Validation**: Pydantic model validation for all requests

## 📈 Performance Optimization

- **Redis Caching**: Frequently accessed data with TTL
- **Database Connection Pooling**: SQLAlchemy async connection pooling
- **Background Tasks**: Non-blocking analytics processing
- **Efficient Queries**: Optimized SQLAlchemy queries with proper indexing

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive docstrings
- Add tests for new features
- Update documentation as needed
- Keep dependencies updated

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
