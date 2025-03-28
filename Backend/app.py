from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
import logging

from extensions import db, bcrypt  # Import from extensions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with the app
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt.init_app(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models and routes AFTER initializing extensions
from models import User, Product, Order
import routes

@app.route("/")
def home():
    return {"message": "Welcome to the Warehouse Management System API"}

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return {"error": "Internal server error"}, 500

if __name__ == '__main__':
    logger.info("Starting the Warehouse Management System backend...")
    app.run(debug=True)
