# services/chef_service.py
from typing import List, Dict
from services.recipe_finder import RecipeFinder

class ChefService:
    def __init__(self):
        self.recipe_finder = RecipeFinder()
        print("ChefService initialized.")
        
    def get_recipe_suggestions(self, user_prompt: str) -> List[Dict]:
        print(f"User prompt: {user_prompt}")  # Debug: Log the user prompt
        suggestions = self.recipe_finder.find_similar_recipes(user_prompt)
        return suggestions

