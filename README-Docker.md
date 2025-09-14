# Human Link Backend - Docker Setup

This Django application is containerized with PostgreSQL using Docker and docker-compose.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd human-link-backend
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - PostgreSQL: localhost:5432

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://humanlink:humanlink123@db:5432/humanlink` |
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1,0.0.0.0` |
| `FRONTEND_URL` | Frontend application URL | `http://localhost:3000` |

## Docker Commands

### Development
```bash
# Start services
docker-compose up

# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Database Management
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Open Django shell
docker-compose exec web python manage.py shell

# Access PostgreSQL
docker-compose exec db psql -U humanlink -d humanlink
```

### Production Deployment
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up --build -d
```

## Database

The application uses PostgreSQL 15 with the following default credentials:
- Database: `humanlink`
- Username: `humanlink`
- Password: `humanlink123`

Data is persisted in a Docker volume named `postgres_data`.

## Architecture

- **Web Service**: Django application running on port 8000
- **Database Service**: PostgreSQL 15 running on port 5432
- **Volumes**: PostgreSQL data persistence
- **Networks**: Default Docker network for service communication

## Troubleshooting

### Database Connection Issues
```bash
# Check if database is ready
docker-compose exec web python manage.py wait_for_db

# Reset database
docker-compose down -v
docker-compose up --build
```

### View Service Status
```bash
docker-compose ps
```

### Access Container Shell
```bash
# Django container
docker-compose exec web bash

# PostgreSQL container
docker-compose exec db bash
```