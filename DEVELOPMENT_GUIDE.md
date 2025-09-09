# HRMS Development Setup Guide

## Prerequisites

Before running the HRMS application, ensure you have the following installed:

- **Docker**: Version 20.0 or higher
- **Docker Compose**: Version 2.0 or higher
- **Node.js**: Version 18 or higher (for local development)
- **Python**: Version 3.11 or higher (for local development)

## Quick Start with Docker

1. **Clone and navigate to the project directory:**
   ```bash
   cd /home/rajasekhar/Desktop/anil
   ```

2. **Start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - API Documentation: http://localhost:5000/docs
   - Database: PostgreSQL on localhost:5432

## Services Overview

### Database (PostgreSQL)
- **Port**: 5432
- **Database**: hrms_db
- **Username**: hrms_user
- **Password**: hrms_password
- **Features**: Comprehensive HR schema with 20+ tables

### Backend (Python/FastAPI)
- **Port**: 5000
- **Framework**: FastAPI with SQLAlchemy ORM
- **Authentication**: JWT-based authentication
- **API Documentation**: Swagger UI at `/docs`

### Frontend (React/TypeScript)
- **Port**: 3000
- **Framework**: React with TypeScript
- **UI**: TailwindCSS with Headless UI components
- **State Management**: React Query + Context API

## Database Schema

The database includes the following main entities:

### Core Entities:
- **Organizations**: Company/organization details
- **Departments**: Department structure and management
- **Positions**: Job positions and roles
- **Employees**: Complete employee profile management
- **Users**: Authentication and user accounts

### HR Modules:
- **Attendance**: Time tracking and attendance management
- **Leave Management**: Leave types, requests, and approvals
- **Payroll**: Salary processing and payroll management
- **Recruitment**: Job postings, applications, and hiring process
- **Performance**: Employee performance reviews and ratings
- **Training**: Training programs and employee development

### Supporting Tables:
- **Roles & Permissions**: Role-based access control
- **Announcements**: Company-wide announcements
- **Employee Documents**: Document management
- **Employee Benefits**: Benefits tracking

## Development Workflow

### Starting the Application
```bash
# Start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f [service_name]
```

### Stopping the Application
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (will delete database data)
docker-compose down -v
```

### Development Commands

#### Backend Development
```bash
# Enter backend container
docker exec -it hrms_backend bash

# Install new Python packages
docker exec -it hrms_backend pip install package_name

# Run database migrations (when implemented)
docker exec -it hrms_backend alembic upgrade head
```

#### Frontend Development
```bash
# Enter frontend container
docker exec -it hrms_frontend bash

# Install new npm packages
docker exec -it hrms_frontend npm install package_name

# Build for production
docker exec -it hrms_frontend npm run build
```

#### Database Operations
```bash
# Connect to PostgreSQL
docker exec -it hrms_postgres psql -U hrms_user -d hrms_db

# Backup database
docker exec hrms_postgres pg_dump -U hrms_user hrms_db > backup.sql

# Restore database
docker exec -i hrms_postgres psql -U hrms_user hrms_db < backup.sql
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout

### Employee Management
- `GET /api/employees` - List employees
- `POST /api/employees` - Create employee
- `GET /api/employees/{id}` - Get employee details
- `PUT /api/employees/{id}` - Update employee
- `DELETE /api/employees/{id}` - Delete employee

### Department Management
- `GET /api/departments` - List departments
- `POST /api/departments` - Create department
- `GET /api/departments/{id}` - Get department details
- `PUT /api/departments/{id}` - Update department
- `DELETE /api/departments/{id}` - Delete department

### Attendance Tracking
- `GET /api/attendance` - Get attendance records
- `POST /api/attendance/check-in` - Employee check-in
- `PUT /api/attendance/{id}/check-out` - Employee check-out

## Environment Configuration

### Backend Environment Variables (.env)
```
DATABASE_URL=postgresql://hrms_user:hrms_password@postgres:5432/hrms_db
JWT_SECRET=your_jwt_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=5000
ENVIRONMENT=development
```

### Frontend Environment Variables (.env)
```
REACT_APP_API_URL=http://localhost:5000
GENERATE_SOURCEMAP=false
```

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **Password Hashing**: bcrypt for password security
3. **Role-Based Access Control**: User roles and permissions
4. **Input Validation**: Pydantic models for data validation
5. **SQL Injection Prevention**: SQLAlchemy ORM protection

## Default User Accounts

After running the initial setup, you can create user accounts through the registration endpoint or directly in the database.

## Troubleshooting

### Common Issues:

1. **Port Conflicts**:
   - Ensure ports 3000, 5000, and 5432 are available
   - Modify docker-compose.yml to use different ports if needed

2. **Database Connection Issues**:
   - Check if PostgreSQL service is running
   - Verify database credentials in environment files

3. **Frontend Build Issues**:
   - Clear node_modules and reinstall dependencies
   - Check for TypeScript errors

4. **Backend Import Errors**:
   - Ensure all Python dependencies are installed
   - Check requirements.txt for missing packages

### Useful Commands:
```bash
# Check running containers
docker ps

# Check container logs
docker-compose logs [service_name]

# Rebuild specific service
docker-compose up --build [service_name]

# Remove all containers and start fresh
docker-compose down -v
docker-compose up --build
```

## Production Deployment

For production deployment:

1. Update environment variables with production values
2. Use production database credentials
3. Enable HTTPS/SSL
4. Set up reverse proxy (nginx)
5. Configure backup strategies
6. Set up monitoring and logging

## Features Roadmap

### Phase 1 (Current)
- ✅ Basic authentication
- ✅ Employee management
- ✅ Department management
- ✅ Basic attendance tracking

### Phase 2 (Next)
- 🔄 Complete attendance management
- 🔄 Leave management system
- 🔄 Payroll processing
- 🔄 Performance reviews

### Phase 3 (Future)
- 📋 Recruitment portal
- 📋 AI-powered candidate screening
- 📋 Training management
- 📋 Advanced reporting and analytics
- 📋 Mobile application
- 📋 Integration APIs

## Support

For technical support or questions:
1. Check the API documentation at http://localhost:5000/docs
2. Review the database schema in `/database/init.sql`
3. Check application logs using docker-compose logs

## Contributing

1. Follow the existing code structure
2. Add appropriate tests for new features
3. Update documentation for API changes
4. Use TypeScript for frontend development
5. Follow Python PEP 8 standards for backend development
