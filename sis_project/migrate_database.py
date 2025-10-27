#!/usr/bin/env python
"""
Complete Database Migration Script for SIS Django Project
This script performs a comprehensive migration of the entire database
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Add Django project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis.settings')

django.setup()

def full_database_migration():
    """Perform complete database migration"""
    
    print("🚀 Starting Complete Database Migration...")
    print("=" * 60)
    
    try:
        # Step 1: Check database connection
        print("1️⃣ Checking database connection...")
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        print(f"   ✅ Connected to: {db_version}")
        
        # Step 2: Create migrations for all apps
        print("\n2️⃣ Creating migrations for all apps...")
        apps = ['admin_app', 'students_app', 'tutors_app']
        
        for app in apps:
            print(f"   📦 Creating migrations for {app}...")
            call_command('makemigrations', app, verbosity=1)
        
        # Create migrations for all apps if any changes detected
        print("   📦 Creating migrations for all apps...")
        call_command('makemigrations', verbosity=1)
        
        # Step 3: Apply all migrations
        print("\n3️⃣ Applying all migrations...")
        call_command('migrate', verbosity=1)
        
        # Step 4: Synchronize unmigrated apps
        print("\n4️⃣ Synchronizing unmigrated apps...")
        call_command('migrate', '--run-syncdb', verbosity=1)
        
        # Step 5: Collect static files
        print("\n5️⃣ Collecting static files...")
        call_command('collectstatic', '--noinput', '--clear', verbosity=1)
        
        # Step 6: Verify migration status
        print("\n6️⃣ Verifying migration status...")
        
        # Check migration status
        cursor.execute("""
            SELECT app, COUNT(*) as migration_count
            FROM django_migrations 
            GROUP BY app 
            ORDER BY app;
        """)
        
        migrations = cursor.fetchall()
        print("   📋 Migration Summary:")
        for app, count in migrations:
            print(f"     📂 {app}: {count} migrations applied")
        
        # Step 7: Verify models and data
        print("\n7️⃣ Verifying models and data...")
        
        from admin_app.models import Student, Tutor, Admin, School, Department, AcademicGroup
        
        counts = {
            'Students': Student.objects.count(),
            'Tutors': Tutor.objects.count(),
            'Admins': Admin.objects.count(),
            'Schools': School.objects.count(),
            'Departments': Department.objects.count(),
            'Academic Groups': AcademicGroup.objects.count(),
        }
        
        print("   📊 Data Summary:")
        for model, count in counts.items():
            print(f"     📁 {model}: {count} records")
        
        # Step 8: Run system checks
        print("\n8️⃣ Running Django system checks...")
        call_command('check', verbosity=1)
        
        print("\n" + "=" * 60)
        print("✅ COMPLETE DATABASE MIGRATION SUCCESSFUL!")
        print("🎉 Your SIS Django project is ready for production!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_superuser_if_needed():
    """Create a superuser if none exists"""
    
    try:
        from django.contrib.auth.models import User
        
        if not User.objects.filter(is_superuser=True).exists():
            print("\n👤 No superuser found. Creating default superuser...")
            
            User.objects.create_superuser(
                username='admin',
                email='admin@sis.local',
                password='admin123'
            )
            
            print("   ✅ Superuser created:")
            print("      Username: admin")
            print("      Password: admin123")
            print("      ⚠️  Please change this password in production!")
        else:
            print("\n👤 Superuser already exists.")
            
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == "__main__":
    print("🔧 SIS Django Project - Complete Database Migration")
    print("=" * 60)
    
    # Perform full migration
    if full_database_migration():
        # Create superuser if needed
        create_superuser_if_needed()
        
        print("\n🚀 Next steps:")
        print("   1. Start the development server: python manage.py runserver")
        print("   2. Access admin panel: http://localhost:8000/admin/")
        print("   3. Access SIS application: http://localhost:8000/")
        print("\n📝 For Docker deployment:")
        print("   docker-compose up -d")
        
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)