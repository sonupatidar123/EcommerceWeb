# Complete SQLite to MySQL Migration Guide

## Prerequisites Checklist

- [ ] MySQL Server installed and running
- [ ] PyMySQL installed (`pip install PyMySQL`)
- [ ] python-decouple installed (`pip install python-decouple`)

## Step 1: Create MySQL Database

Open MySQL command line (or MySQL Workbench) and run:

```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or use a different database name if you prefer.

## Step 2: Create .env File

Create a `.env` file in the project root directory (`C:\Users\sonup\Desktop\EcommerceWeb\.env`) with:

```env
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_HOST=localhost
DB_PORT=3306
```

**Important:** Replace `your_mysql_password_here` with your actual MySQL root password.

## Step 3: Run Migration Script

Use the automated migration script:

```bash
python migrate_to_mysql.py
```

This script will:
- ✅ Check/create the MySQL database
- ✅ Test the connection
- ✅ Run all Django migrations
- ✅ Create all necessary tables

## Step 4: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Step 5: Verify Migration

Test the connection:

```bash
python manage.py check --database default
```

Start the server:

```bash
python manage.py runserver
```

## Manual Migration Steps (Alternative)

If you prefer to do it manually:

### 1. Test Connection
```bash
python manage.py check --database default
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

## Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"
- Check your MySQL password in the `.env` file
- Verify MySQL server is running
- Try connecting with MySQL client to verify credentials

### Error: "Unknown database 'ecommerce_db'"
- Create the database manually (see Step 1)
- Or let the migration script create it for you

### Error: "ModuleNotFoundError: No module named 'pymysql'"
```bash
pip install PyMySQL
```

### Error: "ModuleNotFoundError: No module named 'decouple'"
```bash
pip install python-decouple
```

## Data Migration (Optional)

If you have important data in SQLite that you want to migrate:

### Option 1: Using Django dumpdata/loaddata
```bash
# Export from SQLite (temporarily switch back to SQLite in settings)
python manage.py dumpdata > data.json

# Switch to MySQL and import
python manage.py loaddata data.json
```

### Option 2: Manual SQL Export/Import
- Export data from SQLite using SQLite tools
- Import into MySQL using MySQL tools
- **Note:** This requires careful handling of data types and foreign keys

## Verification

After migration, verify everything works:

1. ✅ Server starts without errors
2. ✅ Can access admin panel
3. ✅ Can register new users
4. ✅ Can login/logout
5. ✅ Database tables exist in MySQL

## Current Status

- ✅ Database configuration updated to MySQL
- ✅ PyMySQL installed and configured
- ✅ Migration script created
- ⏳ **Next:** Create `.env` file and run migrations

