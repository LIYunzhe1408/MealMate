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
        self.database = [pd.read_csv(database_paths[0]), pd.read_csv(database_paths[1]), pd.read_csv(database_paths[2]), pd.read_csv(database_paths[3]), pd.read_csv(database_paths[4])]
        self.grocery_names = [self.database[0]['PRODUCT_NAME'].tolist(), self.database[1]['PRODUCT_NAME'].tolist(), self.database[2]['PRODUCT_NAME'].tolist(), self.database[3]['PRODUCT_NAME'].tolist(), self.database[4]['PRODUCT_NAME'].tolist()]
        self.grocery_prices = [self.database[0]['PRICE_CURRENT'].tolist(), self.database[1]['PRICE_CURRENT'].tolist(), self.database[2]['PRICE_CURRENT'].tolist(), self.database[3]['PRICE_CURRENT'].tolist(), self.database[4]['PRICE_CURRENT'].tolist()]
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
            embeddings = [np.load(self.embeddings_paths[0]), np.load(self.embeddings_paths[1]), np.load(self.embeddings_paths[2]), np.load(self.embeddings_paths[3]), np.load(self.embeddings_paths[4])]
            print(f"Embeddings shape: {embeddings[0].shape}")
            return embeddings
        else:
            print("No precomputed embeddings found. Creating embeddings...")
            embeddings = [self.embeddings_model.encode(self.grocery_names[0], show_progress_bar=True), self.embeddings_model.encode(self.grocery_names[1], show_progress_bar=True), self.embeddings_model.encode(self.grocery_names[2], show_progress_bar=True), self.embeddings_model.encode(self.grocery_names[3], show_progress_bar=True), self.embeddings_model.encode(self.grocery_names[4], show_progress_bar=True)]
            for i in range(5):
                os.makedirs(os.path.dirname(self.embeddings_paths[i]), exist_ok=True)
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
        general_ingredient_embedding = self.embeddings_model.encode(general_ingredient).reshape(1, -1)
        similarity_scores = cosine_similarity(self.grocery_products_embeddings[store_num], general_ingredient_embedding).flatten()
        similarity_df = pd.DataFrame({'Category Name': self.grocery_names[store_num], 'Prices' : self.grocery_prices[store_num], 'Similarity Score': similarity_scores})
        similarity_df = similarity_df.sort_values(by='Similarity Score', ascending=False)
        return similarity_df.head(n)
    

    # def LLM_find_best_match(self, closest_ingredients: List[str], specific_ingredient: str, recipe: Dict[str, List[str]]) -> str:
    #     prompt = f"""I am going to make the recipe {recipe}. I have automated a search through a store's database and have found the 5 closest ingredients to {specific_ingredient}: {closest_ingredients}.
    # Your job is to find out if any of the ingredients, {closest_ingredients} match the ingredient I am looking for: {specific_ingredient}. The ingredients do not have to match exactly,
    # but it has to work in the recipe I provided. That means that synonyms or similar ingredients are also valid, as long as they work in the recipe. However, be careful and use your knowledge
    # about food. Just because two ingredients have similar names, does not mean they work in the same recipe.
    # If one or more of the ingredients matches the ingredient I am looking for, output the ingredient that matches best. If none of the ingredients match, please write 'None'.
    # Only output either the closest ingredient or 'None'."""
    #     best_match = self.get_llm_response(prompt)
    #     return best_match
    
    
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

    # def find_prices_for_ingredients(ingredients_dict: Dict[str, List[str]], csv_path: str) -> Dict[str, Dict[str, float]]:
    #     # Load the CSV file
    #     print("Loading CSV file...")
    #     df = pd.read_csv(csv_path)

    #     # Ensure the necessary columns exist
    #     if "description" not in df.columns or "price" not in df.columns:
    #         raise ValueError("CSV file must contain 'description' and 'price' columns.")

    #     # Initialize the results dictionary
    #     results = {}

    #     # Iterate through the input dictionary
    #     for ingredient, matches in ingredients_dict.items():
    #         ingredient_prices = {}

    #         for match in matches:
    #             # Search for the match in the 'description' column containing "lb" or similar units
    #             matched_rows = df[
    #                 df["description"].str.contains(match, case=False, na=False) &
    #                 df["description"].str.contains(r"\b(lb|lbs|pound|pounds)\b", case=False, na=False)
    #             ]

    #             # If matches are found, store their prices
    #             if not matched_rows.empty:
    #                 # Extract the first price match (can extend this logic later)
    #                 price = matched_rows.iloc[0]["price"]
    #                 description = matched_rows.iloc[0]["description"]
    #                 ingredient_prices[match] = {"price_per_lb": round(float(price), 2), "description": description}
    #             else:
    #                 ingredient_prices[match] = {"price_per_lb": None, "description": "Not Found"}

    #         results[ingredient] = ingredient_prices

    #     return results
    
    # def select_best_match(self, matches: List[str], budget_sensitivity: int) -> Dict[str, Any]:
    #     if not matches:
    #         return {"best_match": None, "price": None, "reason": "No matches found"}

    #     # Simulate prices for the given matches (e.g., 1 to 10)
    #     # price_data = {ingredient: random.uniform(1.0, 10.0) for ingredient in matches}

    #     print(f"Generated prices: {price_data}")  # Debug: Print price data

    #     # Sort based on budget sensitivity:
    #     # - Low sensitivity (1): Sort by price last.
    #     # - High sensitivity (5): Prioritize the cheapest.
    #     if budget_sensitivity == 1:
    #         # Pick the first ingredient (ignoring price)
    #         best_match = matches[0]
    #     else:
    #         # Sort by price (ascending) to prioritize cheaper ingredients
    #         sorted_matches = sorted(price_data.items(), key=lambda x: x[1])
    #         best_match = sorted_matches[0][0]  # Ingredient with the lowest price

    #     return {
    #         "best_match": best_match,
    #         "price": round(price_data[best_match], 2),
    #         "reason": f"Selected based on budget sensitivity: {budget_sensitivity}"
    #     }

    def search_for_ingreds(self, recipe: Dict[str, List[str]], store_num: int, budget_preference: int):
        # def convert_to_lbs(description: str, price: float) -> float:
        #     """Converts price to price per pound if weight is specified."""
        #     import re
        #     match = re.search(r'(\d+(?:\.\d+)?)\s*(oz|lb|lbs)', description.lower())
        #     if match:
        #         weight = float(match.group(1))
        #         unit = match.group(2)
        #         if "oz" in unit:
        #             weight /= 16  # Convert ounces to pounds
        #         return round(price / weight, 2) if weight > 0 else None
        #     return None  # No weight information available

        def convert_prices_to_lbs(df: pd.DataFrame) -> pd.DataFrame:
            """
            Convert prices in the dataframe to a per-lb price based on Category Name.

            Args:
                df (pd.DataFrame): DataFrame with 'Category Name' and 'Prices' columns.

            Returns:
                pd.DataFrame: Updated DataFrame with 'Price per lb' column.
            """

            def extract_weight_and_convert(price: float, name: str) -> float:
                """
                Extract weight (lbs, oz, L, mL) from the name and convert price to per-lb price.
                Ignores percentages or other non-unit numbers.
                Assumptions:
                - 1 L ≈ 2.2 lbs
                - 1 mL ≈ 0.0022 lbs
                - 16 oz = 1 lb
                """
                import re
                # Enhanced regex to exclude percentages and invalid matches
                match = re.search(r"(?<!\d)(\d+(\.\d+)?)(\s*)?(oz|lb|lbs|l|ml)\b", name.lower())

                if match:
                    weight = float(match.group(1))  # Extract numeric value
                    unit = match.group(4)           # Extract unit (oz, lb, L, mL)

                    # Convert units to pounds
                    if unit == "oz":
                        weight_lbs = weight / 16  # Convert oz to lbs
                    elif unit in ["lb", "lbs"]:
                        weight_lbs = weight       # Already in pounds
                    elif unit == "l" or unit == "liter":
                        weight_lbs = weight * 2.2  # Convert liters to pounds (approximate)
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
            df['Price per lb'] = df.apply(lambda row: extract_weight_and_convert(row['Prices'], row['Category Name']), axis=1)
            return df

        def normalize_column(column: pd.Series) -> pd.Series:
            min_val, max_val = column.min(), column.max()
            if max_val == min_val:
                return column.apply(lambda x: 0.0)  # Return all 0 if values are constant
            return (column - min_val) / (max_val - min_val)
    
        def calculate_final_score(similarity: float, price: float, w_s: float, w_p: float) -> float:
            """Calculate final score based on weighted similarity and price."""
            return w_s * similarity - w_p * price

        # Assign weights based on budget preference
        weight_map = {
            1: (0.9, -0.1),  # Strong bias towards similarity, little concern for price
            2: (0.75, -0.25),  # Moderate bias towards similarity, minor concern for price
            3: (0.5, -0.5),  # Neutral balance between similarity and price
            4: (0.25, -0.75),  # Moderate bias towards cheaper prices
            5: (0.1, -0.9),  # Strong bias towards cheaper prices
        }
        w_s, w_p = weight_map[budget_preference]
        # remove_dish = False
        # Step 1: Remove basic ingredients using LLM
        filtered_recipe = self.LLM_remove_basic_ingredients(recipe)

        recipe_ingredients = [item for sublist in recipe.values() for item in sublist]
        filtered_ingredients = [item for sublist in filtered_recipe.values() for item in sublist]
        basic_ingreds = [item for item in recipe_ingredients if item not in filtered_ingredients]

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
            # Step 1: Find 10 closest specific ingredients
            similarity_scores = self.get_similarity_scores(ingredient, store_num, self.n_products)
            updated_df = convert_prices_to_lbs(similarity_scores)

            # Step 2: Normalize prices and similarity scores
            updated_df['Normalized Price'] = normalize_column(updated_df['Price per lb'])
            updated_df['Normalized Similarity'] = normalize_column(updated_df['Similarity Score'])

            # Step 3: Use LLM to find acceptable ingredients
            closest_ingredients = updated_df['Category Name'].tolist()
            print("Closest ingredients: ", closest_ingredients)
            acceptable_ingredients = self.LLM_find_matches(closest_ingredients, ingredient, recipe)
            print("Acceptable ingredients: ", acceptable_ingredients)

            # Filter DataFrame for acceptable ingredients
            filtered_df = updated_df[updated_df['Category Name'].isin(acceptable_ingredients)]

            # Step 4: Calculate final scores
            filtered_df = filtered_df.copy()
            filtered_df['Final Score'] = calculate_final_score(
                filtered_df['Normalized Similarity'], filtered_df['Normalized Price'], w_s, w_p
            )

            # # Step 5: Select the best match
            # if not filtered_df.empty:
            #     print("\n--- Accepted Ingredients ---")
            #     # Print all accepted ingredients with price per lb and final score
            #     for index, row in filtered_df.iterrows():
            #         print(f"Ingredient: {row['Category Name']}, Price per lb: {row['Price per lb']:.2f}, Final Score: {row['Final Score']:.4f}")
                
            #     # Sort the DataFrame by the 'Final Score' column in descending order
            #     best_match = filtered_df.sort_values(by='Final Score', ascending=False).iloc[0]['Category Name']
                
            #     print(f"\nBest Match for '{ingredient}': {best_match}\n")
                
            #     # Assign the best ingredient match to the 'best_matches' dictionary
            #     best_matches[ingredient] = best_match
            # else:
            #     # If the DataFrame is empty (no acceptable ingredients found)
            #     print(f"\nNo acceptable ingredients found for '{ingredient}'. Assigning 'None'.\n")
            #     best_matches[ingredient] = "None"
            
            # Select best match and exclude "None" matches
            if not filtered_df.empty:
                best_match_row = filtered_df.sort_values(by='Final Score', ascending=False).iloc[0]
                best_match = best_match_row['Category Name']
                price = best_match_row['Price per lb']

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


            # # Step 3: Use LLM to find acceptable ingredients
            # acceptable_ingredients = self.LLM_find_matches(closest_ingredients, ingredient, recipe)
            # acceptable_prices = {}
            # for idx, specific_ingredient in enumerate(closest_ingredients):
            #     if specific_ingredient in acceptable_ingredients:
            #         price_per_lb = convert_to_lbs(specific_ingredient, closest_prices[idx])
            #         if price_per_lb:
            #             acceptable_prices[specific_ingredient] = price_per_lb

            # if not acceptable_ingredients:
            #     best_matches[ingredient] = 'None'
            # else:
            #     # Step 4: Select the best match based on budget sensitivity
            #     sorted_ingredients = sorted(acceptable_prices.items(), key=lambda x: x[1])
            #     if budget_preference == 1:  # User doesn't care about price
            #         best_matches[ingredient] = sorted_ingredients[0][0]
            #     else:
            #         # Adjust sorting based on budget preference (1-5)
            #         best_matches[ingredient] = sorted_ingredients[0][0]  # Cheapest ingredient
            # mapped_ingredients[ingredient] = closest_ingredients
            



            # best_match = self.LLM_find_best_match(similarity_scores["Category Name"].tolist(), ingredient, recipe)
            # best_matches[ingredient] = best_match


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

        print("Best matches: ", best_matches), print("Mapped ingredients: ", mapped_ingredients)

        # Make it best fit for frontend
        formatted_output = produce_matched_ingredient_for_cart(formatted_output)

        return best_matches, mapped_ingredients, formatted_output

    def write_to_csv(self, best_matches: Dict[str, Any], mapped_ingredients: Dict[str, List[str]], output_file: str):
        keys = best_matches.keys()
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Ingredient", "Output embeddings model", "Best matches from LLM"])
            for key in keys:
                writer.writerow([key, ', '.join(mapped_ingredients[key]), best_matches[key]])