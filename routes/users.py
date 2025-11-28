from flask import Blueprint, request, jsonify
from models import User, Login, db
from utils.auth import require_admin, get_current_user, hash_password
from datetime import datetime

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('', methods=['GET'])
@require_admin
def list_users():
    """List all users (admin only)"""
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users]
    }), 200

@users_bp.route('', methods=['POST'])
@require_admin
def create_user():
    """Create a new user (admin only)"""
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    is_admin = data.get('is_admin', False)  # Default to False, only admin can set this
    
    if not email or not name or not password:
        return jsonify({'error': 'Email, name, and password are required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User with this email already exists'}), 400
    
    # Create user
    user = User(email=email, name=name, is_admin=bool(is_admin))
    db.session.add(user)
    db.session.flush()  # Get user_id
    
    # Create login
    current_user = get_current_user()
    login = Login(
        user_id=user.user_id,
        password=hash_password(password),
        created_by=current_user.user_id if current_user else None
    )
    db.session.add(login)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
@require_admin
def get_user(user_id):
    """Get user details (admin only)"""
    user = User.query.get_or_404(user_id)
    return jsonify({'user': user.to_dict()}), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@require_admin
def update_user(user_id):
    """Update user details (admin only)"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # Prevent self-demotion (admin cannot remove their own admin status)
    current_user = get_current_user()
    if user_id == current_user.user_id and data.get('is_admin') is False:
        return jsonify({'error': 'You cannot remove your own admin status'}), 400
    
    # Update fields
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.user_id != user_id:
            return jsonify({'error': 'Email already in use'}), 400
        user.email = data['email']
    if 'is_admin' in data:
        user.is_admin = bool(data['is_admin'])
    
    db.session.commit()
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Delete user (admin only)"""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion
    current_user = get_current_user()
    if user_id == current_user.user_id:
        return jsonify({'error': 'You cannot delete your own account'}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

