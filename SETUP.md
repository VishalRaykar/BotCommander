# BotCommander Setup Guide

## Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database

**Option 1: Using SQL Scripts (Recommended)**

Run the database scripts in order:

```bash
mysql -u root -p < database/01_create_database.sql
mysql -u root -p < database/02_create_tables.sql
```

**Option 2: Manual Creation**

Login to MySQL and create the database:

```sql
CREATE DATABASE bot_commander CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=bot_commander

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production

# Encryption Key (generate using generate_key.py)
ENCRYPTION_KEY=your-generated-encryption-key-here
```

### 4. Generate Encryption Key

Run the key generation script:

```bash
python generate_key.py
```

Copy the generated key and paste it into your `.env` file as `ENCRYPTION_KEY`.

### 5. Initialize Database

Run the database initialization script:

```bash
python database/init_db.py
```

Or if you're in the database folder:

```bash
cd database
python init_db.py
```

This will:
- Create all necessary database tables (if using Python approach)
- Create an admin user with default credentials

**Note**: If you used the SQL scripts (Option 1 in step 2), the tables are already created. The Python script will only create the admin user.

### 6. Start the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Default Admin Credentials

- **Email**: admin@botcommander.com
- **Password**: admin123

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

## Usage Workflow

1. **Login** as admin using the default credentials
2. Navigate to **Admin Panel** (`/admin`)
3. **Create Users** - Add new users who will use the bot control system
4. **Assign Bots** - Assign bot IDs to users (bot IDs are encrypted in the database)
5. **User Login** - Users can login and see their assigned bots
6. **Control Bots** - Users click "Details" on any bot to access the control panel with toggle switches

## Bot Control Features

Each bot has the following controls:

1. **Bot State** - Turn bot ON/OFF
2. **Hard Stop All Trades** - Close all trades and stop new trades
3. **Listen to Common Commander** - Enable common controller API
4. **News Based Start Stop** - Enable news-based start/stop feature
5. **Refresh Data from Bot** - Refresh bot data in database

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/me` - Get current user info

### Users (Admin Only)
- `GET /api/users` - List all users
- `POST /api/users` - Create new user
- `GET /api/users/<id>` - Get user details
- `DELETE /api/users/<id>` - Delete user

### Bots
- `GET /api/bots` - List user's assigned bots
- `GET /api/bots/<assign_id>` - Get bot details
- `POST /api/bots` - Assign bot to user (admin only)
- `POST /api/bots/<assign_id>/control` - Control bot actions
- `DELETE /api/bots/<assign_id>` - Unassign bot (admin only)

## Security Notes

- Bot IDs are encrypted using Fernet (symmetric encryption) before storing in database
- Passwords are hashed using bcrypt
- Session-based authentication
- Admin access is restricted to the first user (user_id = 1)

## Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check database credentials in `.env`
- Ensure database exists

### Encryption Key Error
- Generate a new key using `generate_key.py`
- Update `ENCRYPTION_KEY` in `.env`
- Restart the application

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

