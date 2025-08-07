from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from mongoengine import connect

from app.documents import User
import os

app = Flask(__name__)
app.secret_key = os.environ["AUCTIONMAN_SECRET_KEY"]
# app.config.from_object(Config)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# MongoEngine setup
connect('cexytime', host='mongodb://localhost:27017/', tz_aware=True)  # Update with your MongoDB URI

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

# Import routes and error handlers
from app import routes

print(app.url_map)
