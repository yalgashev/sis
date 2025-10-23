#!/usr/bin/env python
"""
Django Database Export Script
Exports database schema and data using Django's management commands
"""

import os
import sys
import subprocess
from datetime import datetime

# Add Django project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis.settings')

import django
django.setup()

from django.core.management import call_command
from django.db import connection
from django.conf import settings

def export_database():
    """Export database using Django management commands"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = "database_exports"
    
    # Create export directory
    os.makedirs(export_dir, exist_ok=True)
    
    print("🗄️ Exporting SIS Database with Django...")
    print(f"📁 Export directory: {export_dir}")
    
    try:
        # 1. Export all data as JSON (Django fixtures format)
        json_file = os.path.join(export_dir, f"sis_data_{timestamp}.json")
        print(f"📋 Exporting data to: {json_file}")
        
        call_command('dumpdata', 
                    '--indent=2', 
                    '--output=' + json_file,
                    '--exclude=contenttypes',
                    '--exclude=auth.Permission',
                    '--exclude=sessions.Session')
        
        # 2. Export schema (SQL CREATE statements)
        sql_file = os.path.join(export_dir, f"sis_schema_{timestamp}.sql")
        print(f"🏗️ Exporting schema to: {sql_file}")
        
        with open(sql_file, 'w', encoding='utf-8') as f:
            # Get SQL statements for creating tables
            with connection.cursor() as cursor:
                # Get all table names
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                """)
                
                tables = [row[0] for row in cursor.fetchall()]
                
                f.write("-- SIS Database Schema Export\n")
                f.write(f"-- Generated on: {datetime.now()}\n")
                f.write(f"-- Database: {settings.DATABASES['default']['NAME']}\n\n")
                
                for table in tables:
                    if not table.startswith('django_') and not table.startswith('auth_'):
                        # Get CREATE TABLE statement
                        cursor.execute(f"""
                            SELECT 
                                'CREATE TABLE ' || schemaname||'.'||tablename || ' (' ||
                                array_to_string(
                                    array_agg(
                                        column_name || ' ' || type || coalesce(' ' || not_null, '') ||
                                        coalesce(' DEFAULT ' || column_default, '')
                                    ), ', '
                                ) || ');'
                            FROM (
                                SELECT 
                                    schemaname, tablename, column_name, type, not_null, column_default
                                FROM (
                                    SELECT 
                                        n.nspname AS schemaname,
                                        c.relname AS tablename,
                                        a.attname AS column_name,
                                        pg_catalog.format_type(a.atttypid, a.atttypmod) AS type,
                                        CASE WHEN a.attnotnull THEN 'NOT NULL' ELSE '' END AS not_null,
                                        pg_catalog.pg_get_expr(d.adbin, d.adrelid) AS column_default
                                    FROM pg_catalog.pg_class c
                                    LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                                    LEFT JOIN pg_catalog.pg_attribute a ON a.attrelid = c.oid
                                    LEFT JOIN pg_catalog.pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
                                    WHERE c.relname = '{table}' AND a.attnum > 0 AND NOT a.attisdropped
                                    ORDER BY a.attnum
                                ) AS sq
                            ) AS q
                            GROUP BY schemaname, tablename;
                        """)
                        
                        result = cursor.fetchone()
                        if result:
                            f.write(f"-- Table: {table}\n")
                            f.write(result[0] + "\n\n")
        
        # 3. Create a combined SQL file with both schema and data
        combined_file = os.path.join(export_dir, f"sis_complete_{timestamp}.sql")
        print(f"🔗 Creating combined export: {combined_file}")
        
        # Convert JSON data to SQL INSERT statements
        import json
        
        with open(json_file, 'r', encoding='utf-8') as json_f:
            data = json.load(json_f)
        
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write("-- SIS Complete Database Export (Schema + Data)\n")
            f.write(f"-- Generated on: {datetime.now()}\n")
            f.write(f"-- Database: {settings.DATABASES['default']['NAME']}\n\n")
            
            # Add schema
            f.write("-- SCHEMA\n")
            with open(sql_file, 'r', encoding='utf-8') as schema_f:
                f.write(schema_f.read())
            
            f.write("\n-- DATA\n")
            
            # Group data by model
            model_data = {}
            for item in data:
                model = item['model']
                if model not in model_data:
                    model_data[model] = []
                model_data[model].append(item)
            
            # Generate INSERT statements
            for model, items in model_data.items():
                if items:
                    app_label, model_name = model.split('.')
                    table_name = f"{app_label}_{model_name}"
                    
                    f.write(f"\n-- Data for {model}\n")
                    
                    for item in items:
                        fields = item['fields']
                        if fields:  # Skip empty records
                            columns = ', '.join(f'"{k}"' for k in fields.keys())
                            values = []
                            for v in fields.values():
                                if v is None:
                                    values.append('NULL')
                                elif isinstance(v, bool):
                                    values.append('true' if v else 'false')
                                elif isinstance(v, (int, float)):
                                    values.append(str(v))
                                else:
                                    # Escape single quotes in strings
                                    escaped = str(v).replace("'", "''")
                                    values.append(f"'{escaped}'")
                            
                            values_str = ', '.join(values)
                            f.write(f"INSERT INTO {table_name} (id, {columns}) VALUES ({item['pk']}, {values_str});\n")
        
        # 4. Create database initialization script for Docker
        docker_init_file = os.path.join(export_dir, "01-init.sql")
        print(f"🐳 Creating Docker init script: {docker_init_file}")
        
        # Copy the combined file as Docker initialization script
        import shutil
        shutil.copy2(combined_file, docker_init_file)
        
        # 5. Display export summary
        print("\n✅ Database export completed successfully!")
        print(f"\n📊 Export Summary:")
        print(f"   📁 Directory: {os.path.abspath(export_dir)}")
        print(f"   📋 JSON Data: {json_file}")
        print(f"   🏗️ SQL Schema: {sql_file}")
        print(f"   🔗 Combined SQL: {combined_file}")
        print(f"   🐳 Docker Init: {docker_init_file}")
        
        # Get file sizes
        for filename in [json_file, sql_file, combined_file]:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                if size > 1024 * 1024:
                    size_str = f"{size / 1024 / 1024:.1f} MB"
                elif size > 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size} bytes"
                print(f"   📁 {os.path.basename(filename)}: {size_str}")
        
        print(f"\n🚀 Ready for deployment:")
        print(f"   1. Copy '{docker_init_file}' to your server")
        print(f"   2. Place it in the 'database_init/' directory")
        print(f"   3. Run 'docker-compose up -d' to deploy")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during export: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    export_database()