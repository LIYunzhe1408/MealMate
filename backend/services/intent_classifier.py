from transformers import pipeline

class IntentClassifier:
    def __init__(self):
        # Load a lightweight pre-trained text classification model
        print("Loading zero-shot classification model...")
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.candidate_labels = ["recipe-related", "non-recipe-related"]
        print("Zero-shot classification model loaded.")

    def classify(self, query: str) -> str:
        # Predict the most likely category
        result = self.classifier(query, candidate_labels=self.candidate_labels)
        return result["labels"][0]  # Returns the label with the highest score
