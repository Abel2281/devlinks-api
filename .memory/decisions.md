# DevLinks API - Architecture Decisions

## Decision 1: Dual Token JWT Strategy
- **Context:** Need secure authentication with ability to revoke sessions
- **Decision:** Use short-lived access tokens (15 min) + long-lived refresh tokens (7 days) stored hashed in DB
- **Rationale:** Access tokens are stateless (fast), refresh tokens enable session management and revocation
- **Trade-off:** Requires DB lookup for refresh token validation, but enables explicit logout

## Decision 2: Service Layer Pattern
- **Context:** Business logic should be separated from route handlers
- **Decision:** Use a service layer between routers and models
- **Rationale:** Keeps route handlers thin, enables easier testing of business logic
- **Trade-off:** More files, but cleaner separation of concerns

## Decision 3: Redis for Caching + Rate Limiting
- **Context:** Public profiles need fast access, sensitive routes need protection
- **Decision:** Use Redis for both profile caching (5-min TTL) and rate limiting
- **Rationale:** Single infrastructure dependency for two concerns; fast in-memory operations
- **Trade-off:** Additional infrastructure dependency; cache invalidation complexity

## Decision 4: UUID Primary Keys
- **Context:** Need non-sequential, unique identifiers
- **Decision:** Use UUID v4 for all primary keys
- **Rationale:** Prevents enumeration attacks, works well with distributed systems
- **Trade-off:** Slightly larger index size vs auto-increment integers

## Decision 5: Async Analytics Ingestion
- **Context:** Link clicks should be recorded without blocking the response
- **Decision:** Use FastAPI background tasks for click recording
- **Rationale:** Simple, no additional message broker needed for current scale
- **Trade-off:** Not durable if worker crashes; for production scale, consider a message queue

## Decision 6: Pydantic v2 Strict Validation
- **Context:** Need to prevent XSS and injection attacks via URL fields
- **Decision:** Use Pydantic v2 with strict mode, custom validators for URL sanitization
- **Rationale:** Blocks javascript: URLs, enforces alphanumeric usernames, validates URL format
- **Trade-off:** Slightly more verbose schema definitions