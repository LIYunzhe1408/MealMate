from line_cook_agent import LLM_find_best_match

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
test_score = 0

ingredient = "1 onion"
candidates = ["Lay's Potato Chips, Sour Cream-Onion", "Onion Powder", "Onion Soup Mix", "Onion", "Onion, Powdered"]
closest_ingredient = "Onion"
LLM_suggestion = LLM_find_best_match(candidates, ingredient, ingredients_bolognese)
if LLM_suggestion == closest_ingredient:
    test_score += 1
    print(f'Test passed: {LLM_suggestion} == {closest_ingredient}')
else:
    print(f'Test failed: {LLM_suggestion} != {closest_ingredient}')

ingredient = "1 onion"
candidates = ["Lay's Potato Chips, Sour Cream-Onion", "Onion Powder", "Onion Soup Mix", "Onion, Powdered"]
closest_ingredient = "None"
LLM_suggestion = LLM_find_best_match(candidates, ingredient, ingredients_bolognese)
if LLM_suggestion == closest_ingredient:
    test_score += 1
    print(f'Test passed: {LLM_suggestion} == {closest_ingredient}')
else:
    print(f'Test failed: {LLM_suggestion} != {closest_ingredient}')

ingredient = "1 red bell pepper"
candidates = ["Lay's Potato Chips, pepper", " Black pepper", "Chili pepper", "Red bell pepper"]
closest_ingredient = "Red bell pepper"
LLM_suggestion = LLM_find_best_match(candidates, ingredient, ingredients_bolognese)
if LLM_suggestion == closest_ingredient:
    test_score += 1
    print(f'Test passed: {LLM_suggestion} == {closest_ingredient}')
else:
    print(f'Test failed: {LLM_suggestion} != {closest_ingredient}')

ingredient = "1 red bell pepper"
candidates = ["Lay's Potato Chips, pepper", " Black pepper", "Chili pepper", "powdered pepper"]
closest_ingredient = "None"
LLM_suggestion = LLM_find_best_match(candidates, ingredient, ingredients_bolognese)
if LLM_suggestion == closest_ingredient:
    test_score += 1
    print(f'Test passed: {LLM_suggestion} == {closest_ingredient}')
else:
    print(f'Test failed: {LLM_suggestion} != {closest_ingredient}')

print(f'Test score: {test_score}/4')

