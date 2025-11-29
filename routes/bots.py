

# Place this endpoint after bots_bp is defined
from flask import Blueprint, request, jsonify
from models import UserBot, User, BotBehaviour, db
from utils.auth import require_login, require_admin, get_current_user
from utils.encryption import encrypt_bot_id, decrypt_bot_id
from sqlalchemy.exc import IntegrityError

bots_bp = Blueprint('bots', __name__, url_prefix='/api/bots')

@bots_bp.route('', methods=['GET'])
@require_login
def list_bots():
    """List bots - for admin: filtered by user_id query param, for users: their own bots"""
    try:
        user = get_current_user()
        # For admin, get user_id from query params (default to self)
        if user.is_admin:
            view_user_id = request.args.get('user_id', user.user_id, type=int)
            # Admin sees all bots for selected user
            user_bots = UserBot.query.filter_by(user_id=view_user_id, is_active=True).all()
        else:
            # Regular users see only their own bots
            user_bots = UserBot.query.filter_by(user_id=user.user_id, is_active=True).all()
        bots = []
        for ub in user_bots:
            try:
                bot_data = ub.to_dict(decrypt_bot_id=True)
                bots.append({
                    'assign_id': bot_data['assign_id'],
                    'bot_id': bot_data['bot_id'],
                    'user_id': bot_data['user_id'],
                    'allow_admin_control': bot_data['allow_admin_control'],
                    'created_on': bot_data['created_on']
                })
            except Exception as e:
                # Log error but continue with other bots
                print(f"Error processing bot {ub.assign_id}: {str(e)}")
                bots.append({
                    'assign_id': ub.assign_id,
                    'user_id': ub.user_id,
                    'bot_id': '[Decryption Error]',
                    'allow_admin_control': getattr(ub, 'allow_admin_control', False),
                    'created_on': ub.created_on.isoformat() if ub.created_on else None
                })
        return jsonify({'bots': bots}), 200
    except Exception as e:
        import traceback
        print(f"Error in list_bots: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to load bots: {str(e)}'}), 500

@bots_bp.route('/<int:assign_id>', methods=['GET'])
@require_login
def get_bot_details(assign_id):
    """Get bot details by assign_id - checks ownership or admin control permission"""
    try:
        user = get_current_user()
        user_bot = UserBot.query.filter_by(assign_id=assign_id, is_active=True).first_or_404()
        # Check if user can access this bot
        if user_bot.user_id != user.user_id:
            # Admin can view any bot, but controls depend on allow_admin_control
            if not user.is_admin:
                return jsonify({'error': 'Access denied'}), 403
        bot_data = user_bot.to_dict(decrypt_bot_id=True)
        # Add flag for admin control permission (for frontend)
        can_admin_control = False
        if user.user_id == user_bot.user_id:
            can_admin_control = True  # Owner always has control
        elif user.is_admin:
            can_admin_control = bool(user_bot.allow_admin_control)
        bot_data['can_admin_control'] = can_admin_control
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
    except Exception as e:
        import traceback
        print(f"Error in get_bot_details: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to load bot details: {str(e)}'}), 500

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
    """Control bot actions or toggle admin control permission"""
    user = get_current_user()
    user_bot = UserBot.query.filter_by(assign_id=assign_id, is_active=True).first_or_404()
    # Check if user can control this bot (except for validity update)
    data = request.get_json()
    action = data.get('action')
    value = data.get('value')
    if not action:
        return jsonify({'error': 'Action is required'}), 400
    # Allow admin to update validity even if admin control is not enabled
    if action == 'validity':
        if not user.is_admin:
            return jsonify({'error': 'Only admin can update validity'}), 403
        from datetime import datetime
        try:
            print('Received validity value:', value)  # Debug print
            # Remove trailing Z if present (Z = UTC)
            val = value.rstrip('Z') if value else None
            user_bot.validity = datetime.fromisoformat(val) if val else None
            print('Parsed validity:', user_bot.validity)  # Debug print
            user_bot.updated_by = user.user_id
            db.session.commit()
            return jsonify({'message': 'Validity updated successfully', 'validity': user_bot.validity.isoformat() if user_bot.validity else None}), 200
        except Exception as e:
            print('Error parsing validity:', str(e))  # Debug print
            return jsonify({'error': f'Invalid datetime format: {str(e)}'}), 400
    # Handle allow_admin_control toggle (only bot owner can change)
    if action == 'allow_admin_control':
        if user_bot.user_id != user.user_id:
            return jsonify({'error': 'Only bot owner can change admin control permission'}), 403
        user_bot.allow_admin_control = bool(value)
        user_bot.updated_by = user.user_id
        db.session.commit()
        return jsonify({
            'message': 'Admin control permission updated successfully',
            'allow_admin_control': user_bot.allow_admin_control
        }), 200
    # For all other actions, check control permission
    if user_bot.user_id != user.user_id:
        if not (user.is_admin and user_bot.allow_admin_control):
            return jsonify({'error': 'Access denied'}), 403
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
        valid_actions = ', '.join(action_map.keys())
        return jsonify({'error': f'Invalid action. Valid actions: {valid_actions}'}), 400
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

