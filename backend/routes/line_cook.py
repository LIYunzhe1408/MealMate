import json
from flask import Blueprint, jsonify, request
from services.line_cook_service import LineCookService

line_cook_bp = Blueprint('line_cook', __name__)

# Initialize LineCookService
# line_cook_service = LineCookService(database_path="/Users/emil/Library/Mobile Documents/com~apple~CloudDocs/Documents/projects/anything/sampled_food.csv")

@line_cook_bp.route('/line-cook', methods=['POST'])
def line_cook():
    try:
        # Parse the JSON payload
        data = request.get_json()
        recipe = data.get('recipe', {})

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

        return jsonify({
            "message": "Recipe saved successfully.",
            "recipe": recipe
        }), 200

    except Exception as e:
        print(f"Error in /line-cook: {str(e)}")
        return jsonify({"error": str(e)}), 500
