@echo off
REM BotCommander Database Setup Script for Windows
REM Run all database setup scripts in order

echo ==========================================
echo BotCommander Database Setup
echo ==========================================
echo.

REM Prompt for MySQL credentials
set /p DB_USER="MySQL username [root]: "
if "%DB_USER%"=="" set DB_USER=root
set /p DB_PASS="MySQL password: "

REM Create database
echo.
echo Step 1: Creating database...
mysql -u %DB_USER% -p%DB_PASS% < 01_create_database.sql
if errorlevel 1 (
    echo Failed to create database
    exit /b 1
)
echo Database created successfully

REM Create tables
echo.
echo Step 2: Creating tables...
mysql -u %DB_USER% -p%DB_PASS% < 02_create_tables.sql
if errorlevel 1 (
    echo Failed to create tables
    exit /b 1
)
echo Tables created successfully

REM Initialize with Python
echo.
echo Step 3: Initializing with Python (creating admin user)...
python init_db.py
if errorlevel 1 (
    echo Failed to initialize database
    exit /b 1
)
echo Database initialized successfully

echo.
echo ==========================================
echo Database setup complete!
echo ==========================================
pause

