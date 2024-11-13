from flask import Blueprint, request, jsonify
from services.chef_service import get_recipe
from services.line_cook_service import check_availability

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    user_message = data.get('message')
    
    try:
        # Get recipe from Chef de Cuisine
        recipe = get_recipe(user_message)
        
        # Check availability with Line Cook
        available_ingredients = check_availability(recipe)
        
        response = {
            'recipe': recipe,
            'available_ingredients': available_ingredients,
            'message': "Here's what I found for you!"
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500