import logging
import json
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

line_cook_bp = Blueprint('line_cook', __name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize LineCookService
line_cook_service = LineCookService(database_path="/Users/emil/Library/Mobile Documents/com~apple~CloudDocs/Documents/projects/anything/sampled_food.csv")

@line_cook_bp.route('/line-cook', methods=['POST'])
def line_cook():
    try:
        print("HANDLE Line Cook 1")
        # Parse the JSON payload
        data = request.get_json()
        recipe = data.get('recipe', {})
        print("recipe!!!!!", recipe)

        # Validate the payload
        if not recipe or 'title' not in recipe or 'ingredients' not in recipe:
            return jsonify({"error": "Invalid payload. 'recipe' must contain 'title' and 'ingredients'."}), 400

        # Ensure ingredients is a list
        ingredients = recipe.get('ingredients')
        if isinstance(ingredients, str):
            # Convert string to list by splitting on semicolons
            ingredients = [item.strip() for item in ingredients.split(";")]
        elif not isinstance(ingredients, list):
            return jsonify({"error": "'ingredients' must be a list or a semicolon-separated string."}), 400

        recipe['ingredients'] = ingredients  # Save normalized ingredients as a list

        # Save the recipe to a JSON file
        file_path = 'saved_recipes.json'
        try:
            # Load existing data if the file exists
            with open(file_path, 'r', encoding='utf-8') as file:
                recipes = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            recipes = []

        # Add the new recipe
        recipes.append(recipe)

        # Write back to the file with readable Unicode characters
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(recipes, file, indent=4, ensure_ascii=False)
        
        # search_for_ingreds on the recipe
        # best_matches, mapped_ingredients = line_cook_service.search_for_ingreds(recipe)


        # Return the response
        # return jsonify({
        #     "type": "ingredients",
        #     "message": "Recipe saved successfully.",
        #     "recipe": recipe,
        #     "best_matches": best_matches,
        #     "mapped_ingredients": mapped_ingredients
        # }), 200
        recipe = [recipe]


        return jsonify({
            "type": "ingredients",
            "recipe": recipe
        }), 200

    except Exception as e:
        print(f"Error in /line-cook: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    # print("HANDLE CHAT")
    # logger.debug("Received request to /line-cook")
    # data = request.json

    # try: 
    #     user_message = data.get('message', '')
    #     logger.debug(f"User message: {user_message}")
        
    
        
    #     logger.debug(f"Intent: {intent}")
    #     if intent == "recipe-related":
    #         # Step 2: Get recipe suggestions for recipe-related queries
    #         recipe = chef_service.get_recipe_suggestions(user_message)
    #         print(" RECIPE!!!!!!!!!!!!!!!!!!! ", recipe)
    #         chosen_recipe = {
    #         recipe[0]['title']: recipe[0]['ingredients']
    #     }
    #         print(chosen_recipe)
    #         response = {
    #             'type': 'recipe',
    #             'recipe': recipe,
    #             'message': "Here are the top recipes matching your query!"
    #         }
    #     else:
    #         # Step 3: Use OpenAI for non-recipe-related queries
    #         completion = openai.ChatCompletion.create(
    #             model="gpt-4o-mini",  # You can use "gpt-3.5-turbo" for cost efficiency
    #             messages=[
    #                 {"role": "system", "content": "You are a helpful assistant."},
    #                 {"role": "user", "content": user_message}
    #             ]
    #         )
    #         gpt_response = completion["choices"][0]["message"]["content"]
    #         logger.debug(f"GPT-4 response: {gpt_response}")
    #         response = {
    #             'type': 'general',
    #             'message': gpt_response
    #         }
    #     logging.debug(f"Response to frontend: {response}")
    #     return jsonify(response), 200

    # except Exception as e:
    #     logging.error(f"Error handling chat request: {str(e)}", exc_info=True)
    #     return jsonify({'error': str(e)}), 500
