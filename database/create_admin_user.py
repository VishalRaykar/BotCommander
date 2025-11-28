"""
Script to generate SQL INSERT statement for admin user
Generates bcrypt hashed password and creates INSERT statements
"""
import sys
import os

# Try to use app's hash_password, otherwise use bcrypt directly
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.auth import hash_password
except ImportError:
    # Fallback: use bcrypt directly
    try:
        import bcrypt
        def hash_password(password: str) -> str:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except ImportError:
        print("Error: bcrypt module not found. Please install it with: pip install bcrypt")
        sys.exit(1)

def generate_admin_user_sql(email: str, name: str, password: str):
    """Generate SQL INSERT statements for admin user"""
    hashed_password = hash_password(password)
    
    # Escape single quotes in SQL
    email_escaped = email.replace("'", "''")
    name_escaped = name.replace("'", "''")
    password_hash_escaped = hashed_password.replace("'", "''")
    
    sql = f"""-- Insert admin user: {name} ({email})
-- Generated password hash for password: {password}
-- Run this script to create/update the admin user

USE `bot_commander`;

-- Insert user
INSERT INTO `user` (`email`, `name`, `is_admin`, `created_on`)
VALUES ('{email_escaped}', '{name_escaped}', TRUE, NOW())
ON DUPLICATE KEY UPDATE 
    `name` = VALUES(`name`),
    `is_admin` = TRUE;

-- Get the user_id
SET @user_id = (SELECT `user_id` FROM `user` WHERE `email` = '{email_escaped}' LIMIT 1);

-- Insert login credentials
INSERT INTO `login` (`user_id`, `password`, `created_on`, `created_by`, `is_active`)
VALUES (@user_id, '{password_hash_escaped}', NOW(), @user_id, TRUE)
ON DUPLICATE KEY UPDATE
    `password` = VALUES(`password`),
    `is_active` = TRUE,
    `updated_on` = NOW(),
    `updated_by` = @user_id;

SELECT CONCAT('Admin user created/updated: ', '{name_escaped}', ' (', '{email_escaped}', ')') AS result;
"""
    return sql

if __name__ == '__main__':
    email = 'vishal_r'
    name = 'Vishal R'
    password = 'vishal_bot_commander'
    
    print("=" * 70)
    print("Admin User SQL Generator")
    print("=" * 70)
    print(f"\nEmail: {email}")
    print(f"Name: {name}")
    print(f"Password: {password}")
    print("\n" + "=" * 70)
    print("Generated SQL:")
    print("=" * 70)
    print()
    
    sql = generate_admin_user_sql(email, name, password)
    print(sql)
    
    # Also save to file
    output_file = os.path.join(os.path.dirname(__file__), '06_insert_admin_user.sql')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql)
    
    print("\n" + "=" * 70)
    print(f"SQL saved to: {output_file}")
    print("=" * 70)
