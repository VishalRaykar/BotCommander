# Database Setup Scripts

This folder contains all database-related scripts for BotCommander.

## Database Name
**bot_commander**

## Setup Instructions

### Quick Setup (All-in-One)

**Windows:**
```bash
run_all.bat
```

**Linux/Mac:**
```bash
chmod +x run_all.sh
./run_all.sh
```

This will run all scripts in the correct order automatically.

### Manual Setup

#### Option 1: Using SQL Scripts (Recommended for Production)

1. **Create the database:**
   ```bash
   mysql -u root -p < 01_create_database.sql
   ```

2. **Create all tables:**
   ```bash
   mysql -u root -p < 02_create_tables.sql
   ```

3. **Initialize with Python (creates admin user):**
   ```bash
   python init_db.py
   ```
   Or from project root:
   ```bash
   python database/init_db.py
   ```

### Option 2: Using Python Only (Development)

1. **Create the database manually:**
   ```sql
   CREATE DATABASE bot_commander CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Run the Python initialization script:**
   ```bash
   python init_db.py
   ```
   Or from project root:
   ```bash
   python database/init_db.py
   ```

## Scripts Overview

### `01_create_database.sql`
- Creates the `bot_commander` database
- Sets proper character set and collation

### `02_create_tables.sql`
- Creates all required tables:
  - `user` - User information (includes `is_admin` column)
  - `login` - Authentication credentials
  - `user_bot` - Bot assignments (with encrypted bot_id)
  - `bots_behaviour` - Bot control settings and behaviours

### `03_add_is_admin_column.sql`
- Migration script for existing databases
- Adds `is_admin` column to the `user` table
- Sets first user (user_id = 1) as admin if upgrading from old version
- Run this if you have an existing database without the `is_admin` column

### `04_add_bots_behaviour_table.sql`
- Migration script for existing databases
- Creates the `bots_behaviour` table to store bot control settings
- Creates default behaviour records for existing bot assignments
- Run this if you have an existing database without the `bots_behaviour` table

### `05_add_bot_id_unique_constraint.sql`
- Migration script for existing databases
- Adds UNIQUE constraint to `bot_id` column in `user_bot` table
- Ensures each bot can only be assigned to one user at a time
- Run this if you have an existing database without the unique constraint
- **Note**: Check for duplicate bot_ids before running this script

### `init_db.py`
- Python script that uses SQLAlchemy to:
  - Create all tables (if using Python approach)
  - Create default admin user
  - Set up initial data

## Default Admin Credentials

After running `init_db.py`:
- **Email**: admin@botcommander.com
- **Password**: admin123

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

## Creating Additional Admin Users

### Using Python Script (Recommended)

To create the admin user "vishal_r":

```bash
python database/create_vishal_admin.py
```

This will create:
- **Email**: vishal_r
- **Name**: Vishal R
- **Password**: vishal_bot_commander
- **Admin**: Yes

### Using SQL Script

1. Generate the SQL with proper password hash:
   ```bash
   python database/create_admin_user.py
   ```
   This will generate `06_insert_admin_user.sql` with the encrypted password.

2. Run the generated SQL:
   ```bash
   mysql -u root -p < database/06_insert_admin_user.sql
   ```

## Migration from Old Version

### Adding is_admin column

If you have an existing database without the `is_admin` column:

```bash
mysql -u root -p < 03_add_is_admin_column.sql
```

This will add the `is_admin` column and set the first user as admin.

### Adding bots_behaviour table

If you have an existing database without the `bots_behaviour` table:

```bash
mysql -u root -p < 04_add_bots_behaviour_table.sql
```

This will create the `bots_behaviour` table and create default behaviour records for existing bot assignments.

### Adding unique constraint to bot_id

If you have an existing database without the unique constraint on `bot_id`:

```bash
mysql -u root -p < 05_add_bot_id_unique_constraint.sql
```

**Important**: Before running this script, check for duplicate bot_ids:
```sql
SELECT bot_id, COUNT(*) as count
FROM user_bot
WHERE is_active = TRUE
GROUP BY bot_id
HAVING count > 1;
```

If duplicates exist, resolve them first (e.g., by deactivating duplicate assignments) before adding the unique constraint.

## Notes

- All scripts are idempotent (safe to run multiple times)
- The SQL scripts use `CREATE TABLE IF NOT EXISTS` to prevent errors
- Foreign key constraints ensure data integrity
- Bot IDs are stored encrypted in the `user_bot` table
- Admin status is now controlled by the `is_admin` column in the `user` table

