# DevLinks API - Architecture

## Directory Structure
```
devlinks-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy engine & session config
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings & env vars via pydantic-settings
│   │   ├── security.py      # JWT creation/verification, password hashing
│   │   └── redis.py         # Redis client setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLAlchemy model
│   │   ├── link.py          # Link SQLAlchemy model
│   │   └── click.py         # Click analytics model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic schemas for user
│   │   ├── link.py          # Pydantic schemas for link
│   │   ├── auth.py          # Pydantic schemas for auth
│   │   └── analytics.py     # Pydantic schemas for analytics
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # /auth endpoints
│   │   ├── links.py         # /links endpoints
│   │   ├── profile.py       # /profile/{username} endpoint
│   │   ├── analytics.py     # /analytics endpoints
│   │   └── deps.py          # FastAPI dependencies (get_current_user, etc.)
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py  # Auth business logic
│       ├── link_service.py  # Link business logic
│       ├── profile_service.py # Profile business logic
│       └── analytics_service.py # Analytics business logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures & test setup
│   ├── test_auth.py
│   ├── test_links.py
│   ├── test_profile.py
│   └── test_analytics.py
├── migrations/              # Alembic migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .env.example
└── .gitignore
```

## Data Flow

### Authentication Flow
1. User registers -> password hashed with bcrypt -> stored in DB
2. User logs in -> verify password -> issue access_token (15min) + refresh_token (7 days)
3. Refresh token stored hashed in DB
4. On refresh -> verify refresh token -> issue new pair, invalidate old refresh token
5. On logout -> delete refresh token from DB

### Profile Caching Flow
1. GET /profile/{username} -> check Redis cache
2. Cache hit -> return cached response
3. Cache miss -> query DB -> store in Redis with 5-min TTL -> return response
4. On profile/link update -> invalidate cache for that username

### Analytics Flow
1. Link click -> POST to /analytics/click with link_id
2. Capture IP, user-agent, referrer from request headers
3. Store click event in DB asynchronously
4. GET /analytics -> aggregate clicks by day for authenticated user

## Database Schema

### users
- id: UUID (PK)
- email: String (unique, indexed)
- username: String (unique, indexed, alphanumeric)
- display_name: String
- bio: Text (nullable)
- profile_image_url: String (nullable)
- hashed_password: String
- created_at: DateTime
- updated_at: DateTime

### links
- id: UUID (PK)
- user_id: UUID (FK -> users.id, indexed)
- title: String
- url: String (validated against javascript: injection)
- order: Integer (for sorting)
- is_active: Boolean (default True)
- created_at: DateTime
- updated_at: DateTime

### refresh_tokens
- id: UUID (PK)
- user_id: UUID (FK -> users.id, indexed)
- hashed_token: String
- expires_at: DateTime
- created_at: DateTime

### clicks
- id: UUID (PK)
- link_id: UUID (FK -> links.id, indexed)
- ip_address: String
- user_agent: String (nullable)
- referrer: String (nullable)
- clicked_at: DateTime

## API Endpoints

### Auth
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login, returns tokens
- POST /api/auth/refresh - Refresh access token
- POST /api/auth/logout - Invalidate refresh token

### Links
- GET /api/links - List user's links
- POST /api/links - Create link (max 10)
- PUT /api/links/{link_id} - Update link
- DELETE /api/links/{link_id} - Delete link

### Profile
- GET /api/profile/{username} - Get public profile (cached)

### Analytics
- POST /api/analytics/click - Record a click
- GET /api/analytics - Get click analytics for user