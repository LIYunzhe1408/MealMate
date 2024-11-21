from line_cook_agent import search_for_ingreds, write_to_csv, LLM_suggest_replacements, LLM_remove_basic_ingredients, LLM_find_best_match, get_similarity_scores
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import openai
import ast
import os 
import numpy as np
import csv


database = pd.read_csv('/Users/matswiigmartinussen/Documents/Berkeley/194/Project/MealMate/LineCookAgent/food.csv')
database = database.sample(n=10000, random_state=42)
grocery_names = database['description'].tolist()
embeddings_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
grocery_products_embeddings = embeddings_model.encode(grocery_names)

ingredients_bolognese = [
    "2 tbsp olive oil",
    "1 onion",
    "1 carrot",
    "1 celery stalk",
    "2 garlic cloves",
    "500g ground beef",
    "400g canned chopped tomatoes",
    "2 tbsp tomato paste",
    "1/2 cup beef or vegetable stock",
    "1/2 cup whole milk",
    "1 tsp dried oregano",
    "1 tsp dried basil",
    "Salt and pepper",
    "400g spaghetti",
    "Grated Parmesan cheese",
    "1/4 cup red wine"
]
recipe = {"Spaghetti Bolognese": ingredients_bolognese}

best_matches, mapped_ingredients = search_for_ingreds(recipe, grocery_products_embeddings, grocery_names, 5)
write_to_csv(best_matches, mapped_ingredients, 'testing.csv')