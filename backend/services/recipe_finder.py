from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import numpy as np
from typing import List, Dict

class RecipeFinder:
    def __init__(self):
        # Load the dataset once
        self.ds = load_dataset("Shengtao/recipe")
        # Initialize the embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Pre-compute embeddings for all recipes
        self.recipe_embeddings = self.model.encode([
            f"{recipe['title']} {' '.join(recipe['ingredients'])}"
            for recipe in self.ds['train']
        ])

    def find_similar_recipes(self, query: str, k: int = 3) -> List[Dict]:
        # Encode the query
        query_embedding = self.model.encode(query)
        
        # Calculate similarities
        similarities = np.dot(self.recipe_embeddings, query_embedding)
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        # Return top k recipes
        return [
            {
                'title': self.ds['train'][idx]['title'],
                'ingredients': self.ds['train'][idx]['ingredients'],
                'similarity_score': similarities[idx]
            }
            for idx in top_k_indices
        ]