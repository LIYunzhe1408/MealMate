# testing the agent that searches for the closest ingredients.
# The agent takes one ingredient and a list of candidate ingredients(that represents a store's inventory), and then the agent outputs the closest ingredient. 
# There are some tricky test cases where such as Ingredient = "1 onion", and then one of the candidate ingredients are "Lay's Potato Chips, Sour Cream-Onion", 
# which the model does not output as the closest, even though it contains the word onion.

# The only failing test case is where ground beef is not available, and the model outputs turkey mince as the closest. (We define the correct output as None, but 
# it really depends on the user preference to choose turkey mince instead of ground beef).
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.line_cook_service import LineCookService
from line_cook_testing_part2_data import test_cases, ingredients_bolognese, ingredients_pizza, ingredients_salad, ingredients_soup

file_paths = [
                os.path.join(os.path.dirname(__file__), '..', 'backend','data', 'grocery_names_prices_safeway.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'backend','data', 'grocery_names_prices_target.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'backend','data', 'grocery_names_prices_trader_joes.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'backend','data', 'grocery_names_prices_walmart.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'backend','data', 'grocery_names_prices_whole_foods.csv')
                ]

# Resolve the path to its absolute form for clarity (optional, for debugging purposes)
absolute_paths = [os.path.abspath(file_paths[0]), os.path.abspath(file_paths[1]), os.path.abspath(file_paths[2]), os.path.abspath(file_paths[3]), os.path.abspath(file_paths[4])]
print(f"Resolved file path: {absolute_paths}")

# Initialize LineCookService
line_cook_service = LineCookService(database_paths=absolute_paths)

# Map reference_list strings to actual lists
reference_mapping = {
    "ingredients_bolognese": ingredients_bolognese,
    "ingredients_pizza": ingredients_pizza,
    "ingredients_salad": ingredients_salad,
    "ingredients_soup": ingredients_soup
}

test_score = 0
total_tests = len(test_cases)

start_time = time.time()

for test in test_cases:
    ingredient = test["ingredient"]
    candidates = test["candidates"]
    expected = test["expected"]
    reference_list = reference_mapping[test["reference_list"]]
    
    LLM_suggestion = line_cook_service.LLM_find_matches(
        candidates, ingredient, {"ingredients": reference_list})

    # Convert both to lowercase for comparison
    if len(LLM_suggestion) > 0:
        if LLM_suggestion[0].lower() == expected.lower():
            test_score += 1
            print(f"Test passed: {LLM_suggestion[0]} == {expected}")
        else:
            print(f"Test failed: {LLM_suggestion[0]} != {expected}")
    else:
        if 'None'.lower() == expected.lower():
            test_score += 1
            print(f"Test passed: None == {expected}")
        else:
            print(f"Test failed: None != {expected}")

end_time = time.time()

# Calculate total elapsed time
elapsed_time = end_time - start_time

print(f"Test score: {test_score}/{total_tests}")
print(f"Total testing time: {elapsed_time:.2f} seconds")