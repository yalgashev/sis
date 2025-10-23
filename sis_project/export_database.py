#!/usr/bin/env python
import os
import subprocess
import sys

def export_database():
    """Export the current SIS database to SQL file"""
    
    # Database connection details from settings
    db_name = 'sis'
    db_user = 'postgres'
    db_host = 'localhost'
    db_port = '5432'
    
    # Output file
    output_file = 'sis_database_dump.sql'
    
    print("Exporting SIS database...")
    
    try:
        # Run pg_dump command
        cmd = [
            'pg_dump',
            f'-h', db_host,
            f'-p', db_port,
            f'-U', db_user,
            f'-d', db_name,
            f'--file={output_file}',
            '--verbose'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Database exported successfully to {output_file}")
            print(f"📁 File size: {os.path.getsize(output_file)} bytes")
        else:
            print(f"❌ Error exporting database:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ pg_dump not found. Please ensure PostgreSQL client tools are installed.")
        print("You can download from: https://www.postgresql.org/download/")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    export_database()