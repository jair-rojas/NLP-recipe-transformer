import re
import spacy

nlp = spacy.load('en_core_web_sm')
# test_ingredients = ['18 medium taco shells','2 pounds lean ground beef','1 (14 ounce) bottle ketchup','1 (8 ounce) package shredded Cheese','1 large tomato, diced','1 cup iceberg lettuce, shredded', '3 1/4 cups fusilli pasta','2 tablespoons butter','2 tablespoons all-purpose flour','2 cups milk','1 1/2 cups shredded Cheddar cheese, divided','3 teaspoons lemon juice','1/2 teaspoon mustard powder',' salt and ground black pepper to taste','15 ounces tuna packed in water, drained and flaked','1/4 cup dry bread crumbs']

class Ingredient:
    def __init__(self, qty, unit, item, comments = None, qty_details = None):
        self.qty = qty
        self.qty_details = qty_details
        self.unit = unit
        self.item = item
        self.comments = comments

    def show(self):
        print(' ')
        print('qty: ',self.qty,
              '\nqty_details: ',self.qty_details,
              '\nunit: ',self.unit,
              '\nitem: ',self.item,
              '\ncomment: ',self.comments,)
        print(' ')
        print('--------------------------------')

UNITWORDS = set(['can','jar','pound','ounce','cup','packet','bottle','pinch','teaspoon','tablespoon'])

# Parsing Functions
# Remove 's' character from string
def cut_s(string):
    s = string
    if s.endswith('s'): s = s[:-1]
    return(s)

# Convert to integers
def str_to_frac(string):
    t = string.split('/')
    return int(t[0])/int(t[1])

# Parse important information into class methods
def parse_ingredients(ingreds):
    paren_pat = re.compile(r'\((.*?)\)')

    parsed_ingreds = []
    for line in ingreds:
        # all the vars we need for Ingredient class
        qty = 0
        qty_details = ''
        unit = ''
        item = ''
        comments = ''

        # look for parentheses, take them out, place whats in them in the qty_details
        if re.search(paren_pat,line):
            qty_details = re.search(paren_pat,line).group(0)
            qty_details = qty_details[1:len(qty_details)-1]
            line = re.sub(r'\((.*?)\)', '', line)

   
        # look for numbers, put them in qty
        number = re.search('\d*\s*[^A-Za-z]*', line).group(0)
        for num in number.split():
            if '/' in num:
                num = str_to_frac(num)
            else:
                num = int(num)
            qty = qty + num
        line = re.sub('[0-9]+\s*[^A-Za-z]*', '', line)

   
        # look for unit words
        if cut_s(line.split()[0]) in UNITWORDS:
            unit = line.split()[0]
            line = ' '.join(line.split()[1:])

   
        # split string on ',' for item and comment
        if re.search('to taste', line):
            line = re.sub('to taste', ' ', line)
            comments += 'to taste'
        line = line.split(',')
        item = line[0]
        try:
            comments += line[1]
        except: pass
        parsed_ingreds.append(Ingredient(qty,unit,item,comments,qty_details))
        
    return(parsed_ingreds)

# parsed = parse_ingredients(test_ingredients)
# for i in parsed:
#     i.show()


# Scaling Functions
def scale_ingredient(ingred, scaling_factor):
    new_amount = ingred.qty * scaling_factor
    
    # If new_amount has more than 2 decimals then round to nearest tenth
    str_amount = str(new_amount)
    decimal_digits = str_amount[::-1].find('.')
    if decimal_digits > 2:
        new_amount = round(new_amount, 1)

    # Make units plural or singular
    if new_amount > 1 and ingred.unit.endswith('s') == False and ingred.unit != "":
        ingred.unit += "s"
    elif new_amount <= 1:
        ingred.unit = cut_s(ingred.unit)

    ingred.qty = new_amount

def scale_all(ingreds, steps, scaling_factor):
    for i in ingreds:
        scale_ingredient(i, scaling_factor)
    return ingreds, steps


# Metric Functions
# mL for liquids and grams for solids
to_mL = {"teaspoon": 5, "tablespoon": 15, "cup": 240, "pint": 475, "quart": 950, "gallon": 3800}
to_grams = {"ounce": 28, "pound": 450}
def convert_to_metric(ingred):
    new_amount = 0
    cust_unit = cut_s(ingred.unit)

    mul_factor = 0
    if cust_unit == "":
        pass
    elif cust_unit == "ounce" or cust_unit == "pound":
        ingred.qty *= to_grams[cust_unit]
        ingred.unit = "g"
    else:
        try:
            ingred.qty *= to_mL[cust_unit]
            ingred.unit = "mL"
        except KeyError:
            print("     *Unit below was not accounted for")

def convert_all(ingreds, steps):
    for i in ingreds:
        convert_to_metric(i)
    return ingreds, steps