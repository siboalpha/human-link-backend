# HumanLink Platform – API Documentation

This document describes the architecture and design of the API layer for the HumanLink platform.  
It details endpoints, request/response formats, authentication, permissions, and best practices for building a scalable and secure REST API.

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication & Security](#authentication--security)
3. [API Versioning](#api-versioning)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Pagination & Filtering](#pagination--filtering)
7. [API Endpoints](#api-endpoints)
8. [Background Tasks & WebSockets](#background-tasks--websockets)
9. [Testing & Documentation](#testing--documentation)

---

## Overview

The API Layer is built using **Django REST Framework (DRF)**.  
It exposes all business logic to web and mobile clients through secure endpoints.  

### Key Principles
- RESTful structure
- JWT-based authentication
- Role-based access control
- Pagination and filtering
- Versioning for forward compatibility
- Consistent response format
- Comprehensive error handling

### Base URL
```
https://api.humanlink.com/api/v1/
```

---

## Authentication & Security

### Authentication Method
- **JWT Authentication**: Using `django-rest-framework-simplejwt`
- **Token Types**:
  - Access Token: Short-lived (15 minutes)
  - Refresh Token: Long-lived (7 days)

### User Roles
- **Normal User**: Regular app user with basic permissions
- **Friend**: Virtual friend offering sessions with extended permissions
- **Manager**: Staff with elevated permissions for user management
- **Admin**: Full system access and administrative privileges

### Security Features
- **CORS**: Configured for web and mobile frontends
- **Rate Limiting**: Applied to prevent abuse
- **Data Protection**: GDPR/CCPA-compliant data handling
- **HTTPS Only**: All communications encrypted

### Headers Required
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## API Versioning

All endpoints are prefixed with a version to ensure backward compatibility:

```
/api/v1/
```

Future versions will increment (`/api/v2/`, etc.) without breaking older clients.

---

## Response Format

### Success Response
All successful responses follow this JSON structure:

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Optional success message",
  "pagination": {
    "count": 100,
    "next": "http://api.example.org/accounts/?page=4",
    "previous": "http://api.example.org/accounts/?page=2",
    "results": []
  }
}
```

### Error Response
```json
{
  "success": false,
  "errors": {
    "field_name": ["Error message here"],
    "non_field_errors": ["General error message"]
  },
  "message": "Operation failed"
}
```

---

## Error Handling

### HTTP Status Codes
| Code | Description |
|------|-------------|
| 200  | OK - Request successful |
| 201  | Created - Resource created successfully |
| 400  | Bad Request - Invalid request data |
| 401  | Unauthorized - Authentication required |
| 403  | Forbidden - Permission denied |
| 404  | Not Found - Resource not found |
| 429  | Too Many Requests - Rate limit exceeded |
| 500  | Internal Server Error - Server error |

---

## Pagination & Filtering

### Pagination
- **Type**: PageNumberPagination
- **Page Size**: 20 items per page (configurable)
- **Query Parameters**:
  - `page`: Page number
  - `page_size`: Items per page (max 100)

### Filtering
Using `django-filter` for query parameters:

```
/api/v1/sessions/?type=video&status=upcoming&date_after=2023-01-01
```

Common filter parameters:
- `search`: Text search across relevant fields
- `ordering`: Sort by field (prefix with `-` for descending)
- `date_after`, `date_before`: Date range filtering

---

## API Endpoints

### 1. Authentication

#### Register User
```http
POST /api/v1/auth/register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "personality_data": {
    "interests": ["technology", "sports"],
    "communication_style": "friendly"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "message": "User registered successfully"
}
```

#### Login
```http
POST /api/v1/auth/login/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Logout
```http
POST /api/v1/auth/logout/
```
*Requires Authentication*

---

### 2. Users

#### Get Current User Profile
```http
GET /api/v1/users/me/
```
*Requires Authentication*

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "created_at": "2023-01-01T00:00:00Z",
    "subscription_status": "active"
  }
}
```

#### Update Current User Profile
```http
PATCH /api/v1/users/me/
```
*Requires Authentication*

**Request Body:**
```json
{
  "first_name": "John",
  "personality_data": {
    "interests": ["technology", "music"]
  }
}
```

#### Get User by ID
```http
GET /api/v1/users/{id}/
```
*Requires Authentication (Limited to public info)*

#### List All Users
```http
GET /api/v1/users/
```
*Requires Admin Authentication*

---

### 3. Matches

#### List User's Matches
```http
GET /api/v1/matches/
```
*Requires Authentication*

**Query Parameters:**
- `status`: `pending`, `accepted`, `declined`
- `compatibility_score_min`: Minimum compatibility score

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "friend": {
          "id": 2,
          "name": "Sarah",
          "avatar": "https://example.com/avatar.jpg"
        },
        "compatibility_score": 85,
        "status": "pending",
        "created_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
}
```

#### Create Match
```http
POST /api/v1/matches/
```
*Requires Manager/Admin Authentication*

#### Get Specific Match
```http
GET /api/v1/matches/{id}/
```
*Requires Authentication*

#### Remove Match
```http
DELETE /api/v1/matches/{id}/
```
*Requires Manager/Admin Authentication*

---

### 4. Sessions

#### List Sessions
```http
GET /api/v1/sessions/
```
*Requires Authentication*

**Query Parameters:**
- `type`: `text`, `voice`, `video`
- `status`: `upcoming`, `completed`, `cancelled`
- `date_after`: Filter sessions after date
- `date_before`: Filter sessions before date

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "friend": {
          "id": 2,
          "name": "Sarah"
        },
        "type": "video",
        "status": "upcoming",
        "scheduled_at": "2023-01-15T14:00:00Z",
        "duration_minutes": 60,
        "price": "29.99"
      }
    ]
  }
}
```

#### Book New Session
```http
POST /api/v1/sessions/
```
*Requires Authentication*

**Request Body:**
```json
{
  "friend_id": 2,
  "type": "video",
  "scheduled_at": "2023-01-15T14:00:00Z",
  "duration_minutes": 60,
  "notes": "Looking forward to our chat!"
}
```

#### Get Session Details
```http
GET /api/v1/sessions/{id}/
```
*Requires Authentication*

#### Update Session
```http
PATCH /api/v1/sessions/{id}/
```
*Requires Authentication*

**Request Body:**
```json
{
  "scheduled_at": "2023-01-15T15:00:00Z",
  "notes": "Rescheduled for later"
}
```

#### Cancel Session
```http
DELETE /api/v1/sessions/{id}/
```
*Requires Authentication*

---

### 5. Feedback

#### Submit Feedback
```http
POST /api/v1/feedback/
```
*Requires Authentication*

**Request Body:**
```json
{
  "session_id": 1,
  "rating": 5,
  "comment": "Excellent session, very helpful!",
  "categories": ["helpful", "professional", "engaging"]
}
```

#### View Feedback
```http
GET /api/v1/feedback/
```
*Requires Friend/Admin Authentication*

**Query Parameters:**
- `session_id`: Filter by session
- `rating_min`: Minimum rating
- `date_after`: Filter after date

---

### 6. Payments

#### Subscribe to Plan
```http
POST /api/v1/payments/subscribe/
```
*Requires Authentication*

**Request Body:**
```json
{
  "plan_id": "premium_monthly",
  "payment_method_id": "pm_1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "subscription": {
      "id": "sub_1234567890",
      "status": "active",
      "current_period_end": "2023-02-01T00:00:00Z"
    },
    "client_secret": "pi_1234567890_secret_abc"
  }
}
```

#### Get Subscription Status
```http
GET /api/v1/payments/status/
```
*Requires Authentication*

---

### 7. Events

#### List Group Events
```http
GET /api/v1/events/
```
*Requires Authentication*

**Query Parameters:**
- `category`: Event category
- `date_after`: Events after date
- `location`: Filter by location

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "title": "Virtual Coffee Chat",
        "description": "Join us for a friendly group discussion",
        "date": "2023-01-20T18:00:00Z",
        "capacity": 10,
        "registered_count": 7,
        "price": "5.00"
      }
    ]
  }
}
```

#### Book Event Ticket
```http
POST /api/v1/events/book/
```
*Requires Authentication*

**Request Body:**
```json
{
  "event_id": 1,
  "payment_method_id": "pm_1234567890"
}
```

---

### 8. Admin Tools

#### Admin User Management
```http
GET /api/v1/admin/users/
```
*Requires Admin Authentication*

**Query Parameters:**
- `role`: Filter by user role
- `status`: Filter by account status
- `search`: Search by name or email

#### Admin Friend Management
```http
GET /api/v1/admin/friends/
```
*Requires Admin Authentication*

#### Support Tickets Dashboard
```http
GET /api/v1/admin/tickets/
```
*Requires Admin/Manager Authentication*

---

## Background Tasks & WebSockets

### Background Tasks
- **Redis Queues**: Used for background tasks such as:
  - Match scoring calculations
  - Email notifications
  - Payment processing
  - Data analytics

### Real-time Features
- **Django Channels**: WebSocket support for:
  - Session reminders
  - Live chat during sessions
  - Real-time notifications
  - Status updates

### WebSocket Endpoints
```
ws://api.humanlink.com/ws/notifications/{user_id}/
ws://api.humanlink.com/ws/sessions/{session_id}/chat/
```

---

## Testing & Documentation

### Automated Testing
- **Framework**: pytest with DRF test client
- **Coverage**: Minimum 90% code coverage
- **Types**:
  - Unit tests for models and utilities
  - Integration tests for API endpoints
  - Performance tests for critical paths

### API Documentation
- **Auto-generation**: Using `drf-spectacular` for OpenAPI 3.0
- **Interactive Docs**: Swagger UI available at `/api/docs/`
- **Redoc**: Alternative documentation at `/api/redoc/`

### Rate Limiting
```python
# Default rate limits
ANONYMOUS: 100/hour
AUTHENTICATED: 1000/hour
PREMIUM: 5000/hour
```

---

## Development Guidelines

### Code Style
- Follow PEP 8 standards
- Use black for code formatting
- Type hints required for all functions

### Security Best Practices
- Input validation on all endpoints
- SQL injection prevention
- XSS protection
- CSRF tokens for state-changing operations
- Regular security audits

### Performance Optimization
- Database query optimization
- Caching with Redis
- CDN for static assets
- Compression for API responses
