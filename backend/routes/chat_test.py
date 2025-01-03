from flask import Blueprint, request, jsonify
from services.chef_service import ChefService

chat_bp = Blueprint('chat', __name__)
chef_service = ChefService()

@chat_bp.route('/test-message', methods=['POST'])
def test_message():
    data = request.json
    user_message = data.get('message')
    
    return jsonify({
        'received_message': user_message,
        'response': "Message received successfully!"
    }), 200