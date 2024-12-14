import logging
import json
from flask import Blueprint, request, jsonify
from services.chef_service import ChefService
from services.intent_classifier import IntentClassifier
from services.line_cook_service import LineCookService
# from transformers import pipeline
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
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sampled_food.csv')

# Resolve the path to its absolute form for clarity (optional, for debugging purposes)
absolute_path = os.path.abspath(file_path)
print(f"Resolved file path: {absolute_path}")

# Initialize LineCookService
line_cook_service = LineCookService(database_path=absolute_path)

@line_cook_bp.route('/line-cook', methods=['POST'])
def line_cook():
    try:
        
        # Parse the JSON payload
        data = request.get_json()
        recipe = data.get('recipe', {})
        
        # recipe looks like this: {'title': 'Homemade Pasta without a Pasta Machine', 'ingredients': ['2\u2009½ cups Italian-style tipo 00 flour, plus additional for dusting ', ' 3 large eggs ', ' 1 pinch salt ', ' 1 tablespoon water, or as needed']}

        key = recipe['title']
        value = recipe['ingredients']
        recipe = {key: value}
        # print("RECIPEEEEEE: ", recipe)

        best_matches, mapped_ingredients = line_cook_service.search_for_ingreds(recipe)

        print("BEST MATCHES: ", best_matches), print("MAPPED INGREDIENTS: ", mapped_ingredients)


        # Return the response
        return jsonify({
            "type": "ingredients",
            "message": "Recipe saved successfully.",
            "best_matches": best_matches,
            "mapped_ingredients": mapped_ingredients
        }), 200

    except Exception as e:
        print(f"Error in /line-cook: {str(e)}")
        return jsonify({"error": str(e)}), 500