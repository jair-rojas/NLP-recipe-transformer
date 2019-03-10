import human_readable
import parsers2
import fetch_page
from pprint import pprint
import transforming
from koreanize import koreanize
from healthy import to_unhealthy
from healthy import to_healthy


def find_input():
    switch = input('Please input number corresponding to desired transformation: ')
    good = 0
    while good != 1:
        try:
            switch = int(switch)
        except:
            pass
        if isinstance(switch,int):
            if (switch < 1) or (switch > 9):
                switch = input('Error: Input out of range. Please input number corresponding to desired transformation: ')
            else:
                good = 1
        else:
            switch = input('Error: Input was not a number. Please input number corresponding to desired transformation: ')
    return(switch)


#recipe_url = "https://www.allrecipes.com/recipe/22849/beef-tacos/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%202"  #beef tacos
# recipe_url = "https://www.allrecipes.com/recipe/223042/chicken-parmesan/?internalSource=hub%20recipe&referringContentType=Search"  #chicken parm
def call_api(recipe_url = None):
    if recipe_url == None:
        recipe_url = input("Please provide a recipe url from AllRecipes.com: ")

    recipe = fetch_page.get_ingredients_and_directions(recipe_url)

    ingredients = parsers2.parse_ingredients(recipe['ingredients'])
    steps = parsers2.split_into_substeps(recipe['directions'])
    mappings = parsers2.compute_ingredient_name_mappings(ingredients, steps)
    transformation_name = 'whoops'

    print('\n-----------------------------------')
    print('Available transformations:')
    print('1. To Vegetarian')
    print('2. From Vegetarian')
    print('3. To Healthy')
    print('4. Unhealthy')
    print('5. To Korean')
    print('6. To Easy')
    print('7. To Very Easy')
    print('8. To Stir Fry')
    print('9. Hell\'s Kitchen')
    switch = find_input()


    if switch == 1:
        ingredients, steps = transforming.transform_ingredients(mappings,ingredients,steps,'to_vegetarian')
        transformation_name = 'Vegetarian'
    if switch == 2:
        ingredients, steps = transforming.transform_ingredients(mappings,ingredients,steps,'from_vegetarian')
        transformation_name = 'Meat'
    if switch == 3:
        ingredients, steps = to_healthy(mappings,ingredients,steps)
        transformation_name = 'Healthy'
    if switch == 4:
        ingredients, steps = to_unhealthy(mappings,ingredients,steps)
        transformation_name = 'Unhealthy'
    if switch == 5:
        ingredients, steps = koreanize(mappings,ingredients,steps)
        transformation_name = 'Korean'
    if switch == 6:
        ingredients, steps = transforming.transform_ingredients(mappings,ingredients,steps,'to_easy')
        transformation_name = 'Easy'
    if switch == 7:
        ingredients, steps = transforming.transform_ingredients(mappings,ingredients,steps,'to_very_easy')
        transformation_name = 'Very Easy'
    # if switch == 8:
    #     ingredients, steps = transforming.transform_ingredients(mappings,ingredients,steps,'stir_fry')
    #     transformation_name = 'Stir Fry'
    if switch == 9:
        ingredients, steps = transforming.transform_ingredients(mappings,ingredients,steps,'hells_kitchen')
        transformation_name = 'Agressive adverbs'


    #ingredients, steps = transforming.transform_ingredients(mappings, ingredients, steps, style)

    ingredient_strs, step_strs = human_readable.reassemble(ingredients, steps)


    print("-----------------------------------")

     #print original form
    print('Original Recipe: ')
    human_readable.human_readable(recipe['ingredients'], recipe['directions'])

    print("V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V\n")
    #print final form
    print('Transformation:\n')
    print(recipe['title'] + ' --> ' + transformation_name + '\n')
    human_readable.human_readable(ingredient_strs, step_strs)

    again = 0
    while again != -1:
        again = input('Would you like to do another transformation on the original recipe? Y/N: ')
        if again.lower() == 'y':
            call_api(recipe_url)
            again = 1
            return
        if again.lower() == 'n':
            again = 1
            return
        else:
            print('Error: input was not "Y" or "N"')

call_api()
