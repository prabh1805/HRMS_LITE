# HRMSLite - Employee & Attendance Management System

A modern, full-stack HR Management System for managing employees and tracking attendance with an intuitive dashboard and analytics.

## 🎯 Project Overview

HRMSLite is a lightweight HRMS application designed for small to medium-sized organizations to efficiently manage employee records and track daily attendance. The system provides:

- **Employee Management**: Add, edit, delete, and view employee records with auto-generated employee IDs
- **Attendance Tracking**: Mark daily attendance (Present/Absent) with date filtering capabilities
- **Dashboard Analytics**: Real-time statistics showing attendance rates, employee counts, and individual attendance summaries
- **Responsive UI**: Modern gradient-based design that works seamlessly across devices
- **Data Pagination**: Efficient handling of large datasets with paginated tables

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.13)
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Server**: Uvicorn (ASGI)

### Frontend
- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Development Tools
- Python virtual environment (.venv)
- Node.js & npm
- Git for version control

## 📋 Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.13+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** and npm ([Download](https://nodejs.org/))
- **PostgreSQL 14+** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/downloads))

## 🚀 Steps to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/prabh1805/HRMS_LITE.git
cd HRMS_LITE
```

### 2. Database Setup

Create a PostgreSQL database:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE hrms_lite;

# Exit psql
\q
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your database credentials
# DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/hrms_lite

# Run database migrations
alembic upgrade head

# (Optional) Seed database with 100 employees and attendance data
python seed_data.py

# Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### 4. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file (optional - defaults to localhost:8000)
cp .env.example .env

# Start the development server
npm run dev
```

Frontend will be running at: `http://localhost:5173`

### 5. Access the Application

Open your browser and navigate to `http://localhost:5173`

**Default Pages:**
- Dashboard: `/`
- Employees: `/employees`
- Attendance: `/attendance`

## 📁 Project Structure

```
HRMS_LITE/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── repositories/     # Database operations
│   │   ├── exceptions/       # Custom exceptions
│   │   └── middleware/       # Middleware (logging, etc.)
│   ├── .env.example          # Environment variables template
│   ├── requirements.txt      # Python dependencies
│   └── seed_data.py          # Database seeding script
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ui/          # Reusable UI components
│   │   │   ├── employee/    # Employee-specific components
│   │   │   └── attendance/  # Attendance-specific components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   ├── hooks/           # Custom React hooks
│   │   └── utils/           # Utility functions
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
│
└── README.md                # This file
```

## 🎨 Features

### Employee Management
- Auto-generated employee IDs (EMP-0001, EMP-0002, etc.)
- Full CRUD operations (Create, Read, Update, Delete)
- Fields: Employee ID, Full Name, Email, Department
- Paginated table view (10 employees per page)
- Search and filter capabilities

### Attendance Management
- Mark attendance for any employee on any date
- Status options: Present / Absent
- Edit or delete attendance records
- Date range filtering
- Paginated table view (15 records per page)
- Prevents duplicate attendance for same employee on same date

### Dashboard
- Total employee count
- Today's present/absent counts
- Attendance rate visualization (circular progress chart)
- Employee attendance summary table with:
  - Total present days
  - Total absent days
  - Individual attendance percentage
  - Color-coded performance indicators
- Paginated summary (10 employees per page)

### UI/UX Features
- Modern gradient-based design
- Responsive layout for all screen sizes
- Loading states with spinners
- Toast notifications for all actions
- Empty states with helpful messages
- Error handling with retry options
- Smooth transitions and animations

## ⚙️ Configuration

### Backend Configuration (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/hrms_lite

# Application
DEBUG=true
APP_NAME=HRMSLite
VERSION=0.1.0

# CORS (for frontend)
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

### Frontend Configuration (.env)

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 🧪 API Endpoints

### Employees
- `GET /api/v1/employees` - Get all employees
- `POST /api/v1/employees` - Create employee
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Attendance
- `GET /api/v1/attendance` - Get all attendance (with optional date filters)
- `POST /api/v1/attendance` - Mark attendance
- `PUT /api/v1/attendance/{id}` - Update attendance
- `DELETE /api/v1/attendance/{id}` - Delete attendance
- `GET /api/v1/attendance/summary/by-employee` - Get attendance summary

### Dashboard
- `GET /api/v1/dashboard/stats` - Get dashboard statistics

### Health Check
- `GET /api/v1/health` - API health status

Full API documentation available at: `http://localhost:8000/docs`

## 🔒 Assumptions & Limitations

### Assumptions
1. **Single Admin User**: No authentication/authorization implemented - assumes single admin user
2. **Working Days**: Attendance can be marked for any day (including weekends)
3. **Timezone**: All dates use server timezone (no timezone conversion)
4. **Email Uniqueness**: Employee emails must be unique
5. **Employee ID Format**: Auto-generated in format EMP-XXXX (4 digits)

### Limitations
1. **No Authentication**: No login/logout functionality
2. **No Role-Based Access**: All users have full access
3. **No Leave Management**: Only Present/Absent status (no leave types)
4. **No Payroll**: Payroll calculations not included
5. **No File Uploads**: No support for employee documents/photos
6. **No Bulk Operations**: No bulk import/export of data
7. **No Email Notifications**: No automated email alerts
8. **No Audit Trail**: No tracking of who made changes
9. **No Reports**: No PDF/Excel report generation
10. **Client-Side Pagination**: Pagination done in frontend (not ideal for very large datasets)

### Future Enhancements
- User authentication and authorization
- Leave management system
- Shift management
- Department hierarchy
- Employee performance tracking
- Report generation (PDF/Excel)
- Email notifications
- Bulk data import/export
- Advanced analytics and charts
- Mobile app

## 🐛 Troubleshooting

### Backend Issues

**Database connection error:**
```bash
# Check PostgreSQL is running
sudo service postgresql status  # Linux
brew services list              # macOS

# Verify database exists
psql -U postgres -l
```

**Migration errors:**
```bash
# Reset migrations (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head
```

### Frontend Issues

**Port already in use:**
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5173   # Windows
```

**API connection error:**
- Verify backend is running on port 8000
- Check VITE_API_BASE_URL in frontend/.env
- Ensure CORS is configured correctly in backend

## 📝 License

This project is created for educational/demonstration purposes.

## 👤 Author

**Prabhat Jha**
- GitHub: [@prabh1805](https://github.com/prabh1805)

## 🙏 Acknowledgments

- FastAPI for the excellent async Python framework
- React team for the powerful UI library
- Tailwind CSS for the utility-first CSS framework
- PostgreSQL for the robust database system
