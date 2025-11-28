#!/bin/bash
# BotCommander Database Setup Script
# Run all database setup scripts in order

echo "=========================================="
echo "BotCommander Database Setup"
echo "=========================================="
echo ""

# Check if MySQL is available
if ! command -v mysql &> /dev/null; then
    echo "Error: MySQL client not found. Please install MySQL client."
    exit 1
fi

# Prompt for MySQL credentials
read -p "MySQL username [root]: " DB_USER
DB_USER=${DB_USER:-root}
read -sp "MySQL password: " DB_PASS
echo ""

# Create database
echo "Step 1: Creating database..."
mysql -u "$DB_USER" -p"$DB_PASS" < 01_create_database.sql
if [ $? -eq 0 ]; then
    echo "✓ Database created successfully"
else
    echo "✗ Failed to create database"
    exit 1
fi

# Create tables
echo ""
echo "Step 2: Creating tables..."
mysql -u "$DB_USER" -p"$DB_PASS" < 02_create_tables.sql
if [ $? -eq 0 ]; then
    echo "✓ Tables created successfully"
else
    echo "✗ Failed to create tables"
    exit 1
fi

# Initialize with Python
echo ""
echo "Step 3: Initializing with Python (creating admin user)..."
python init_db.py
if [ $? -eq 0 ]; then
    echo "✓ Database initialized successfully"
else
    echo "✗ Failed to initialize database"
    exit 1
fi

echo ""
echo "=========================================="
echo "Database setup complete!"
echo "=========================================="

