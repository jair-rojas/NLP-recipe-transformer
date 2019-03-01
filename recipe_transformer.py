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

ingred1 = ['18 medium taco shells','2 pounds lean ground beef','1 (14 ounce) bottle ketchup','1 (8 ounce) package shredded Cheese','1 large tomato, diced','1 cup iceberg lettuce, shredded']
directions1 = ['Preheat oven to 375 degrees F (190 degrees C).',
          'Warm taco shells for 5 minutes on the center rack in the preheated oven.',
          'In a medium skillet over medium high heat, brown the beef. Halfway through browning, pour in ketchup. Stir well and let simmer for 5 minutes.',
          'Spoon the meat mixture into the warm taco shells and top with Cheddar cheese. Return the filled taco shells to the preheated oven and bake until cheese is melted. Top each taco with a little tomato and lettuce.']


# sample_recipe_url = "https://www.allrecipes.com/recipe/22849/beef-tacos/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%202"
#
# recipe = fetch_page.get_ingredients_and_directions(sample_recipe_url)

 #  API hookup -> recipe['ingredients'], recipe['directions']

ingredients = parsers2.parse_ingredients(ingred1)
steps = parsers2.split_into_substeps(directions1)

mappings = parsers2.compute_ingredient_name_mappings(ingredients, steps)

ingredients, steps = transforming.sub(mappings, ingredients, steps)

ingredient_strs, step_strs = human_readable.reassemble(ingredients, steps)

human_readable.human_readable(ingredient_strs, step_strs)
