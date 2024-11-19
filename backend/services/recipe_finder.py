from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import numpy as np
import os
from typing import List, Dict

class RecipeFinder:
    def __init__(self, embeddings_path="data/recipe_embeddings.npy"):
        self.embeddings_path = embeddings_path

        # Load dataset
        print("Loading dataset...")
        self.ds = load_dataset("Shengtao/recipe")
        print("Dataset loaded.")
        
        # used for testing
        # self.subset = self.ds['train'].select(range(100))
        # print(f"Subset sample: {self.subset[:2]}")
        
        # Initialize model
        print("Loading model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded.")
        
        # Load or encode embeddings
        if os.path.exists(self.embeddings_path):
            print("Loading precomputed embeddings...")
            self.recipe_embeddings = np.load(self.embeddings_path)
            print(f"Embeddings shape: {self.recipe_embeddings.shape}")
            print("Embeddings loaded.")
        else:
            print("Encoding recipes with progress...")
            self.recipe_embeddings = self._encode_with_progress()
            print("Recipes encoded. Saving embeddings...")
            np.save(self.embeddings_path, self.recipe_embeddings)
            print("Embeddings saved.")

    def _encode_with_progress(self):
        # Create a list of recipe text
        recipe_texts = [
            f"{recipe['title']}:{' '.join(recipe['ingredients'])}"
            for recipe in self.ds['train']
        ]
        # Encode with a progress bar
        embeddings = []
        for text in tqdm(recipe_texts, desc="Encoding recipes", unit="recipe"):
            embeddings.append(self.model.encode(text))
        return np.array(embeddings)

    def find_similar_recipes(self, query: str, k: int = 3) -> List[Dict]:
        print(f"Query: {query}")  # Debug: Check the query
        query_embedding = self.model.encode(query)
        print(f"Query embedding: {query_embedding[:5]}...")  # Debug: Print a sample of the query embedding

        similarities = np.dot(self.recipe_embeddings, query_embedding)
        print(f"Similarities: {similarities[:5]}...")  # Debug: Print a sample of similarity scores

        top_k_indices = np.argsort(similarities)[-k:][::-1]
        print(f"Top K indices: {top_k_indices}")  # Debug: Check the top K indices
    
        print(f"Dataset size: {len(self.ds['train'])}")
        
        
        results = [
            {
                'title': self.ds['train']['title'][idx],
                'ingredients': self.ds['train']['ingredients'][idx],
                'similarity_score': float(similarities[idx])
            }
            for idx in top_k_indices
        ]
        return results
