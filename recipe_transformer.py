import human_readable
import parsers2
import fetch_page
from pprint import pprint
import transforming

ingred2 = ['3 1/4 cups fusilli pasta','2 tablespoons butter','2 tablespoons all-purpose flour','2 cups milk','1 1/2 cups shredded Cheddar cheese, divided','3 teaspoons lemon juice','1/2 teaspoon mustard powder',' salt and ground black pepper to taste','15 ounces tuna packed in water, drained and flaked','1/4 cup dry bread crumbs']
directions2 = ['Preheat the oven to 350 degrees F (175 degrees C). ',
           'Bring a large pot of lightly salted water to a boil. Cook fusilli in the boiling water, stirring occasionally, until tender yet firm to the bite, about 12 minutes. ',
           'Meanwhile, melt butter in a saucepan over medium heat. Whisk in flour, stirring constantly for about 1 minute. Remove from heat and gradually pour in milk, whisking constantly the entire time to avoid lumps from forming. Return to heat and cook, stirring constantly, until slightly thickened, about 2 minutes. Stir in 1/2 of the Cheddar cheese. Add lemon juice, mustard powder, salt, and pepper and mix well. ',
           'Drain fusilli and fold into the sauce. Mix in tuna. Pour mixture into an 8-inch casserole dish and sprinkle with breadcrumbs. Top with remaining Cheddar cheese. ',
           'Bake in the preheated oven until cheese is melted and golden, about 30 minutes.' ]

ingred1 = ['18 medium taco shells','2 pounds lean ground beef','1 (14 ounce) bottle ketchup','1 (8 ounce) package shredded Cheddar cheese','1 large tomato, diced','1 cup iceberg lettuce, shredded']
directions1 = ['Preheat oven to 375 degrees F (190 degrees C).',
          'Warm taco shells for 5 minutes on the center rack in the preheated oven.',
          'In a medium skillet over medium high heat, brown the beef. Halfway through browning, pour in ketchup. Stir well and let simmer for 5 minutes.',
          'Spoon the meat mixture into the warm taco shells and top with Cheddar cheese. Return the filled taco shells to the preheated oven and bake until cheese is melted. Top each taco with a little tomato and lettuce.']


recipe_url = "https://www.allrecipes.com/recipe/22849/beef-tacos/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%202"  #beef tacos
# recipe_url = "https://www.allrecipes.com/recipe/223042/chicken-parmesan/?internalSource=hub%20recipe&referringContentType=Search"  #chicken parm

recipe_url = "https://www.allrecipes.com/recipe/230857/easy-tuna-patties/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%208" #tuna patties

# recipe_url = "https://www.allrecipes.com/recipe/50795/grilled-tropical-tuna-steaks/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%204" # tuna steaks

# recipe_url = "https://www.allrecipes.com/recipe/23852/creamy-chicken-and-wild-rice-soup/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%2010" #chicken cream soup

# recipe_url = "https://www.allrecipes.com/recipe/100606/beef-bulgogi/"  #beef bulgogi

# recipe_url = "https://www.allrecipes.com/recipe/45641/roasted-rack-of-lamb/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%202" #lamb chops

# recipe_url = "https://www.allrecipes.com/recipe/163001/bourbon-mango-pulled-pork/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%2019" # pulled pork

# recipe_url = "https://www.allrecipes.com/recipe/222979/chicken-milanese/?internalSource=recipe%20hub&referringContentType=Search&clickId=cardslot%2072" #chicken milansese

# recipe_url = "https://www.allrecipes.com/recipe/202804/baked-tuna-crab-cakes/?internalSource=rotd&referringContentType=Homepage&clickId=cardslot%201" #tuna cakes

# recipe_url = input("Please provide a recipe url from AllRecipes.com:")

recipe = fetch_page.get_ingredients_and_directions(recipe_url)




 #  API hookup -> recipe['ingredients'], recipe['directions']

# recipe = {}
# recipe['ingredients'] = ingred1
# recipe['directions'] = directions1



ingredients = parsers2.parse_ingredients(recipe['ingredients'])
steps = parsers2.split_into_substeps(recipe['directions'])

mappings = parsers2.compute_ingredient_name_mappings(ingredients, steps)

ingredients, steps = transforming.transform_ingredients(mappings, ingredients, steps, 'to_vegetarian')
transformation_name = 'Vegetarian'

ingredient_strs, step_strs = human_readable.reassemble(ingredients, steps)

print("-----------------------------------")

 #print original form
human_readable.human_readable(recipe['ingredients'], recipe['directions'])

print("V V V V V V V V V V V V V V V V V V V V V V V V V V V V\n\n")
#print final form
print(recipe['title'] + ' --> ' + transformation_name + '\n\n')

human_readable.human_readable(ingredient_strs, step_strs)
