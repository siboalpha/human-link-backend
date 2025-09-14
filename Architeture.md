# HumanLink Platform – Technical Architecture Overview

## Overview
The HumanLink platform is a scalable, real-time social application connecting users with virtual friends for text, voice, or video chats.  
It supports key stages:
- **Discovery**: Ads and organic channels  
- **Onboarding**: Sign-up and personality matching  
- **Engagement**: Live chats and feedback  
- **Retention**: Re-matches and group events  

Roles include Normal Users, Friends, Managers, and Admins.

---

## Application Architecture Pattern

### Layer Structure
Our Django application follows a clean architecture pattern with clear separation of concerns:

```
API Layer (Views) → Service Layer → Repository Layer → Data Layer (Models)
```

### 1. **Repository Layer**
- **Purpose**: Handle all database operations and queries
- **Location**: `{app}/repositories/`
- **Responsibility**: 
  - Database queries and operations
  - Data validation at DB level
  - Return raw objects or querysets
- **Return Type**: `RepositoryResponse` with objects/querysets
- **Example Structure**:
  ```python
  # users/repositories/questionnaire_repository.py
  class QuestionnaireRepository:
      def create_questionnaire(self, profile, data) -> RepositoryResponse:
          # Database operations
          return RepositoryResponse(success=True, data=questionnaire_obj)
  ```

### 2. **Service Layer**  
- **Purpose**: Handle business logic and orchestration
- **Location**: `{app}/services/`
- **Types**:
  - **Operations**: CRUD operations (`questionnaire_operations.py`)
  - **Query**: Complex queries and filtering (`questionnaire_query.py`) 
  - **Utils**: App-specific utilities (`questionnaire_utils.py`)
- **Responsibility**:
  - Business logic validation
  - Data transformation and serialization
  - Orchestrating multiple repositories
  - Email sending, token generation, etc.
- **Return Type**: `ServiceResponse` with serialized data
- **Example Structure**:
  ```python
  # users/services/questionnaire_operations.py
  class QuestionnaireOperations:
      def __init__(self):
          self.repository = QuestionnaireRepository()
      
      def create_questionnaire(self, user, data) -> ServiceResponse:
          # Business logic
          # Call repository
          # Return serialized data
  ```

### 3. **API Layer (Views)**
- **Purpose**: Handle HTTP requests and responses
- **Location**: `{app}/views.py`
- **Responsibility**:
  - Request validation
  - Authentication/authorization
  - Call appropriate services
  - Return REST framework Response
- **Return Type**: `rest_framework.Response`
- **Example**:
  ```python
  @api_view(['POST'])
  @permission_classes([IsAuthenticated])
  def create_questionnaire_view(request):
      service = QuestionnaireOperations()
      response = service.create_questionnaire(request.user, request.data)
      return Response(response.data, status=response.status_code)
  ```

### 4. **Data Classes**
- **ServiceResponse**: Used by services to return serialized data
  ```python
  @dataclass
  class ServiceResponse:
      success: bool
      message: str
      data: Optional[dict] = field(default_factory=dict)
      status_code: int = 400
  ```

- **RepositoryResponse**: Used by repositories to return objects/queries
  ```python
  @dataclass
  class RepositoryResponse:
      success: bool
      message: str
      data: Any = None
      error: Optional[str] = None
  ```

### 5. **Testing Structure**
- **Location**: `{app}/tests/`
- **Structure**:
  - `repositories/` - Test repository layer
  - `services/` - Test service layer  
  - `endpoints/` - Test API endpoints
  - `factory.py` - Test data factories

---

## Technology Stack

- **Backend**: Python Django (REST API, user/friend management, matching logic)  
- **Real-Time Communication**: WebSockets via Django Channels for live text, voice, and video chats  
- **Frontend**: Next.js with TypeScript (responsive web app, landing page, dashboards)  
- **Mobile**: Flutter (cross-platform iOS/Android app for consistent UX)  
- **Database**: PostgreSQL (user profiles, session logs, ratings)  

### Additional Components
- **Authentication**: Django Allauth (email, Google SSO, X login)  
- **Payment Processing**: Stripe (subscriptions and premium sessions)  
- **Real-Time Infrastructure**: Twilio/Agora (voice and video integration)  
- **Hosting/Cloud**: AWS (EC2, ECS, S3 for media storage)  
- **Analytics**: Google Analytics (conversion tracking)  
- **Monitoring**: Sentry (error tracking)  
- **Queue**: Redis (WebSockets and background tasks)  

---

## Architectural Components

### 1. Client Layer  

#### Next.js Web App (TypeScript)
- Landing page: "Unlimited Connections" and "Start 7-Day Free Trial" CTA  
- User dashboard: Profile, match list, session scheduler, feedback form  
- Friend dashboard: Session calendar, user messages, payout tracking  
- Manager/Admin portals: Ticket management, performance analytics  

#### Flutter Mobile App
- Cross-platform iOS/Android with the same features as web (sign-up, chats, feedback)  
- Push notifications (Firebase): "New friend match!" or renewal reminders  

#### SEO
- Server-side rendering (Next.js) for organic discovery and link sharing  

---

### 2. API Layer (Django REST Framework)

**Endpoints:**
- `/auth`: Sign-up/login (email, Google, X via Allauth)  
- `/users`: Profile management (Normal User, Super User, Friend)  
- `/matches`: Personality-based matching (algorithm in Django)  
- `/sessions`: Schedule/book text/voice/video chats  
- `/feedback`: Submit ratings and surveys  
- `/payments`: Handle Stripe subscriptions and premium sessions  
- `/events`: Group event bookings  
- `/admin`: Manager/Admin tools for stats and ticket management  

**Security:**
- JWT tokens (django-rest-framework-simplejwt)  
- GDPR/CCPA compliance  

---

### 3. Real-Time Layer (Django Channels, WebSockets)
- Handles live text chats (Django Channels with Redis)  
- Integrates Twilio/Agora for voice and video calls  
- Scales horizontally with user growth  

---

### 4. Database Layer (PostgreSQL)

**Schemas:**
- **Users**: ID, email, personality form (JSON), role (Normal, Friend, Super User)  
- **Matches**: User-Friend pairs, match score, session history  
- **Sessions**: Timestamp, type (text/voice/video), duration, rating  
- **Payments**: Stripe subscription ID, status, amount  
- **Feedback**: Ratings (1-5), comments  
- **Events**: Group event details, bookings  

**Performance:**
- Indexes on user/match IDs  
- Sharding for scale as needed  

---

### 5. Infrastructure Layer (AWS)
- **EC2**: Hosts Django app  
- **ECS**: Autoscaling WebSocket servers (Django Channels)  
- **S3**: Stores user media (profile pictures, session recordings)  
- **RDS**: Managed PostgreSQL database  
- **Elastic Load Balancer**: Distributes traffic  

---

### 6. Additional Services
- **Stripe**: Processes subscriptions and premium sessions  
- **Google Analytics**: Tracks landing page conversions and ad clicks  
- **Sentry**: Monitors and logs errors (e.g., chat failures)  
- **Redis**: Queues WebSocket messages and background tasks (e.g., match calculations)  
- **Firebase**: Push notifications and analytics for the Flutter app  

---
