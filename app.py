import os
import logging
from flask import Flask, send_from_directory
from config import config
from database import init_db
from routes.api import api_bp

def create_app(config_name='default'):
    """Application factory for creating the Flask app instance."""
    app = Flask(__name__, static_folder='static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Configure Logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
    
    # Ensure upload folder exists with proper permissions
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Serve static frontend
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory(app.static_folder, path)
    
    return app

if __name__ == '__main__':
    # Determine environment
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    
    print("=" * 60)
    print(f"AI Resume Skill Gap Detection System - {env.upper()} MODE")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000)
