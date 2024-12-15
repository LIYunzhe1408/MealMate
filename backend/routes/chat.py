import logging
from flask import Blueprint, request, jsonify
from services.chef_service import ChefService
from services.intent_classifier import IntentClassifier
from services.line_cook_service import LineCookService
# from transformers import pipeline
import openai
import os

# Configure logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("fsspec").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


chat_bp = Blueprint('chat', __name__)

# Initialize services
chef_service = ChefService()
intent_classifier = IntentClassifier()

openai.api_key = os.getenv("OPENAI_API_KEY")

# lightweight model from huggingface, mighe be useful to replace the openai model
# chat_model = pipeline("text-generation", model="")

@chat_bp.route('/chat', methods=['POST'])
def handle_chat():
    logger.debug("Received request to /chat")
    data = request.json

    try: 
        user_message = data.get('message', '')
        logger.debug(f"User message: {user_message}")
        
        # Step 1: Classify intent
        intent = intent_classifier.classify(user_message)
        
        logger.debug(f"Intent: {intent}")
        if intent == "recipe-related":
            # Step 2: Get recipe suggestions for recipe-related queries
            recipe = chef_service.get_recipe_suggestions(user_message)
            # print(" RECIPE!!!!!!!!!!!!!!!!!!! ", recipe)
            chosen_recipe = {
            recipe[0]['title']: recipe[0]['ingredients']
        }
            print(chosen_recipe)
            response = {
                'type': 'recipe',
                'recipe': recipe,
                'message': "Here are the top recipes matching your query!"
            }
        else:
            # Step 3: Use OpenAI for non-recipe-related queries
            completion = openai.chat.completions.create(
                model="gpt-4o-mini",  # You can use "gpt-3.5-turbo" for cost efficiency
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            gpt_response = completion.choices[0].message.content
            logger.debug(f"GPT-4 response: {gpt_response}")
            response = {
                'type': 'general',
                'message': gpt_response
            }
        logging.debug(f"Response to frontend: {response}")
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error handling chat request: {str(e)}", exc_info=True)
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
