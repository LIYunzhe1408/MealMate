from flask import Blueprint, request, jsonify
from services.chef_service import get_recipe_suggestions
# from services.line_cook_service import check_availability
from services.chef_service import ChefService

chat_bp = Blueprint('chat', __name__)
chef_service = ChefService()

@chat_bp.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    user_message = data.get('message')
    
    try:
        # Get recipe from Chef de Cuisine
        recipe = get_recipe_suggestions(user_message)
        
        # Check availability with Line Cook
        # available_ingredients = check_availability(recipe)
        
        response = {
            'recipe': recipe,
            # 'available_ingredients': available_ingredients,
            'message': "Here's what I found for you!"
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/suggest-recipes', methods=['POST'])
def suggest_recipes():
    data = request.json
    user_prompt = data.get('message')
    
    try:
        suggestions = chef_service.get_recipe_suggestions(user_prompt)
        return jsonify({
            'suggestions': suggestions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@chat_bp.route('/test-message', methods=['POST'])
def test_message():
    data = request.json
    user_message = data.get('message')
    
    return jsonify({
        'received_message': user_message,
        'response': "Message received successfully!"
    }), 200