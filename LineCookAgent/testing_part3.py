import line_cook_agent
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

test_score = 0
recipe = {"Spaghetti Bolognese": ingredients_bolognese}
replacement_test = LLM_suggest_replacements(recipe, ingredients_bolognese[2])
if replacement_test == 'Remove ingredient.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')

replacement_test = LLM_suggest_replacements(recipe, ingredients_bolognese[-2])
if replacement_test == 'Remove ingredient.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')

replacement_test = LLM_suggest_replacements(recipe, ingredients_bolognese[5])
if replacement_test == 'Remove dish.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')

replacement_test = LLM_suggest_replacements(recipe, ingredients_bolognese[6])
if replacement_test == 'Remove dish.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')

recipe = {"Spaghetti Bolognese": ingredients_pizza}
replacement_test = LLM_suggest_replacements(recipe, ingredients_pizza[8])
if replacement_test == 'Remove ingredient.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')

replacement_test = LLM_suggest_replacements(recipe, ingredients_pizza[-2])
if replacement_test == 'Remove ingredient.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')

replacement_test = LLM_suggest_replacements(recipe, ingredients_pizza[0])
if replacement_test == 'Remove dish.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')

replacement_test = LLM_suggest_replacements(recipe, ingredients_pizza[7])
if replacement_test == 'Remove dish.':
    print('Test passed')
    test_score += 1
else:
    print('Test failed')


print("The model scored: ", test_score, " out of 8")