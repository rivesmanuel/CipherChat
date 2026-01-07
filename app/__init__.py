from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    with app.app_context():
        from app.models import Conversacion

    from app.api.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    @app.route('/')
    @app.route('/inicio')
    def inicio():
        return render_template('chat.html')

    return app