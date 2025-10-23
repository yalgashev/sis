# SIS Django Project Setup and Run Guide

## 🚀 Quick Setup Instructions

### 1. Prerequisites
- Python 3.12.10 (already installed)
- PostgreSQL (make sure it's running)

### 2. Install Dependencies
```bash
cd sis_project
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# First, create the database using your SQL file
psql -U postgres -c "CREATE DATABASE sis;"

# Run your admin table creation script
psql -U postgres -d sis -f ../database/create_database.sql
```

### 4. Update Database Settings
Edit `sis/settings.py` and update the database password:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sis',
        'USER': 'postgres',
        'PASSWORD': 'your_actual_password_here',  # Change this!
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Django Setup
```bash
# Create and apply Django migrations
python manage.py makemigrations
python manage.py migrate

# Create Django superuser (optional)
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```

### 7. Access the Application
- **Login Page:** http://127.0.0.1:8000/
- **Admin Dashboard:** http://127.0.0.1:8000/dashboard/ (after login)

## 🔐 Login Credentials

Use the admin credentials from your database:
- **Username:** yalgashev
- **Password:** San0bar

## 📁 Project Structure

```
sis_project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── sis/                     # Django project settings
│   ├── settings.py          # Main settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── admin_app/               # Django app for admin functionality
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URLs
│   └── apps.py              # App configuration
└── templates/               # HTML templates
    ├── login.html           # Beautiful login page
    └── dashboard.html       # Simple dashboard
```

## 🎯 How It Works

1. **Login Process:**
   - User visits `/` and sees the beautiful login page
   - Form submits to `/login/` 
   - Django validates credentials against the `admin` table
   - On success, redirects to `/dashboard/`
   - Stores admin info in session

2. **Authentication:**
   - Session-based authentication
   - Checks credentials against your PostgreSQL `admin` table
   - Tracks login time and user status

3. **Dashboard:**
   - Shows admin information
   - Displays welcome message
   - Logout functionality

## 🔧 Key Features

- ✅ Beautiful responsive login page (using your existing design)
- ✅ Session-based authentication
- ✅ PostgreSQL integration with your admin table
- ✅ Django messages for error/success feedback
- ✅ Logout functionality
- ✅ Super admin role detection

## 🛠️ Next Steps

After this basic setup, you can:
1. Add more admin functionality to the dashboard
2. Implement password hashing for security
3. Add student/faculty management features
4. Create additional pages and functionality

## 🐛 Troubleshooting

### Database Connection Issues
- Make sure PostgreSQL is running
- Check database credentials in settings.py
- Ensure the `sis` database exists

### Module Import Errors
- Make sure you're in the `sis_project` directory
- Install requirements: `pip install -r requirements.txt`

### Login Issues
- Verify admin data exists in the database
- Check username/password match exactly