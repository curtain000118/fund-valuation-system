"""
Flask应用初始化
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
        
        if os.environ.get('VERCEL_ENV'):
            config_name = 'vercel'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app
