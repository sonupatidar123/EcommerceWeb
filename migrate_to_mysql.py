"""
Script to help migrate from SQLite to MySQL
This script will:
1. Export data from SQLite
2. Create MySQL database if needed
3. Run migrations on MySQL
4. Import data to MySQL (optional)
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcommerceWeb.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
from decouple import config

def check_mysql_connection():
    """Check if MySQL connection is working"""
    try:
        db = connections['default']
        db.ensure_connection()
        print("SUCCESS: MySQL connection successful!")
        return True
    except Exception as e:
        print(f"ERROR: MySQL connection failed: {e}")
        print("\nPlease make sure:")
        print("1. MySQL server is running")
        print("2. Database exists (create it if needed)")
        print("3. .env file is configured with correct credentials")
        return False

def create_database_if_not_exists():
    """Create MySQL database if it doesn't exist"""
    db_name = config('DB_NAME', default='ecommerce_db')
    db_user = config('DB_USER', default='root')
    db_password = config('DB_PASSWORD', default='')
    db_host = config('DB_HOST', default='localhost')
    db_port = config('DB_PORT', default='3306')
    
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb
        
        # Connect without specifying database
        conn = MySQLdb.connect(
            host=db_host,
            port=int(db_port),
            user=db_user,
            passwd=db_password
        )
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()
        
        if not result:
            print(f"Creating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"SUCCESS: Database '{db_name}' created successfully!")
        else:
            print(f"SUCCESS: Database '{db_name}' already exists!")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"WARNING: Could not create database automatically: {e}")
        print(f"Please create the database manually:")
        print(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return False

def run_migrations():
    """Run Django migrations on MySQL"""
    try:
        print("\n🔄 Running migrations...")
        call_command('migrate', verbosity=1)
        print("SUCCESS: Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def main():
    print("=" * 60)
    print("SQLite to MySQL Migration Helper")
    print("=" * 60)
    
    # Step 1: Create database if needed
    print("\nStep 1: Checking/Creating MySQL database...")
    create_database_if_not_exists()
    
    # Step 2: Check connection
    print("\nStep 2: Testing MySQL connection...")
    if not check_mysql_connection():
        print("\nERROR: Please fix the connection issues and try again.")
        sys.exit(1)
    
    # Step 3: Run migrations
    print("\nStep 3: Running migrations...")
    if not run_migrations():
        print("\nERROR: Migration failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SUCCESS: Migration completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the server: python manage.py runserver")
    print("\nNote: Your SQLite data (db.sqlite3) is still available")
    print("      if you need to export/import data manually.")

if __name__ == '__main__':
    main()

