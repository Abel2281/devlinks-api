# DevLinks API - Project Overview

## Description
A developer-focused link-in-bio REST API (similar to Linktree) that allows developers to create profiles, aggregate social links (GitHub, LinkedIn, portfolios), track link-click analytics, and serve public profiles instantly using aggressive caching.

## Tech Stack
- **Framework:** FastAPI (Python 3.11+) with async routing and Depends() injection
- **Database:** PostgreSQL with SQLAlchemy 2.0 (Declarative Mapping) + Alembic migrations
- **Security:** JWT dual-token strategy (Access + Refresh tokens), passlib[bcrypt] for password hashing
- **Caching:** Redis for public profile caching (5-min TTL) and rate-limiting
- **Validation:** Pydantic v2 for strict input sanitization
- **Testing:** pytest + httpx (async client)
- **Deployment:** Docker + Docker Compose

## Core Features
1. **/auth** - Registration, login, token refresh, logout
2. **/links** - Authenticated CRUD for user links (max 10 per user)
3. **/profile/{username}** - Public cached endpoint with user details + active links
4. **/analytics** - Link click tracking with IP, timestamp, referrer metadata

## Project Status
- Initial scaffolding in progress