def produce_matched_ingredient_for_cart(formatted_output):
    for entry in formatted_output:
        entry["imageUrl"] = "/images/pasta/pasta.png"
    return formatted_output
