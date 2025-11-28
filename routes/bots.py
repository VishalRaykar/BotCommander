from flask import Blueprint, request, jsonify
from models import UserBot, User, BotBehaviour, db
from utils.auth import require_login, require_admin, get_current_user
from utils.encryption import encrypt_bot_id, decrypt_bot_id
from sqlalchemy.exc import IntegrityError

bots_bp = Blueprint('bots', __name__, url_prefix='/api/bots')

@bots_bp.route('', methods=['GET'])
@require_login
def list_bots():
    """List all bots assigned to current user"""
    user = get_current_user()
    user_bots = UserBot.query.filter_by(user_id=user.user_id, is_active=True).all()
    
    bots = []
    for ub in user_bots:
        bot_data = ub.to_dict(decrypt_bot_id=True)
        bots.append({
            'assign_id': bot_data['assign_id'],
            'bot_id': bot_data['bot_id'],
            'created_on': bot_data['created_on']
        })
    
    return jsonify({'bots': bots}), 200

@bots_bp.route('/<int:assign_id>', methods=['GET'])
@require_login
def get_bot_details(assign_id):
    """Get bot details by assign_id"""
    user = get_current_user()
    user_bot = UserBot.query.filter_by(
        assign_id=assign_id,
        user_id=user.user_id,
        is_active=True
    ).first_or_404()
    
    bot_data = user_bot.to_dict(decrypt_bot_id=True)
    
    # Get or create bot behaviour
    behaviour = BotBehaviour.query.filter_by(assign_id=assign_id, is_active=True).first()
    if not behaviour:
        # Create default behaviour record
        behaviour = BotBehaviour(
            assign_id=assign_id,
            created_by=user.user_id
        )
        db.session.add(behaviour)
        db.session.commit()
    
    bot_data['behaviour'] = behaviour.to_dict()
    return jsonify({'bot': bot_data}), 200

@bots_bp.route('', methods=['POST'])
@require_admin
def assign_bot():
    """Assign bot to user (admin only)"""
    data = request.get_json()
    user_id = data.get('user_id')
    bot_id = data.get('bot_id')
    
    if not user_id or not bot_id:
        return jsonify({'error': 'user_id and bot_id are required'}), 400
    
    # Verify user exists
    user = User.query.get_or_404(user_id)
    
    # Encrypt bot_id
    encrypted_bot_id = encrypt_bot_id(bot_id)
    
    # Check if bot_id already exists
    existing_bot = UserBot.query.filter_by(bot_id=encrypted_bot_id, is_active=True).first()
    if existing_bot:
        return jsonify({'error': 'This bot is already assigned to another user'}), 400
    
    # Create assignment
    current_user = get_current_user()
    try:
        user_bot = UserBot(
            user_id=user_id,
            bot_id=encrypted_bot_id,
            created_by=current_user.user_id if current_user else None
        )
        db.session.add(user_bot)
        db.session.flush()  # Get assign_id
        
        # Create default behaviour record
        behaviour = BotBehaviour(
            assign_id=user_bot.assign_id,
            created_by=current_user.user_id if current_user else None
        )
        db.session.add(behaviour)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # Check if it's a unique constraint violation
        if 'bot_id' in str(e.orig) or 'Duplicate entry' in str(e.orig):
            return jsonify({'error': 'This bot is already assigned to another user'}), 400
        raise
    
    return jsonify({
        'message': 'Bot assigned successfully',
        'assign_id': user_bot.assign_id
    }), 201

@bots_bp.route('/<int:assign_id>/control', methods=['POST'])
@require_login
def control_bot(assign_id):
    """Control bot actions"""
    user = get_current_user()
    user_bot = UserBot.query.filter_by(
        assign_id=assign_id,
        user_id=user.user_id,
        is_active=True
    ).first_or_404()
    
    data = request.get_json()
    action = data.get('action')
    value = data.get('value')
    
    if not action:
        return jsonify({'error': 'Action is required'}), 400
    
    # Get or create bot behaviour
    behaviour = BotBehaviour.query.filter_by(assign_id=assign_id, is_active=True).first()
    if not behaviour:
        behaviour = BotBehaviour(
            assign_id=assign_id,
            created_by=user.user_id
        )
        db.session.add(behaviour)
        db.session.flush()
    
    # Valid actions mapping to database columns
    action_map = {
        'bot_state': 'bot_state',
        'hard_stop_all_trades': 'hard_stop_all_trades',
        'listen_to_common_commander': 'listen_to_common_commander',
        'news_based_start_stop': 'news_based_start_stop',
        'refresh_data_from_bot': 'refresh_data_from_bot'
    }
    
    if action not in action_map:
        return jsonify({'error': f'Invalid action. Valid actions: {", ".join(action_map.keys())}'}), 400
    
    # Update the behaviour record
    column_name = action_map[action]
    setattr(behaviour, column_name, bool(value))
    behaviour.updated_by = user.user_id
    db.session.commit()
    
    # Decrypt bot_id for API call (if needed for actual bot communication)
    bot_id = decrypt_bot_id(user_bot.bot_id)
    
    # Here you would make API call to the actual bot
    # TODO: Implement actual bot API communication using bot_id and the updated behaviour
    
    return jsonify({
        'message': f'Bot control action "{action}" updated successfully',
        'bot_id': bot_id,
        'action': action,
        'value': value,
        'behaviour': behaviour.to_dict()
    }), 200

@bots_bp.route('/<int:assign_id>', methods=['DELETE'])
@require_admin
def unassign_bot(assign_id):
    """Unassign bot from user (admin only)"""
    user_bot = UserBot.query.get_or_404(assign_id)
    user_bot.is_active = False
    current_user = get_current_user()
    user_bot.updated_by = current_user.user_id if current_user else None
    db.session.commit()
    
    return jsonify({'message': 'Bot unassigned successfully'}), 200

