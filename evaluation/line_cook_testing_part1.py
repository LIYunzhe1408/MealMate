from line_cook_agent import LLM_find_best_match, get_similarity_scores
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

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

for i, ingreident in enumerate(ingredients_bolognese):

    similarity_scores = get_similarity_scores(ingreident, grocery_products_embeddings, 5, grocery_names)
    print(f'Similarity scores for ingredient {ingreident} is {similarity_scores}')