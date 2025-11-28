from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    login = db.relationship('Login', foreign_keys='[Login.user_id]', backref='user', uselist=False, cascade='all, delete-orphan')
    user_bots = db.relationship('UserBot', foreign_keys='[UserBot.user_id]', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'is_admin': self.is_admin,
            'created_on': self.created_on.isoformat() if self.created_on else None
        }

class Login(db.Model):
    __tablename__ = 'login'
    
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def to_dict(self):
        return {
            'login_id': self.login_id,
            'user_id': self.user_id,
            'is_active': self.is_active,
            'created_on': self.created_on.isoformat() if self.created_on else None
        }

class UserBot(db.Model):
    __tablename__ = 'user_bot'
    
    assign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    bot_id = db.Column(db.Text, nullable=False, unique=True)  # Encrypted bot_id stored as text, unique
    allow_admin_control = db.Column(db.Boolean, default=False, nullable=False)  # Allow admin to control this bot
    validity = db.Column(db.DateTime, nullable=True)  # Validity datetime for bot assignment
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    behaviour = db.relationship('BotBehaviour', backref='user_bot', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, decrypt_bot_id=False):
        from utils.encryption import decrypt_bot_id as decrypt
        bot_id_decrypted = None
        if decrypt_bot_id:
            try:
                bot_id_decrypted = decrypt(self.bot_id)
            except Exception as e:
                # Handle decryption errors gracefully
                print(f"Warning: Failed to decrypt bot_id for assign_id {self.assign_id}: {str(e)}")
                bot_id_decrypted = "[Decryption Failed]"
        data = {
            'assign_id': self.assign_id,
            'user_id': self.user_id,
            'bot_id': bot_id_decrypted,
            'allow_admin_control': self.allow_admin_control,
            'validity': self.validity.isoformat() if self.validity else None,
            'is_active': self.is_active,
            'created_on': self.created_on.isoformat() if self.created_on else None,
            'updated_on': self.updated_on.isoformat() if self.updated_on else None
        }
        return data

class BotBehaviour(db.Model):
    __tablename__ = 'bots_behaviour'
    
    bot_behav_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assign_id = db.Column(db.Integer, db.ForeignKey('user_bot.assign_id', ondelete='CASCADE'), nullable=False, unique=True)
    bot_state = db.Column(db.Boolean, default=False, nullable=False)
    hard_stop_all_trades = db.Column(db.Boolean, default=False, nullable=False)
    listen_to_common_commander = db.Column(db.Boolean, default=False, nullable=False)
    news_based_start_stop = db.Column(db.Boolean, default=False, nullable=False)
    refresh_data_from_bot = db.Column(db.Boolean, default=False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def to_dict(self):
        return {
            'bot_behav_id': self.bot_behav_id,
            'assign_id': self.assign_id,
            'bot_state': self.bot_state,
            'hard_stop_all_trades': self.hard_stop_all_trades,
            'listen_to_common_commander': self.listen_to_common_commander,
            'news_based_start_stop': self.news_based_start_stop,
            'refresh_data_from_bot': self.refresh_data_from_bot,
            'created_on': self.created_on.isoformat() if self.created_on else None,
            'updated_on': self.updated_on.isoformat() if self.updated_on else None,
            'is_active': self.is_active
        }

