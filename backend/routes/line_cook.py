import logging
import json
from flask import Blueprint, request, jsonify
from services.line_cook_service import LineCookService
import openai
from dotenv import load_dotenv
import os

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

@line_cook_bp.route('/set-budget', methods=['POST'])
def set_budget():
    global BUDGET_PREFERENCE
    data = request.get_json()
    BUDGET_PREFERENCE = data.get('budgetPreference', 3)  # Default to 3
    print(f"Budget preference set to: {BUDGET_PREFERENCE}")
    return jsonify({"message": "Budget preference saved", "budgetPreference": BUDGET_PREFERENCE}), 200

@line_cook_bp.route('/line-cook', methods=['POST'])
def line_cook():
    try:
        global BUDGET_PREFERENCE
        print(f"Using budget preference: {BUDGET_PREFERENCE}")
        # Parse the JSON payload
        data = request.get_json()
        recipe = data.get('recipe', {})
        
        # recipe looks like this: {'title': 'Homemade Pasta without a Pasta Machine', 'ingredients': ['2\u2009½ cups Italian-style tipo 00 flour, plus additional for dusting ', ' 3 large eggs ', ' 1 pinch salt ', ' 1 tablespoon water, or as needed']}

        key = recipe['title']
        value = recipe['ingredients']
        recipe = {key: value}
        for i in range(5):
            store = "None"
            look_in_new_store = False
            best_matches, mapped_ingredients, formatted_output = line_cook_service.search_for_ingreds(recipe, i, BUDGET_PREFERENCE)
            print
            for key, value in best_matches.items():
                if value == 'None, remove dish':
                    look_in_new_store = True
            if not look_in_new_store:
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

        print("BEST MATCHES: ", best_matches), print("MAPPED INGREDIENTS: ", mapped_ingredients), print("STORE: ", store), print("FORMATTED OUTPUT: ", formatted_output), print("RECIPE: ", recipe)


        # Return the response
        return jsonify({
            "type": "ingredients",
            "message": "Recipe saved successfully.",
            "best_matches": best_matches,
            "mapped_ingredients": mapped_ingredients,
            "store": store,
            "formatted_output": formatted_output,
            "recipe": recipe
        }), 200

    except Exception as e:
        print(f"Error in /line-cook: {str(e)}")
        return jsonify({"error": str(e)}), 500