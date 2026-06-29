# DevLinks API Testing Guide

This guide provides comprehensive instructions for testing all API endpoints in the DevLinks project using the Postman collection.

## API Endpoints Overview

The DevLinks API consists of 4 main route groups:

### 1. Health Check
- `GET /health` - Check API health status

### 2. Authentication Routes (`/api/auth`)
- `POST /register` - Register a new user
- `POST /login` - Authenticate and get access token
- `POST /refresh` - Refresh access token using refresh token
- `POST /logout` - Invalidate refresh token

### 3. Links Routes (`/api/links`) - Requires Authentication
- `GET /` - List all links for authenticated user
- `POST /` - Create a new link
- `PUT /{link_id}` - Update an existing link
- `DELETE /{link_id}` - Delete a link

### 4. Profile Routes (`/api/profile`)
- `GET /{username}` - Get public profile information

### 5. Analytics Routes (`/api/analytics`)
- `POST /click` - Record a link click (public)
- `GET /` - Get analytics for authenticated user's links

## Testing Procedure

### Step 1: Set Up Postman Environment
1. Import the `DevLinks_API_Collection.postman_collection.json` file into Postman
2. Set the `base_url` variable to `http://localhost:8000` (or your server URL)
3. Start the DevLinks API server using `docker-compose up`

### Step 2: Test Health Check
- **Endpoint**: `GET /health`
- **Expected Response**: `{"status": "healthy", "service": "DevLinks API"}`
- **Status Code**: 200 OK

### Step 3: Test Authentication Flow

#### 3.1 Register User
- **Endpoint**: `POST /api/auth/register`
- **Request Body**:
  ```json
  {
    "email": "test@example.com",
    "password": "securepassword123",
    "username": "testuser"
  }
  ```
- **Expected Response**: User registration details with status 201 Created
- **Test Cases**:
  - ✅ Valid registration
  - ❌ Duplicate email (should return 409 Conflict)
  - ❌ Invalid email format (should return 422 Validation Error)

#### 3.2 Login User
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "test@example.com",
    "password": "securepassword123"
  }
  ```
- **Expected Response**: Access token and refresh token with status 200 OK
- **Post-Test Action**: Copy the access token to the `access_token` variable
- **Test Cases**:
  - ✅ Valid credentials
  - ❌ Invalid password (should return 401 Unauthorized)
  - ❌ Non-existent user (should return 401 Unauthorized)

#### 3.3 Test Token Refresh
- **Endpoint**: `POST /api/auth/refresh`
- **Request Body**:
  ```json
  {
    "refresh_token": "your-refresh-token-from-login"
  }
  ```
- **Expected Response**: New access token with status 200 OK
- **Test Cases**:
  - ✅ Valid refresh token
  - ❌ Invalid/expired refresh token (should return 401 Unauthorized)

### Step 4: Test Links Routes (Requires Authentication)

#### 4.1 Create Link
- **Endpoint**: `POST /api/links`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Request Body**:
  ```json
  {
    "title": "Test Link",
    "url": "https://example.com/test",
    "description": "This is a test link",
    "is_active": true
  }
  ```
- **Expected Response**: Created link details with status 201 Created
- **Post-Test Action**: Copy the link ID to the `link_id` variable

#### 4.2 List Links
- **Endpoint**: `GET /api/links`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Expected Response**: Array of links with status 200 OK

#### 4.3 Update Link
- **Endpoint**: `PUT /api/links/{{link_id}}`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Request Body**:
  ```json
  {
    "title": "Updated Test Link",
    "url": "https://example.com/updated",
    "description": "This link has been updated"
  }
  ```
- **Expected Response**: Updated link details with status 200 OK

#### 4.4 Delete Link
- **Endpoint**: `DELETE /api/links/{{link_id}}`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Expected Response**: Status 204 No Content
- **Test Cases**:
  - ✅ Delete existing link
  - ❌ Delete non-existent link (should return 404 Not Found)

### Step 5: Test Profile Route

#### 5.1 Get Profile
- **Endpoint**: `GET /api/profile/{{username}}`
- **Expected Response**: Profile information with status 200 OK
- **Test Cases**:
  - ✅ Existing username
  - ❌ Non-existent username (should return 404 Not Found)

### Step 6: Test Analytics Routes

#### 6.1 Record Click (Public)
- **Endpoint**: `POST /api/analytics/click`
- **Request Body**:
  ```json
  {
    "link_id": "valid-link-id-here"
  }
  ```
- **Expected Response**: Status 204 No Content

#### 6.2 Get Analytics (Authenticated)
- **Endpoint**: `GET /api/analytics`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Expected Response**: Analytics data with status 200 OK

### Step 7: Test Logout
- **Endpoint**: `POST /api/auth/logout`
- **Request Body**:
  ```json
  {
    "refresh_token": "your-refresh-token-from-login"
  }
  ```
- **Expected Response**: Status 204 No Content

## Error Handling Tests

Test these error scenarios for comprehensive coverage:

1. **Authentication Errors**:
   - Missing/Invalid Authorization header (401 Unauthorized)
   - Expired access token (401 Unauthorized)

2. **Validation Errors**:
   - Invalid email format (422 Validation Error)
   - Missing required fields (422 Validation Error)
   - Invalid URL format (422 Validation Error)

3. **Authorization Errors**:
   - Accessing other users' resources (403 Forbidden)
   - Modifying/deleting links you don't own (404 Not Found)

4. **Rate Limiting**:
   - Too many login attempts (429 Too Many Requests)

## Test Data Management

For thorough testing, create multiple test users and links:

```json
{
  "users": [
    {
      "email": "user1@test.com",
      "password": "password123",
      "username": "user1"
    },
    {
      "email": "user2@test.com",
      "password": "password123",
      "username": "user2"
    }
  ],
  "links": [
    {
      "title": "Google",
      "url": "https://google.com",
      "description": "Search engine"
    },
    {
      "title": "GitHub",
      "url": "https://github.com",
      "description": "Code hosting platform",
      "is_active": false
    }
  ]
}
```

## API Testing Checklist

- [ ] Health check endpoint
- [ ] User registration (success + validation errors)
- [ ] User login (success + authentication errors)
- [ ] Token refresh (success + invalid token)
- [ ] Link creation (success + validation errors)
- [ ] Link listing (empty + with data)
- [ ] Link update (success + not found)
- [ ] Link deletion (success + not found)
- [ ] Profile retrieval (success + not found)
- [ ] Click recording (success + invalid link)
- [ ] Analytics retrieval (empty + with data)
- [ ] User logout
- [ ] Authentication header validation
- [ ] Rate limiting tests

## Postman Collection Features

The provided Postman collection includes:

1. **Environment Variables**:
   - `base_url`: API base URL
   - `access_token`: JWT access token (auto-updated after login)
   - `link_id`: Current link ID for testing
   - `username`: Test username

2. **Organized Folders**:
   - Health Check
   - Auth Routes
   - Links Routes
   - Profile Routes
   - Analytics Routes

3. **Pre-configured Requests**:
   - Proper headers (Content-Type, Authorization)
   - Sample request bodies
   - Variable substitution

4. **Test Sequences**:
   - Authentication flow (register → login → test protected routes)
   - CRUD operations (create → read → update → delete)
   - Analytics tracking (record clicks → view analytics)

To use this collection effectively, run tests in the following order:
1. Health Check
2. Auth Routes (register, login)
3. Links Routes (CRUD operations)
4. Profile Routes
5. Analytics Routes
6. Auth Routes (logout)