# MySQL Database Setup Guide

## Prerequisites
1. MySQL Server installed and running
2. MySQL client tools installed

## Step 1: Create MySQL Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or if you want to use a different database name, update the `.env` file accordingly.

## Step 2: Create MySQL User (Optional but Recommended)

```sql
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

## Step 3: Configure Environment Variables

Create a `.env` file in the project root directory with the following:

```
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

**Note:** Replace `your_mysql_password` with your actual MySQL root password (or the user password if you created a separate user).

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Run Migrations

```bash
python manage.py migrate
```

This will create all the necessary tables in your MySQL database.

## Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Troubleshooting

### Connection Error
- Make sure MySQL server is running
- Verify the database name, username, and password in `.env` file
- Check if MySQL is listening on the correct port (default: 3306)

### Character Set Issues
- The database is configured to use `utf8mb4` character set which supports all Unicode characters including emojis

### PyMySQL Installation Issues
- If you encounter issues with PyMySQL, you can alternatively use `mysqlclient`:
  ```bash
  pip install mysqlclient
  ```
  Note: `mysqlclient` requires MySQL development libraries to be installed on your system.

