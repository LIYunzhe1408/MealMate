# services/chef_service.py
from typing import List, Dict
from services.recipe_finder import RecipeFinder
from datasets import load_dataset
import numpy as np

class ChefService:
    def __init__(self):
        self.recipe_finder = RecipeFinder()
        print("Loading Sentence Transformer model...")
        
    def get_recipe_suggestions(self, user_prompt: str) -> List[Dict]:
        return self.recipe_finder.find_similar_recipes(user_prompt)

