# PCC-PASS - Phil Cancer Center Personnel and Supplies System

A comprehensive system for managing personnel records, HR files, IT equipment, and furniture assignments.

## Features

### Authentication
- ✅ User Registration (with admin approval)
- ✅ Admin Registration (with secret key)
- ✅ JWT-based authentication
- ✅ Role-based access control (Admin/User)

### For Users
- View personal information
- Access assigned HR files
- View assigned IT equipment
- View assigned furniture
- Download documents

### For Admins
- Approve/Reject user registrations
- Manage all employees
- Upload and assign HR files
- Manage IT equipment with PAR documents
- Manage furniture with PAR documents
- Complete CRUD operations on all resources

## Tech Stack

### Backend
- FastAPI (Python web framework)
- MongoDB (Database)
- Beanie (MongoDB ODM)
- JWT (Authentication)
- Motor (Async MongoDB driver)

### Frontend
- Angular 17
- TypeScript
- Tailwind CSS
- RxJS

## Installation

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize database:
```bash
python scripts/init_db.py
```

5. Create admin user:
```bash
python scripts/create_admin.py
```

6. Start server:
```bash
chmod +x start.sh
./start.sh
# Or: uvicorn app.main:app --reload
```

Server will run on: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Update environment:
```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

3. Start development server:
```bash
ng serve
```

Application will run on: http://localhost:4200

## Usage

### First Time Setup

1. Start MongoDB
2. Initialize backend database
3. Create first admin user via script
4. Start backend server
5. Start frontend application

### Admin Registration

Admin registration requires an admin key. Access the hidden admin registration page:
- URL: http://localhost:4200/admin/register
- Provide email, password, and the ADMIN_SECRET_KEY from .env

### User Registration

Users can register via the public registration form:
1. Fill out all required fields
2. Submit registration
3. Wait for admin approval
4. Login after approval

### Admin Approval Workflow

1. Admin logs in
2. Navigate to dashboard
3. View pending registrations
4. Review user information
5. Approve or reject users

## API Endpoints

### Authentication
- POST /api/auth/register - User registration
- POST /api/auth/register-admin - Admin registration
- POST /api/auth/login - Login
- GET /api/auth/pending-users - Get pending users (Admin)
- POST /api/auth/approve-user/{id} - Approve user (Admin)
- DELETE /api/auth/reject-user/{id} - Reject user (Admin)

## Environment Variables

### Backend (.env)
- MONGODB_URL - MongoDB connection string
- MONGODB_DB_NAME - Database name
- SECRET_KEY - JWT secret key
- ADMIN_SECRET_KEY - Admin registration key
- ACCESS_TOKEN_EXPIRE_MINUTES - Token expiration
- FRONTEND_URL - Frontend URL for CORS

## Project Structure

```
pcc-pass/
├── backend/
│   ├── app/
│   │   ├── models/         # Beanie document models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   └── main.py         # FastAPI application
│   ├── scripts/            # Database scripts
│   └── requirements.txt
└── frontend/
    └── src/
        └── app/
            ├── auth/       # Authentication components
            ├── core/       # Services, guards, models
            └── dashboard/  # Dashboard components
```

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- Admin approval required for new users
- Secure admin registration with secret key
- HTTP-only cookie support (optional)

## License

MIT License