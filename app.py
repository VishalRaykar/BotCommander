from flask import Flask, render_template, send_from_directory, redirect, session
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.users import users_bp
from routes.bots import bots_bp
from utils.auth import require_login, is_admin

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(bots_bp)
    
    # Frontend routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/bot/<int:assign_id>')
    def bot_details(assign_id):
        return render_template('bot_details.html', assign_id=assign_id)
    
    @app.route('/admin')
    def admin():
        if 'user_id' not in session:
            return redirect('/')
        if not is_admin():
            return redirect('/dashboard')
        return render_template('admin.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print("✓ Database connection successful!")
            print("✓ Tables created/verified")
        except Exception as e:
            print("✗ Database connection error:")
            print(f"  {str(e)}")
            print("\nPlease check:")
            print("  1. MySQL server is running")
            print("  2. Database credentials in .env file are correct")
            print("  3. Database 'bot_commander' exists")
            print("  4. MySQL port is correct (standard is 3306)")
            import sys
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("BotCommander is starting...")
    print("=" * 60)
    print(f"Access the application at: http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

