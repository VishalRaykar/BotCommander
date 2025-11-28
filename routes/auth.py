from flask import Blueprint, request, jsonify, session
from models import User, Login, db
from utils.auth import login_user, logout_user, get_current_user, hash_password, require_login

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user, error = login_user(email, password)
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        import traceback
        print(f"Login error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
@require_login
def logout():
    """User logout endpoint"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/me', methods=['GET'])
@require_login
def get_me():
    """Get current user information"""
    user = get_current_user()
    return jsonify({'user': user.to_dict()}), 200

