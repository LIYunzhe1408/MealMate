import logging
import json
from flask import Blueprint, request, jsonify
from services.line_cook_service import LineCookService
import openai
from dotenv import load_dotenv
import os
import copy

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


if not openai.api_key:
    raise ValueError("API key not found. Please set OPENAI_API_KEY in the environment.")

# Configure logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("fsspec").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

line_cook_bp = Blueprint('line_cook', __name__)
# OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# Assuming this code is in `services/line_cook_service.py`
file_paths = [
                os.path.join(os.path.dirname(__file__), '..', 'data', 'grocery_names_prices_safeway.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'data', 'grocery_names_prices_target.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'data', 'grocery_names_prices_trader_joes.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'data', 'grocery_names_prices_walmart.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'data', 'grocery_names_prices_whole_foods.csv')
                ]

# Resolve the path to its absolute form for clarity (optional, for debugging purposes)
absolute_paths = [os.path.abspath(file_paths[0]), os.path.abspath(file_paths[1]), os.path.abspath(file_paths[2]), os.path.abspath(file_paths[3]), os.path.abspath(file_paths[4])]
print(f"Resolved file path: {absolute_paths}")

# Initialize LineCookService
line_cook_service = LineCookService(database_paths=absolute_paths)


@line_cook_bp.route('/line-cook', methods=['POST'])
def line_cook():
    try:
        # Parse the JSON payload
        data = request.get_json()
        recipe = data.get('recipe', {})
        preferences = data.get('preferences', {})
        price_preference = preferences.get('pricePreference')

        print(f"Budget preference received in back end: {price_preference}")

        key = recipe['title']
        value = recipe['ingredients']
        recipe = {key: value}
        unavailable_ingredients = set()

        for i in range(5):
            store = "None"
            look_in_new_store = False
            recipe_copy = copy.deepcopy(recipe)
            print(f'Recipe_copy: {recipe_copy}')
            best_matches, mapped_ingredients, formatted_output = line_cook_service.search_for_ingreds(
                recipe_copy, i, int(price_preference))

            # Check if any ingredient is unavailable
            for ingredient, match in best_matches.items():
                if match == 'None, remove dish':
                    unavailable_ingredients.add(ingredient)
                    look_in_new_store = True

            if not unavailable_ingredients:  # If no unavailable ingredients, stop searching
                if i == 0:
                    store = "Safeway"
                elif i == 1:
                    store = "Target"
                elif i == 2:
                    store = "Trader Joe's"
                elif i == 3:
                    store = "Walmart"
                elif i == 4:
                    store = "Whole Foods"
                break

        # If there are unavailable ingredients, return a fun message
        if unavailable_ingredients:
            unavailable_message = (
                "Uh-oh! 🚫 It looks like we couldn't find some key ingredients in your local stores: "
                f"{', '.join(unavailable_ingredients)}. Maybe it’s time to unleash your inner chef and try a different dish 🍳!"
            )
            
            print(f"Unavailable ingredients: {unavailable_ingredients}")
            print(f"Unavailable message: {unavailable_message}")
            return jsonify({
                "type": "unavailable_message",
                "unavailable_message": unavailable_message,
                "mapped_ingredients": mapped_ingredients,
                "store": store,
                "formatted_output": formatted_output,
                "recipe": recipe
            }), 200

        # Return success response if all ingredients are found
        return jsonify({
            "type": "ingredients",
            "message": "Recipe ingredients successfully matched!",
            "best_matches": best_matches,
            "mapped_ingredients": mapped_ingredients,
            "store": store,
            "formatted_output": formatted_output,
            "recipe": recipe
        }), 200

    except Exception as e:
        print(f"Error in /line-cook: {str(e)}")
        return jsonify({"error": str(e)}), 500
