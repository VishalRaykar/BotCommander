"""
Database initialization script
Creates all tables and optionally creates an admin user
Run this after creating the database using the SQL scripts
"""
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Login
from utils.auth import hash_password

def init_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@botcommander.com').first()
        if not admin:
            # Create admin user
            admin = User(
                email='admin@botcommander.com',
                name='Administrator',
                is_admin=True
            )
            db.session.add(admin)
            db.session.flush()
            
            # Create admin login
            admin_login = Login(
                user_id=admin.user_id,
                password=hash_password('admin123'),  # Change this password!
                created_by=admin.user_id
            )
            db.session.add(admin_login)
            db.session.commit()
            print("✓ Admin user created!")
            print("  Email: admin@botcommander.com")
            print("  Password: admin123")
            print("  ⚠️  Please change the admin password after first login!")
        else:
            print("ℹ Admin user already exists.")

if __name__ == '__main__':
    print("=" * 60)
    print("BotCommander Database Initialization")
    print("=" * 60)
    init_database()
    print("=" * 60)
    print("Database initialization complete!")
    print("=" * 60)

