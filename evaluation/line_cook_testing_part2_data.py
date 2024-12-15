# test_data.py

# Ingredient lists
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

ingredients_pizza = [
    "500g all-purpose flour",
    "1 tsp salt",
    "1 tsp sugar",
    "1 packet (7g) instant yeast",
    "3 tbsp olive oil",
    "300ml warm water",
    "200ml tomato sauce",
    "200g shredded mozzarella cheese",
    "100g sliced pepperoni",
    "1 tsp dried oregano",
    "1 tsp dried basil",
    "1 red bell pepper",
    "1 small onion",
    "1 handful fresh basil leaves"
]

ingredients_salad = [
    "1 head romaine lettuce",
    "1 cucumber",
    "2 tomatoes",
    "100g feta cheese",
    "50g black olives",
    "2 tbsp olive oil",
    "1 tbsp red wine vinegar",
    "Salt and pepper"
]

ingredients_soup = [
    "1 onion",
    "2 garlic cloves",
    "2 celery stalks",
    "2 carrots",
    "1 bay leaf",
    "2 liters chicken stock",
    "200g shredded chicken",
    "Salt and pepper"
]


# Test cases
# Each test case is a dictionary with:
# - ingredient: the ingredient from the recipe
# - candidates: a list of candidate ingredients from the store
# - expected: the expected best match or "None"
# - reference_list: which reference list to use ("ingredients_bolognese" or "ingredients_pizza")

test_cases = [
    {
        "ingredient": "1 onion",
        "candidates": ["Lay's Potato Chips, Sour Cream-Onion", "Onion Powder", "Onion Soup Mix", "Onion", "Onion, Powdered"],
        "expected": "Onion",
        "reference_list": "ingredients_bolognese"
    },
    {
        "ingredient": "1 onion",
        "candidates": ["Lay's Potato Chips, Sour Cream-Onion", "Onion Powder", "Onion Soup Mix", "Onion, Powdered"],
        "expected": "Onion Powder",
        "reference_list": "ingredients_bolognese"
    },
    {
        "ingredient": "1 red bell pepper",
        "candidates": ["Lay's Potato Chips, pepper", " Black pepper", "Chili pepper", "Red bell pepper"],
        "expected": "Red bell pepper",
        "reference_list": "ingredients_bolognese"
    },
    {
        "ingredient": "1 red bell pepper",
        "candidates": ["Lay's Potato Chips, pepper", " Black pepper", "Chili pepper", "powdered pepper"],
        "expected": "None",
        "reference_list": "ingredients_bolognese"
    },
    # Add more diverse tests:
    {
        "ingredient": "500g ground beef",
        "candidates": ["ground turkey", "beef jerky", "fresh beef steak", "Ground Beef"],
        "expected": "Ground Beef",
        "reference_list": "ingredients_bolognese"
    },
    {
        "ingredient": "500g ground beef",
        "candidates": ["turkey mince", "soy crumbles", "chicken breast"],
        "expected": "turkey mince",
        "reference_list": "ingredients_bolognese"
    },
    {
        "ingredient": "200g shredded mozzarella cheese",
        "candidates": ["mozarella block", "shredded mozzarella", "shredded cheddar", "fresh mozzarella"],
        "expected": "shredded mozzarella",
        "reference_list": "ingredients_pizza"
    },
    {
        "ingredient": "300ml warm water",
        "candidates": ["bottled water", "cold water", "sparkling water"],
        "expected": "None",
        "reference_list": "ingredients_pizza"
    },
    {
        "ingredient": "1 handful fresh basil leaves",
        "candidates": ["dried basil", "fresh basil", "basil leaves"],
        "expected": "fresh basil",
        "reference_list": "ingredients_pizza"
    },
    {
        "ingredient": "2 tbsp olive oil",
        "candidates": ["olive oil spray", "extra virgin olive oil", "canola oil"],
        "expected": "extra virgin olive oil",
        "reference_list": "ingredients_bolognese"
    },
     {
        "ingredient": "1 cucumber",
        "candidates": ["cucumber slices", "cucumber seed", "zucchini", "English cucumber"],
        "expected": "English cucumber",
        "reference_list": "ingredients_salad"
    },
    {
        "ingredient": "1 cucumber",
        "candidates": ["zucchini", "pickle", "melon"],
        "expected": "None",
        "reference_list": "ingredients_salad"
    },
    {
        "ingredient": "100g feta cheese",
        "candidates": ["feta crumbles", "feta block", "goat cheese"],
        "expected": "feta block",
        "reference_list": "ingredients_salad"
    },
    {
        "ingredient": "2 liters chicken stock",
        "candidates": ["chicken broth", "vegetable stock", "beef stock", "stock cube"],
        "expected": "chicken broth",
        "reference_list": "ingredients_soup"
    },
    {
        "ingredient": "200g shredded chicken",
        "candidates": ["shredded turkey", "diced chicken", "chicken strips", "rotisserie chicken"],
        "expected": "diced chicken",
        "reference_list": "ingredients_soup"
    },
    {
        "ingredient": "1 onion",
        "candidates": ["scallion", "spring onion", "shallot"],
        "expected": "None",
        "reference_list": "ingredients_soup"
    },
    {
        "ingredient": "2 tomatoes",
        "candidates": ["Roma tomatoes", "diced tomatoes", "sun-dried tomatoes"],
        "expected": "Roma tomatoes",
        "reference_list": "ingredients_salad"
    }
]