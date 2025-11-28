"""
Script to create user: vishalraykar6@gmail.com
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Login
from utils.auth import hash_password

def create_user():
    app = create_app()
    with app.app_context():
        email = 'vishalraykar6@gmail.com'
        name = 'Vishal Raykar'
        password = 'vishal_bot_commander'
        is_admin = True  # Set as admin
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create user
            user = User(
                email=email,
                name=name,
                is_admin=is_admin
            )
            db.session.add(user)
            db.session.flush()
            print(f"✓ Created user: {name} ({email})")
        else:
            # Update existing user
            user.name = name
            user.is_admin = is_admin
            print(f"✓ Updated user: {name} ({email})")
        
        # Create or update login
        login = Login.query.filter_by(user_id=user.user_id).first()
        if not login:
            login = Login(
                user_id=user.user_id,
                password=hash_password(password),
                created_by=user.user_id,
                is_active=True
            )
            db.session.add(login)
            print(f"✓ Created login credentials")
        else:
            login.password = hash_password(password)
            login.is_active = True
            login.updated_by = user.user_id
            print(f"✓ Updated login credentials")
        
        db.session.commit()
        print(f"\n✓ User '{name}' created/updated successfully!")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"  Admin: {is_admin}")

if __name__ == '__main__':
    print("=" * 70)
    print("Creating User: vishalraykar6@gmail.com")
    print("=" * 70)
    print()
    create_user()
    print("=" * 70)

