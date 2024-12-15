# This is testing part 3, where I test the replacement function. The replacement function receives one unavailable ingredient together with the recipe, 
# and should decide wether it is ok to just remove the ingredient from the recipe or if we need to remove the whole dish and replace it with something else 
# (if the ingredient is important)

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.line_cook_service import LineCookService
from evaluation.line_cook_testing_part3_data import recipes, test_cases_replacements


# Assuming this code is in `services/line_cook_service.py`
file_path = os.path.join(os.path.dirname(
    __file__), '..', 'backend', 'data', 'sampled_food.csv')
# Resolve the path to its absolute form for clarity (optional, for debugging purposes)
absolute_path = os.path.abspath(file_path)
print(f"Resolved file path: {absolute_path}")

# Initialize LineCookService
line_cook_service = LineCookService(database_path=absolute_path)

test_score = 0
total_tests = len(test_cases_replacements)

for test_case in test_cases_replacements:
    recipe_name = test_case["recipe_name"]
    unavailable_ingredient = test_case["unavailable_ingredient"]
    expected = test_case["expected"]

    # Create a single-recipe dict for the function call
    recipe_dict = {recipe_name: recipes[recipe_name]}

    # Perform the test
    replacement_test = line_cook_service.LLM_suggest_replacements(recipe_dict, unavailable_ingredient)
    if replacement_test.lower() == expected.lower():
        print(f"Test passed: {unavailable_ingredient} -> {replacement_test}")
        test_score += 1
    else:
        print(f"Test failed: {unavailable_ingredient} -> {replacement_test}, expected {expected}")

print("The model scored: ", test_score, " out of ", total_tests)
