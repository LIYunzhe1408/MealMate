from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from routes.cart import cart_bp
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)