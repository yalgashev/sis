#!/usr/bin/env python
import os
import sys
import django

# Add Django project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis.settings')

django.setup()

from django.db import connection
from django.core.management.color import no_style

def check_database_tables():
    """Check all tables in the database"""
    
    try:
        cursor = connection.cursor()
        
        print("🗄️ Checking Database Tables...")
        print("=" * 50)
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        print(f"📋 Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            
            # Get row count for each table
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}";')
            count = cursor.fetchone()[0]
            
            print(f"  📁 {table_name:<30} ({count} rows)")
        
        print("\n🔍 Checking Django-specific tables...")
        
        # Check Django migration status
        cursor.execute("""
            SELECT app, name, applied 
            FROM django_migrations 
            ORDER BY app, id;
        """)
        
        migrations = cursor.fetchall()
        print(f"\n📦 Migration Status ({len(migrations)} migrations):")
        
        current_app = None
        for app, name, applied in migrations:
            if app != current_app:
                print(f"\n  📂 {app}:")
                current_app = app
            
            status = "✅" if applied else "❌"
            print(f"    {status} {name}")
        
        print("\n✅ Database check completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

if __name__ == "__main__":
    check_database_tables()