from bs4 import BeautifulSoup
from urllib import request

sample_recipe_url = "https://www.allrecipes.com/recipe/22849/beef-tacos/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%202"

# Helper Functions

# Takes in url string, returns its corresponding BeautifulSoup object containing the page's html.
# Note: to view html, use prettify() function on get_html's output instead of usual print function.
def get_html(url):
    http_object = request.urlopen(url)
    return BeautifulSoup(http_object,'html.parser')

# Takes in BeautifulSoup object, returns array of ingredient strings.
def get_ingredients(html):
    ingredients = []
    ingredient_tags = html.find_all(itemprop="recipeIngredient")
    for tag in ingredient_tags:
        ingredients.append(tag.contents[0])
    return ingredients

# Takes in BeautifulSoup object, returns array of direction strings.
def get_directions(html):
    directions = []
    direction_tags = html.find_all(class_ = 'recipe-directions__list--item')
    # print(direction_tags)
    for tag in direction_tags:
        text = tag.contents
        if text:
            text = str(text[0])
            text = text[0:text.find("\n")]
            directions.append(text)
    return directions

def get_title(html):
    return html.find_all(id="recipe-main-content")[-1].contents[0]

# Main Function

# Input: AllRecipes URL
# Output: dictionary with two keys, "ingredients" and "directions", mapping to two arrays. Each array consists of strings.

def get_ingredients_and_directions(url):
    recipe_dictionary = {}
    # page = input("Provide AllRecipes.com URL... \n")
    bs_html = get_html(url)
    recipe_dictionary["ingredients"] = get_ingredients(bs_html)
    recipe_dictionary["directions"] = get_directions(bs_html)
    recipe_dictionary["title"] = get_title(bs_html)
    return recipe_dictionary
