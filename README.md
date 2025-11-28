# BotCommander

A Python-MySQL web application for managing and controlling trading bots remotely.

## Features

- User authentication and management
- Bot assignment to users
- Remote bot control via web interface
- Secure bot ID encryption
- Admin panel for user and bot management

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Generate encryption key:
```bash
python generate_key.py
# Copy the generated key and add it to your .env file as ENCRYPTION_KEY
```

4. Create MySQL database:
   - Option 1: Use SQL script (recommended):
     ```bash
     mysql -u root -p < database/01_create_database.sql
     mysql -u root -p < database/02_create_tables.sql
     ```
   - Option 2: Create manually:
     ```sql
     CREATE DATABASE bot_commander CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     ```

5. Initialize database:
```bash
python database/init_db.py
```

6. Run the application:
```bash
python app.py
```

7. Access the web interface at `http://localhost:5000`

## Default Admin Credentials

After running `init_db.py`, you can login with:
- **Email**: admin@botcommander.com
- **Password**: admin123

⚠️ **Important**: Change the admin password immediately after first login!

## Usage

1. **Login** as admin using the default credentials
2. **Create Users** via the Admin panel (`/admin`)
3. **Assign Bots** to users via the Admin panel
4. **Users** can login and see their assigned bots on the Dashboard
5. **Control Bots** by clicking "Details" on any bot to access the control panel

## Database Schema

- `user`: User information
- `login`: User authentication credentials
- `user_bot`: Bot assignments to users (with encrypted bot_id)

## API Endpoints

- `/api/login` - User login
- `/api/logout` - User logout
- `/api/users` - User management (admin only)
- `/api/bots` - Bot management
- `/api/bots/<bot_id>/control` - Bot control actions

