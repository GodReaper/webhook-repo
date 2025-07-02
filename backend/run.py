from flask import Flask
from flask_cors import CORS
from app.webhook.routes import webhook_bp
from app.api.routes import api_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(api_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
