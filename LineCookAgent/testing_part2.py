# testing the agent that searches for the closest ingredients.
# The agent takes one ingredient and a list of candidate ingredients(that represents a store's inventory), and then the agent outputs the closest ingredient. 
# There are some tricky test cases where such as Ingredient = "1 onion", and then one of the candidate ingredients are "Lay's Potato Chips, Sour Cream-Onion", 
# which the model does not output as the closest, even though it contains the word onion.

# The only failing test case is where ground beef is not available, and the model outputs turkey mince as the closest. (We define the correct output as None, but 
# it really depends on the user preference to choose turkey mince instead of ground beef).


from line_cook_agent import LLM_find_best_match
from testing_part2_data import test_cases, ingredients_bolognese, ingredients_pizza, ingredients_salad, ingredients_soup

# Map reference_list strings to actual lists
reference_mapping = {
    "ingredients_bolognese": ingredients_bolognese,
    "ingredients_pizza": ingredients_pizza,
    "ingredients_salad": ingredients_salad,
    "ingredients_soup": ingredients_soup
}

test_score = 0
total_tests = len(test_cases)

for test in test_cases:
    ingredient = test["ingredient"]
    candidates = test["candidates"]
    expected = test["expected"]
    reference_list = reference_mapping[test["reference_list"]]

    LLM_suggestion = LLM_find_best_match(candidates, ingredient, reference_list)
    # Convert both to lowercase for comparison
    if LLM_suggestion.lower() == expected.lower():
        test_score += 1
        print(f"Test passed: {LLM_suggestion} == {expected}")
    else:
        print(f"Test failed: {LLM_suggestion} != {expected}")

print(f"Test score: {test_score}/{total_tests}")