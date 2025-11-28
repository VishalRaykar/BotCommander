from functools import wraps
from flask import session, jsonify, request
import bcrypt
from models import User, Login, db

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_user(email: str, password: str):
    """Authenticate user and create session"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return None, "User not found"
    
    login = Login.query.filter_by(user_id=user.user_id, is_active=True).first()
    if not login:
        return None, "Login not found or inactive"
    
    if not verify_password(password, login.password):
        return None, "Invalid password"
    
    session['user_id'] = user.user_id
    session['email'] = user.email
    session['name'] = user.name
    return user, None

def logout_user():
    """Clear user session"""
    session.clear()

def get_current_user():
    """Get current logged in user"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)

def is_admin():
    """Check if current user is admin"""
    user = get_current_user()
    if not user:
        return False
    return user.is_admin

def require_login(f):
    """Decorator to require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    @require_login
    def decorated_function(*args, **kwargs):
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

