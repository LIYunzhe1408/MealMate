import logging
from flask import Blueprint, request, jsonify
from services.chef_service import ChefService
from services.intent_classifier import IntentClassifier
from services.line_cook_service import LineCookService
# from transformers import pipeline
import openai
import os
import json


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
        preferences = data.get('preferences', {})
        price_preference = preferences.get('pricePreference')
        allergies = preferences.get('allergies')

        print(f"price preference: {price_preference} received in backend")
        print(f"allergies: {allergies} received in backend")

        logger.debug(f"User message: {user_message}")

        # Step 1: Classify intent
        intent = intent_classifier.classify(user_message)

        logger.debug(f"Intent: {intent}")
        if intent == "recipe-related":
            # Step 2: Using LLM to get recipe suggestions for recipe-related queries.
            prompt = (
                "You are an expert chef. You will be given a query from a user who wants to find a dish. "
                "The prompt can be vague or specific. "
                "Your task is to find 3 dishes that best match the user's query. "
                "For each dish, provide a title and a list of ingredients. "
                "The user has these allergies: {allergies}. "
                "If there are no allergies, do not suggest allergy-free or substitute ingredients. For example, if there is no gluten allergy, do not suggest gluten-free buns. "
                "If there are specified allergies, you must strictly avoid all ingredients that contain those allergens. "
                "For example if the user has a gluten allergy and wants a hamburger recipe, replace the hamburger buns with gluten-free hamburgern buns. "
                
                "Your final answer must be exactly a JSON array with 3 objects. Each object should have the keys 'title' and 'ingredients'. "
                "The 'ingredients' value should be a single string where each ingredient is separated by a semicolon (';'). "
                "The final format should be exactly: "
                "[{'title': '<Dish 1 title>', 'ingredients': '<Dish 1 ingredients>'}, "
                "{'title': '<Dish 2 title>', 'ingredients': '<Dish 2 ingredients>'}, "
                "{'title': '<Dish 3 title>', 'ingredients': '<Dish 3 ingredients>'}] "
                "Do not include any commentary, instructions, or additional text outside this JSON array."
            )


            completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            gpt_response = completion.choices[0].message.content
            logger.debug(f"GPT-4 recipe response: {gpt_response}")

            try:
                # Safely parse the GPT response as JSON
                formatted_response = gpt_response.replace("'", '"')
                recipe = json.loads(formatted_response)
                response = {
                    'type': 'recipe',
                    'recipe': recipe,
                    'message': "Here are the top recipes matching your query!"
                }
            except Exception as parse_error:
                logger.error(f"Error parsing GPT response: {str(parse_error)}")
                logger.error(f"GPT response: {gpt_response}")
                return jsonify({'error': 'Failed to parse recipe data.'}), 500

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
