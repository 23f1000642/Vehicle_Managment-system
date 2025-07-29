from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
import redis
from celery import Celery

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Enable CORS for Vue.js frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Redis connection
    try:
        app.redis = redis.from_url(app.config['REDIS_URL'])
        app.redis.ping()  # Test connection
        print("✅ Redis connected successfully")
    except:
        print("⚠️ Redis connection failed - caching will be disabled")
        app.redis = None
    
    # Register blueprints (we'll create these later)
    # Register blueprints
    # Register blueprints
    from app.auth import auth_bp
    from app.parking import parking_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(parking_bp, url_prefix='/api/parking')
   
    # from app.routes import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

def create_admin_user():
    """Create admin user if it doesn't exist"""
    from app.models import User
    from app.config import Config
    import bcrypt
    
    admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first()
    if not admin:
        hashed_password = bcrypt.hashpw(
            Config.ADMIN_PASSWORD.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        admin = User(
            username=Config.ADMIN_USERNAME,
            email='admin@parking.com',
            password=hashed_password,
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin user created: {Config.ADMIN_USERNAME}")

def make_celery(app):
    """Create Celery instance for background jobs"""
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery