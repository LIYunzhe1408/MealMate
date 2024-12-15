
ingredients_bolognese = [
    "2 tbsp olive oil",
    "1 medium onion",
    "1 medium carrot",
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
    "1 red bell pepper, sliced",
    "1 small onion, thinly sliced",
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

recipes = {
    "Spaghetti Bolognese": ingredients_bolognese,
    "Pepperoni Pizza": ingredients_pizza,
    "Greek Salad": ingredients_salad,
    "Chicken Soup": ingredients_soup
}

# Test cases for the replacement function
# Each test case is a dict with:
#   - recipe_name: which recipe to test
#   - unavailable_ingredient: the ingredient from that recipe that is unavailable
#   - expected: the expected suggestion ('Remove ingredient.' or 'Remove dish.')
test_cases_replacements = [
    # Original tests from Bolognese
    {
        "recipe_name": "Spaghetti Bolognese",
        "unavailable_ingredient": ingredients_bolognese[2],  # 1 medium carrot
        "expected": "Remove ingredient."
    },
    {
        "recipe_name": "Spaghetti Bolognese",
        "unavailable_ingredient": ingredients_bolognese[-2], # Grated Parmesan cheese
        "expected": "Remove ingredient."
    },
    {
        "recipe_name": "Spaghetti Bolognese",
        "unavailable_ingredient": ingredients_bolognese[5],  # 500g ground beef
        "expected": "Remove dish."
    },
    {
        "recipe_name": "Spaghetti Bolognese",
        "unavailable_ingredient": ingredients_bolognese[6],  # 400g canned chopped tomatoes
        "expected": "Remove dish."
    },
    
    # Original tests from Pizza
    {
        "recipe_name": "Pepperoni Pizza",
        "unavailable_ingredient": ingredients_pizza[8],  # 100g sliced pepperoni
        "expected": "Remove dish."
    },
    {
        "recipe_name": "Pepperoni Pizza",
        "unavailable_ingredient": ingredients_pizza[-2], # 1 small onion, thinly sliced
        "expected": "Remove ingredient."
    },
    {
        "recipe_name": "Pepperoni Pizza",
        "unavailable_ingredient": ingredients_pizza[0],  # 500g all-purpose flour
        "expected": "Remove dish."
    },
    {
        "recipe_name": "Pepperoni Pizza",
        "unavailable_ingredient": ingredients_pizza[7],  # 200g shredded mozzarella cheese
        "expected": "Remove dish."
    },


    # Greek Salad:
    # Removing lettuce (a main ingredient), expect dish removal
    {
        "recipe_name": "Greek Salad",
        "unavailable_ingredient": ingredients_salad[0], # 1 head romaine lettuce
        "expected": "Remove dish."
    },
    # Removing feta cheese (important but could still be a salad without it)
    {
        "recipe_name": "Greek Salad",
        "unavailable_ingredient": ingredients_salad[3], # 100g feta cheese
        "expected": "Remove ingredient."
    },

    # Chicken Soup:
    # Removing chicken stock (base of soup)
    {
        "recipe_name": "Chicken Soup",
        "unavailable_ingredient": ingredients_soup[5], # 2 liters chicken stock
        "expected": "Remove dish."
    },
    # Removing celery stalks (could still make soup without celery)
    {
        "recipe_name": "Chicken Soup",
        "unavailable_ingredient": ingredients_soup[2], # 2 celery stalks
        "expected": "Remove ingredient."
    }
]