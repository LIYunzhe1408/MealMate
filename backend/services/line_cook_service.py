from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import openai
import ast
import os
import numpy as np
import csv
from typing import Dict, List, Any
from utils.data_processor import produce_matched_ingredient_for_cart


class LineCookService:
    def __init__(self, database_paths: str, embeddings_model_name: str = 'paraphrase-MiniLM-L6-v2', n_products: int = 10):

        self.n_products = n_products
        self.embeddings_paths = [os.path.join(
            os.path.dirname(database_paths[0]),
            "grocery_embeddings_safeway.npy"
        ),
            os.path.join(
            os.path.dirname(database_paths[1]),
            "grocery_embeddings_target.npy"
        ),
            os.path.join(
            os.path.dirname(database_paths[2]),
            "grocery_embeddings_trader_joes.npy"
        ),
            os.path.join(
            os.path.dirname(database_paths[3]),
            "grocery_embeddings_walmart.npy"
        ),
            os.path.join(
            os.path.dirname(database_paths[4]),
            "grocery_embeddings_whole_foodst.npy"
        ),
        ]

        self.database_paths = database_paths
        print(f"Database paths: {database_paths}")
        # Load the database
        self.database = [pd.read_csv(database_paths[0]), pd.read_csv(database_paths[1]), pd.read_csv(
            database_paths[2]), pd.read_csv(database_paths[3]), pd.read_csv(database_paths[4])]
        self.grocery_names = [self.database[0]['PRODUCT_NAME'].tolist(), self.database[1]['PRODUCT_NAME'].tolist(
        ), self.database[2]['PRODUCT_NAME'].tolist(), self.database[3]['PRODUCT_NAME'].tolist(), self.database[4]['PRODUCT_NAME'].tolist()]
        self.grocery_prices = [self.database[0]['PRICE_CURRENT'].tolist(), self.database[1]['PRICE_CURRENT'].tolist(
        ), self.database[2]['PRICE_CURRENT'].tolist(), self.database[3]['PRICE_CURRENT'].tolist(), self.database[4]['PRICE_CURRENT'].tolist()]
        # Load embeddings model
        print("Loading embeddings model...")
        self.embeddings_model = SentenceTransformer(embeddings_model_name)
        print("Model loaded.")

        # Load or create embeddings
        self.grocery_products_embeddings = self._load_or_create_embeddings()

    def _load_or_create_embeddings(self):
        """
        Loads embeddings from a .npy file or creates and saves them if not found.
        """
        if os.path.exists(self.embeddings_paths[0]) & os.path.exists(self.embeddings_paths[1]) & os.path.exists(self.embeddings_paths[2]) & os.path.exists(self.embeddings_paths[3]) & os.path.exists(self.embeddings_paths[4]):
            print("Loading precomputed embeddings...")
            embeddings = [np.load(self.embeddings_paths[0]), np.load(self.embeddings_paths[1]), np.load(
                self.embeddings_paths[2]), np.load(self.embeddings_paths[3]), np.load(self.embeddings_paths[4])]
            print(f"Embeddings shape: {embeddings[0].shape}")
            return embeddings
        else:
            print("No precomputed embeddings found. Creating embeddings...")
            embeddings = [self.embeddings_model.encode(self.grocery_names[0], show_progress_bar=True), self.embeddings_model.encode(self.grocery_names[1], show_progress_bar=True), self.embeddings_model.encode(
                self.grocery_names[2], show_progress_bar=True), self.embeddings_model.encode(self.grocery_names[3], show_progress_bar=True), self.embeddings_model.encode(self.grocery_names[4], show_progress_bar=True)]
            for i in range(5):
                os.makedirs(os.path.dirname(
                    self.embeddings_paths[i]), exist_ok=True)
                np.save(self.embeddings_paths[i], embeddings[i])
                print(f"Embeddings saved to {self.embeddings_paths[i]}")

            return embeddings

    def get_llm_response(self, prompt: str) -> str:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def get_similarity_scores(self, general_ingredient: str, store_num: int, n: int = None) -> pd.DataFrame:
        if n is None:
            n = self.n_products
        general_ingredient_embedding = self.embeddings_model.encode(
            general_ingredient).reshape(1, -1)
        similarity_scores = cosine_similarity(
            self.grocery_products_embeddings[store_num], general_ingredient_embedding).flatten()
        similarity_df = pd.DataFrame(
            {'Category Name': self.grocery_names[store_num], 'Prices': self.grocery_prices[store_num], 'Similarity Score': similarity_scores})
        similarity_df = similarity_df.sort_values(
            by='Similarity Score', ascending=False)
        return similarity_df.head(n)


    def LLM_find_matches(self, closest_ingredients: List[str], specific_ingredient: str, recipe: Dict[str, List[str]]) -> List[str]:
        prompt = f"""I am going to make the recipe {recipe}. I have automated a search through a store's database and have found the 5 closest ingredients to {specific_ingredient}: {closest_ingredients}.
    Your job is to find out if any of the ingredients, {closest_ingredients} match the ingredient I am looking for: {specific_ingredient}. The ingredients do not have to match exactly,
    but it has to work in the recipe I provided. That means that synonyms or similar ingredients are also valid, as long as they work in the recipe. However, be careful and use your knowledge
    about food. Just because two ingredients have similar names, does not mean they work in the same recipe. For example: Strawberry flavored ice cream can not replace strawberries in a recipe. Output all ingredients that match the ingredient I am looking for.
    If none of the ingredients match, please write 'None'.
    Only output either the matching ingredient(s) or 'None'.
    The format for the output should be a list of strings, where each string is a specific ingredient found here: {closest_ingredients} that matches the ingredient I am looking for."""
        matches = self.get_llm_response(prompt)

        if matches == 'None':
            return []
        else:
            return ast.literal_eval(matches)

    def LLM_remove_basic_ingredients(self, recipe: Dict[str, List[str]]) -> Dict[str, List[str]]:
        prompt = f""" Given the following recipe: {recipe} Assume the user already has access to basic ingredients. Example of basic ingredients are salt, pepper, olive oil, sugar, water etc. 
        Use your knowledge to identify other commonly considered basic ingredients. By basic ingredients I mean everything you can expect someone to have at home, so that it is not necessary
        to buy it in the store for the recipe.
        Remove all these basic ingredients from the recipe. The edited recipe should maintain the exact structure and wording of the original, but without the basic ingredients. Your response
        should be a dictionary where: - The key is the name of the recipe. - The value is the list of remaining ingredients, each with its corresponding amount exactly as stated in the original recipe.
        Only return the dictionary and nothing else. """
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

    def search_for_ingreds(self, recipe: Dict[str, List[str]], store_num: int, budget_preference: int):
        def convert_prices_to_lbs(df: pd.DataFrame) -> pd.DataFrame:
            def extract_weight_and_convert(price: float, name: str) -> float:
                import re
                # Enhanced regex to exclude percentages and invalid matches
                match = re.search(
                    r"(?<!\d)(\d+(\.\d+)?)(\s*)?(oz|lb|lbs|l|ml)\b", name.lower())

                if match:
                    weight = float(match.group(1))  # Extract numeric value
                    # Extract unit (oz, lb, L, mL)
                    unit = match.group(4)

                    # Convert units to pounds
                    if unit == "oz":
                        weight_lbs = weight / 16  # Convert oz to lbs
                    elif unit in ["lb", "lbs"]:
                        weight_lbs = weight       # Already in pounds
                    elif unit == "l" or unit == "liter":
                        # Convert liters to pounds (approximate)
                        weight_lbs = weight * 2.2
                    elif unit == "ml":
                        weight_lbs = weight * 0.0022  # Convert milliliters to pounds
                    else:
                        weight_lbs = None  # Unrecognized unit

                    # Calculate price per lb if weight is valid
                    if weight_lbs and weight_lbs > 0:
                        return round(price / weight_lbs, 2)

                # If no weight/volume is detected or invalid, assume price is already per lb
                return price

            # Apply the function to each row in the DataFrame
            df['Price per lb'] = df.apply(lambda row: extract_weight_and_convert(
                row['Prices'], row['Category Name']), axis=1)
            return df

        def normalize_column(column: pd.Series) -> pd.Series:
            min_val, max_val = column.min(), column.max()
            if max_val == min_val:
                # Return all 0 if values are constant
                return column.apply(lambda x: 0.0)
            return (column - min_val) / (max_val - min_val)

        def calculate_final_score(similarity: float, price: float, w_s: float, w_p: float) -> float:
            """Calculate final score based on weighted similarity and price."""
            print("Normalized price: ", price)
            return w_s * similarity - w_p * price

        # Assign weights based on budget preference
        weight_map = {
            1: (1, 0.1), # Strong bias towards similarity, little concern for price
            2: (1, 0.2), # Moderate bias towards similarity, minor concern for price
            3: (1, 0.4),  # Neutral balance between similarity and price
            4: (1, 0.5),  # Moderate bias towards cheaper prices
            5: (1, 0.7),  # Strong bias towards cheaper prices
        }
        w_s, w_p = weight_map[budget_preference]
        # remove_dish = False
        # Step 1: Remove basic ingredients using LLM
        filtered_recipe = self.LLM_remove_basic_ingredients(recipe)

        recipe_ingredients = [item for sublist in recipe.values()
                              for item in sublist]
        filtered_ingredients = [
            item for sublist in filtered_recipe.values() for item in sublist]
        basic_ingreds = [
            item.strip() for item in recipe_ingredients
            if item.strip() not in [i.strip() for i in filtered_ingredients]
        ]

        best_matches = {}
        mapped_ingredients = {}
        formatted_output = []
        # prices_best_matches = {}

        # Mark basic ingredients
        for ingredient in basic_ingreds:
            best_matches[ingredient] = 'Basic Ingredient, assumes customer has it'
            mapped_ingredients[ingredient] = ['Basic Ingredient']

        filtered_ingredients_list = list(filtered_recipe.values())[0]
        for ingredient in filtered_ingredients_list:
            print("INGREDIENT: ", ingredient)
            # Step 1: Find 10 closest specific ingredients
            similarity_scores = self.get_similarity_scores(
                ingredient, store_num, self.n_products)
            print("SIMILARITY DATAFRAME: \n", similarity_scores)
            updated_df = convert_prices_to_lbs(similarity_scores)

            # Step 2: Normalize prices and similarity scores
            updated_df['Normalized Price'] = normalize_column(
                updated_df['Price per lb'])
            # updated_df['Normalized Similarity'] = normalize_column(
            #     updated_df['Similarity Score'])
            print("UPDATED DATAFRAME:  \n", updated_df)

            # Step 3: Use LLM to find acceptable ingredients
            closest_ingredients = updated_df['Category Name'].tolist()
            acceptable_ingredients = self.LLM_find_matches(
                closest_ingredients, ingredient, recipe)
            print("ACCEPTABLE INGREDIENTS:  \n", acceptable_ingredients)

            # Filter DataFrame for acceptable ingredients
            filtered_df = updated_df[updated_df['Category Name'].isin(
                acceptable_ingredients)]
            

            # Step 4: Calculate final scores
            filtered_df['Final Score'] = filtered_df.apply(
                lambda row: calculate_final_score(row['Similarity Score'], row['Normalized Price'], w_s, w_p),
                axis=1  # Ensure row-wise application
            )
            print("FILTERED ACCEPTABLE DATAFRAME WITH FINAL SCORE:  \n", filtered_df)

            # Step 4.1: Print each acceptable ingredient's details
            # print("\n--- Acceptable Ingredients ---")
            # if not filtered_df.empty:
            #     for index, row in filtered_df.iterrows():
            #         print(f"Name: {row['Category Name']}, Price per lb: {row['Price per lb']:.2f}, Final Score: {row['Final Score']:.4f}")
            # else:
            #     print("No acceptable ingredients found.")
            # Select best match and exclude "None" matches
            if not filtered_df.empty:
                best_match_row = filtered_df.sort_values(
                    by='Final Score', ascending=False).iloc[0]
                best_match = best_match_row['Category Name']
                price = best_match_row['Prices']

                # Update results
                best_matches[ingredient] = best_match
                mapped_ingredients[ingredient] = closest_ingredients

                # Add to formatted output
                formatted_output.append({
                    "name": best_match,
                    "price": float(round(price, 2)),
                    "recommended": 1,
                    "quantity": 1,
                    "selected": True,
                    "unit": "",
                    "imageUrl": ""
                })
            else:
                best_matches[ingredient] = "None"

            # Store all matched ingredients
            mapped_ingredients[ingredient] = closest_ingredients

            
        # Handle 'None' matches
        keys = list(best_matches.keys())
        for key in keys:
            if best_matches[key] == 'None':
                # print(key)
                action = self.LLM_suggest_replacements(recipe, key)
                # print(action)
                if action == 'Remove ingredient.':
                    # print(f'Removing: {key}')
                    best_matches[key] = 'None, remove ingredient'
                elif action == 'Remove dish.':
                    best_matches[key] = 'None, remove dish'
                    # print(f'Removing dish')

        # Make it best fit for frontend
        formatted_output = produce_matched_ingredient_for_cart(
            formatted_output)
        print("formatted_output: ", formatted_output)
        return best_matches, mapped_ingredients, formatted_output

    def write_to_csv(self, best_matches: Dict[str, Any], mapped_ingredients: Dict[str, List[str]], output_file: str):
        keys = best_matches.keys()
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Ingredient", "Output embeddings model", "Best matches from LLM"])
            for key in keys:
                writer.writerow(
                    [key, ', '.join(mapped_ingredients[key]), best_matches[key]])
