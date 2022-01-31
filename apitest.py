def parse_unit(unit_name):

    #weight
    weight = {
        'grams': ['g', 'grams'],
        'kilograms': ['kg', 'kilograms'],
        'pound': ['lb', 'pounds'], 
        'ouce': ['oz', 'ounce']
    }
    #spoons
    spoon = {
        'teaspoon': ['tsp', 'teaspoon'],
        'tablespoon':['tbsp', 'tablespoon'],
    }
    #volume
    volume = {
        'cup': ['cup'], 
        'liter': ['liter', 'l'], 
        'fluid_oz': ['fluid oz', 'fl oz', 'fluid ounce', 'fl ounce'], 
        'ml': ['ml', 'milliliter'], 
        'gallon': ['gal', 'gallon'], 
    }

    
    for unit in weight:
        for str in weight[unit]:
            if(unit_name == str):
                parsed_unit = unit
                unit_type = 'weight'

    for unit in spoon:
        for str in spoon[unit]:
            if(unit_name == str):
                parsed_unit = unit
                unit_type = 'spoon'

    for unit in volume:
        for str in volume[unit]:
            if(unit_name == str):
                parsed_unit = unit
                unit_type = 'volume'


    return [parsed_unit, unit_type]

print(parse_unit('l'))


        
def convert_units(new_unit, new_unit_type,  database_unit, database_unit_type):
    if(new_unit_type == database_unit_type):
        weight_conversion = [['grams','kilograms', .001], ['grams','pound', 0.002], ['grams','ouce', 0.035],
                        ['kilograms','grams', 1000],['kilograms','pound', 2.205],['kilograms','ouce', 35.274],
                        ['pound','grams', 453.592],['pound','kilograms', 0.454],['pound','ouce', 16],
                        ['ouce','grams', 28.350],['ouce','kilograms', 0.028],['ouce','pound', 0.063]]
        spoon_conversion = [['teaspoon','tablespoon', .33], ['tablespoon','teaspoon', 3]]
        volume_conversion = [['cup','liter', .237], ['cup','fluid_oz', 8], ['cup','ml', 236.588],['cup','gallon', .063],
                            ['liter','cup', 4.227], ['liter','fluid_oz', 33.814], ['liter','ml', 1000],['liter','gallon', .264],
                            ['fluid_oz','cup', .125], ['fluid_oz','liter', .003], ['fluid_oz','ml', 29.574],['fluid_oz','gallon', .007],
                            ['ml','cup', .004], ['ml','liter', .001], ['ml','fluid_oz', .034],['ml','gallon', .0002],
                            ['gallon','cup', 16], ['gallon','liter', 3.785], ['gallon','fluid_oz', 128],['gallon','ml', 3785.41]]
        if(new_unit_type == 'weight'):
            for i in range(len(weight_conversion)):
                if(new_unit == weight_conversion[i][0] and database_unit == weight_conversion[i][1]):
                    return weight_conversion[i][2]
        if(new_unit_type == 'spoon'):
            for i in range(len(spoon_conversion)):
                if(new_unit == spoon_conversion[i][0] and database_unit == spoon_conversion[i][1]):
                    return spoon_conversion[i][2]
        if(new_unit_type == 'volume'):
            for i in range(len(volume_conversion)):
                if(new_unit == volume_conversion[i][0] and database_unit == volume_conversion[i][1]):
                    return volume_conversion[i][2]
    
    else:
        return 0
    


print(convert_units('grams', 'weight', 'kilograms', 'weight'))