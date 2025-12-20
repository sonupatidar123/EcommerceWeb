"""
Quick MySQL Migration Script
Run this after setting up .env file with MySQL credentials
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcommerceWeb.settings')
django.setup()

from django.core.management import call_command
from django.db import connections

def main():
    print("=" * 60)
    print("MySQL Migration Script")
    print("=" * 60)
    
    # Test connection
    print("\nTesting MySQL connection...")
    try:
        db = connections['default']
        db.ensure_connection()
        print("SUCCESS: MySQL connection successful!")
    except Exception as e:
        print(f"ERROR: MySQL connection failed: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. .env file has correct DB_PASSWORD")
        print("3. Database exists (create it if needed)")
        print("\nTo create database, run in MySQL:")
        print("CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        sys.exit(1)
    
    # Run migrations
    print("\nRunning migrations...")
    try:
        call_command('migrate', verbosity=1)
        print("\nSUCCESS: Migrations completed!")
        print("\nNext steps:")
        print("1. Create superuser: python manage.py createsuperuser")
        print("2. Start server: python manage.py runserver")
    except Exception as e:
        print(f"ERROR: Migration failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

