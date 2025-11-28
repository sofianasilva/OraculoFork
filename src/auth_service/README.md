# Oráculo Authentication Service

## Step 1: Django Authentication Foundation ✅

This is the minimal Django authentication service for Oráculo, implementing:

### 🏗️ Architecture
- **Django 4.2.7** with Django REST Framework
- **JWT Authentication** using SimpleJWT
- **Shared PostgreSQL** database with main Oráculo project
- **Docker integration** with automatic startup

### 🔐 Features Implemented
- User registration with email validation
- JWT-based login/logout
- User profile management
- Django Admin interface
- CORS configuration for FastAPI integration

### 📡 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | User registration | No |
| POST | `/api/auth/login/` | User login | No |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PUT | `/api/auth/profile/update/` | Update profile | Yes |
| POST | `/api/auth/token/refresh/` | Refresh JWT token | No |

### 🚀 Quick Start

1. **Start services:**
   ```bash
   docker-compose up -d
   ```

2. **Test authentication:**
   ```bash
   python scripts/test-auth.py
   ```

3. **Access Django Admin:**
   - URL: http://localhost:8001/admin/
   - Credentials: `admin` / `admin123`

### 🔧 Configuration

Environment variables in `.env`:
```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
DB_HOST=db
DB_NAME=databasex
DB_USER=postgres
DB_PASSWORD=postgres
```

### 📊 Database Schema

The authentication service creates these tables:
- `auth_user` - Custom user model
- `auth_user_groups` - User groups (Django default)
- `auth_user_user_permissions` - User permissions (Django default)
- Standard Django auth tables

### 🔄 Next Steps

- **Step 2**: Add authentication endpoints validation
- **Step 3**: Complete Docker integration testing  
- **Step 4**: Integrate with FastAPI (JWT middleware)
- **Step 5**: Implement Access Control Lists (ACL)
- **Step 6**: Set up Django Admin interface
- **Step 7**: Prepare for web interface

### 🧪 Testing

Run the test script to validate all endpoints:
```bash
python scripts/test-auth.py
```

Expected output:
```
🚀 Starting Oráculo Authentication Service Tests
🧪 Testing user registration...
✅ Registration successful!
🧪 Testing authenticated profile access...
✅ Profile access successful!
✅ All tests completed successfully!
```