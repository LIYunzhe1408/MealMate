from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import openai
import ast
import os 
import numpy as np
import csv
from typing import Dict, List, Any

# OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
# openai.api_key = OPENAI_API_KEY
# if not openai.api_key:
#     raise ValueError("API key not found. Please set OPENAI_API_KEY environment variable or pass it directly.")
# #openai.api_key = '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'



# database = pd.read_csv('/Users/emil/Library/Mobile Documents/com~apple~CloudDocs/Documents/projects/anything/GroceryDataset.csv')
# unique_sub_categories = database['Sub Category'].unique().tolist()
# grocery_names = database['Title'].tolist()
# embeddings_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
# grocery_products_embeddings = embeddings_model.encode(grocery_names)



# database = pd.read_csv('sampled_food.csv')
# grocery_names = database['description'].tolist()
# embeddings_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
# grocery_products_embeddings = embeddings_model.encode(grocery_names)

class LineCookService:
    def __init__(self, database_path: str, embeddings_model_name: str = 'paraphrase-MiniLM-L6-v2', n_products: int = 5):
        # self.OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        # openai.api_key = self.OPENAI_API_KEY
        # if not openai.api_key:
        #     raise ValueError("API key not found. Please set OPENAI_API_KEY environment variable or pass it directly.")
        

        self.n_products = n_products

        # Load the database
        self.database = pd.read_csv(database_path)
        self.grocery_names = self.database['description'].tolist()

        # Load embeddings model
        self.embeddings_model = SentenceTransformer(embeddings_model_name)
        self.grocery_products_embeddings = self.embeddings_model.encode(self.grocery_names)


    def get_llm_response(self, prompt: str) -> str:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    
    def get_similarity_scores(self, general_ingredient: str, n: int = None) -> pd.DataFrame:
        if n is None:
            n = self.n_products
        general_ingredient_embedding = self.embeddings_model.encode(general_ingredient).reshape(1, -1)
        similarity_scores = cosine_similarity(self.grocery_products_embeddings, general_ingredient_embedding).flatten()

        similarity_df = pd.DataFrame({'Category Name': self.grocery_names, 'Similarity Score': similarity_scores})
        similarity_df = similarity_df.sort_values(by='Similarity Score', ascending=False)
        return similarity_df.head(n)
    

    def LLM_find_best_match(self, closest_ingredients: List[str], specific_ingredient: str, recipe: Dict[str, List[str]]) -> str:
        prompt = f"""I am going to make the recipe {recipe}. I have automated a search through a store's database and have found the 5 closest igredients to {specific_ingredient}: {closest_ingredients}.
    Your job is to find out if any of the ingredients, {closest_ingredients} match the ingredient I am looking for: {specific_ingredient}. The ingredients do not have to match exacty,
    but it has to work in the recipe I provided. That means that synonyms or similar ingredients are also valid, as long as they work in the recipe. However, be careful and use your knowledge
    about food. Just because two ingredients have similar names, does not mean they work in the same recipe.
    If one or more of the ingredients matches the ingredient I am looking for, output the ingredient that matches best. If none of the ingredients match, please write 'None'.
    Only output either the closest ingredient or 'None'."""
        best_match = self.get_llm_response(prompt)
        return best_match
    
    def LLM_remove_basic_ingredients(self, recipe: Dict[str, List[str]]) -> Dict[str, List[str]]:
        prompt = f"""I am looking at ingredient availability in a store for the ingredients in this recipe: {recipe}. I am assuming that the user has the basic ingredients. Your job is to
    remove all the basic ingredients in the recipe. The recipe you write should look exactly as the one I gave you, just that the basic ingredients are removed. Examples of basic ingredients are 'salt', 'pepper', 'Olive Oil', 'Sugar', but 
    many more exists. 
    The output should only be a dictionary with the key as the name of the recipe and the values as the remaining ingredients, written exactly as in the recipe I provided you, aslo included the amount of each ingredient.
    Your answer should contain nothing else."""
        remaining_recipe = self.get_llm_response(prompt)
        remaining_recipe = ast.literal_eval(remaining_recipe)
        return remaining_recipe
        

    
    def LLM_suggest_replacements(self, recipe: Dict[str, List[str]], unavail_ingred: str) -> str:
        prompt = f"""I am looking at ingredient availability in a store for the ingredients in this recipe: {recipe}. I have found that the following ingredient is not available: {unavail_ingred}.
    Your job is to suggest an action. There are 2 possibilites:
    1. If the ingredient is essential in the recipe, you suggest to "Remove ingredient".
    2. If the ingredient is essential in the recipe, and the dish would not be the same if you swap it with something else, you suggest to "Remove dish".
    If you choose 1, simply write: Remove ingredient. If you choose 2, simply write: Remove dish. You should not write anythng else
    in your response."""
        replacements = self.get_llm_response(prompt)
        return replacements
    

    def search_for_ingreds(self, recipe: Dict[str, List[str]]):
        remove_dish = False
        filtered_recipe = self.LLM_remove_basic_ingredients(recipe)

        recipe_ingredients = [item for sublist in recipe.values() for item in sublist]
        filtered_ingredients = [item for sublist in filtered_recipe.values() for item in sublist]
        basic_ingreds = [item for item in recipe_ingredients if item not in filtered_ingredients]

        best_matches = {}
        mapped_ingredients = {}

        # Mark basic ingredients
        for ingredient in basic_ingreds:
            best_matches[ingredient] = 'Basic Ingredient, assumes customer has it'
            mapped_ingredients[ingredient] = ['Basic Ingredient']

        filtered_ingredients_list = list(filtered_recipe.values())[0] 
        for ingredient in filtered_ingredients_list:
            similarity_scores = self.get_similarity_scores(ingredient, self.n_products)
            mapped_ingredients[ingredient] = similarity_scores["Category Name"].tolist()
            best_match = self.LLM_find_best_match(similarity_scores["Category Name"].tolist(), ingredient, recipe)
            best_matches[ingredient] = best_match

        # Handle 'None' matches
        keys = list(best_matches.keys())
        for key in keys:
            if best_matches[key] == 'None':
                print(key)
                action = self.LLM_suggest_replacements(recipe, key)
                print(action)
                if action == 'Remove ingredient.':
                    print(f'Removing: {key}')
                    best_matches[key] = 'None, remove ingredient'
                elif action == 'Remove dish.':
                    best_matches[key] = 'None, remove dish'
                    print(f'Removing dish')

        return best_matches, mapped_ingredients

    def write_to_csv(self, best_matches: Dict[str, Any], mapped_ingredients: Dict[str, List[str]], output_file: str):
        keys = best_matches.keys()
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Ingredient", "Output embeddings model", "Best matches from LLM"])
            for key in keys:
                writer.writerow([key, ', '.join(mapped_ingredients[key]), best_matches[key]])
