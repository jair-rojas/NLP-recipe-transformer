import human_readable
import parsers2
import fetch_page
from pprint import pprint
from transforming import sub
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
            if (switch < 1) or (switch > 5):
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
    
    print('\n-----------------------------------')
    print('Available transformations:')
    print('1. To Vegetarian')
    print('2. From Vegetarian')
    print('3. To Healthy')
    print('4. From Healthy')
    print('5. To Korean\n')
    switch = find_input()
    def transform_ingredients(mappings, ingredients, steps, style):
        if style == 'to_vegetarian':
            return sub(mappings, ingredients, steps, TO_VEGETARIAN)
        if style == 'from_vegetarian':
            return sub(mappings, ingredients, steps, FROM_VEGETARIAN)
    
        if style == 'healthy':
            return sub(mappings, ingredients, steps, HEALTHY)
        if style == 'unhealthy':
            return sub(mappings, ingredients, steps, UNHEALTHY)
    
        if style == 'to_easy':
            return to_easy(mappings, ingredients, steps)
        if style == 'to_very_easy':
            return to_very_easy(mappings, ingredients, steps)
    
        if style == 'to_korean':
            pass
        if style == 'hells kitchen':
            return replace_adverbs(ingredients, steps, HELLS_KITCHEN)
    
        print("No transform specified")
    
    if switch == 1:
        ingredients, steps = sub(mappings,ingredients,steps,'TO_VEGETARIAN')
    if switch == 2:
        ingredients, steps = sub(mappings,ingredients,steps,'FROM_VEGETARIAN')
    if switch == 3:
        ingredients, steps = to_healthy(mappings,ingredients,steps)
    if switch == 4:
        ingredients, steps = to_unhealthy(mappings,ingredients,steps)
    if switch == 5:
        ingredients, steps = koreanize(mappings,ingredients,steps)
    
    
    #ingredients, steps = transforming.transform_ingredients(mappings, ingredients, steps, style)
    
    ingredient_strs, step_strs = human_readable.reassemble(ingredients, steps)
    
    print("-----------------------------------")
    
     #print original form
    print('Original Recipe: ')
    human_readable.human_readable(recipe['ingredients'], recipe['directions'])
    
    print("V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V\n")
    #print final form
    print('Transformation: ')
    human_readable.human_readable(ingredient_strs, step_strs)
    
    again = 0
    while again != -1:
        again = input('Would you like to do another transformation on this recipe? Y/N: ')
        if again == 'Y':
            call_api(recipe_url)
            again = 1
            return
        if again == 'N':
            again = 1
            return
        else:
            print('Error: input was not "Y" or "N"')

call_api()
    