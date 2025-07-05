from flask import Flask
from flask_cors import CORS
from app.webhook.routes import webhook_bp
from app.api.routes import api_bp
from app.logging_config import setup_logging, get_logger
from app.middleware import log_request_start, log_request_end, log_request_error

def create_app():
    # Setup logging first
    setup_logging()
    logger = get_logger('app')
    
    logger.info("Starting Flask application initialization")
    
    app = Flask(__name__)
    CORS(app)
    
    # Register middleware for request logging
    app.before_request(log_request_start)
    app.after_request(log_request_end)
    app.errorhandler(Exception)(log_request_error)
    
    # Register blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(api_bp)
    
    logger.info("Flask application initialized successfully")
    logger.info(f"Registered blueprints: {[bp.name for bp in app.blueprints.values()]}")
    
    return app

if __name__ == '__main__':
    logger = get_logger('app')
    logger.info("Starting GitHub Webhook Application")
    
    app = create_app()
    
    logger.info("Starting Flask development server on 0.0.0.0:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
