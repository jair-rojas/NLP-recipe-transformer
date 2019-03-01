import re
import spacy

nlp = spacy.load('en_core_web_sm')

test_ingredients = ['18 medium taco shells','2 pounds lean ground beef','1 (14 ounce) bottle ketchup','1 (8 ounce) package shredded Cheese','1 large tomato, diced','1 cup iceberg lettuce, shredded', '3 1/4 cups fusilli pasta','2 tablespoons butter','2 tablespoons all-purpose flour','2 cups milk','1 1/2 cups shredded Cheddar cheese, divided','3 teaspoons lemon juice','1/2 teaspoon mustard powder',' salt and ground black pepper to taste','15 ounces tuna packed in water, drained and flaked','1/4 cup dry bread crumbs']

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

def cut_s(string):
    s = string
    if s.endswith('s'): s = s[:-1]
    return(s)

def str_to_frac(string):
    t = string.split('/')
    return int(t[0])/int(t[1])



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


parsed = parse_ingredients(test_ingredients)

for i in parsed:
    i.show()
