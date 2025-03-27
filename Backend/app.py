from flask import Flask
from config import Config
from models import db, bcrypt
from routes.auth import auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(auth)
    
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
