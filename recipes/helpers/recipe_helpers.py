def clean_instructions(instructions):
    # instructions - list({'step_number': int, 'instructions': str})
    valid_instructions = []
    for instruction in instructions:
        if instruction['instructions']:
            valid_instructions.append(instruction['instructions'])
    return valid_instructions

def clean_ingredients(ingredients):
    # ingredients - list({'ingredient_name': str, 'quantity_unit': int, 'quantity_unit': str})
    valid_ingredients = []
    for ingredient in ingredients:
        if ingredient['ingredient_name'] and ingredient['ingredient_quantity']:
            valid_ingredients.append(ingredient)
    return valid_ingredients
