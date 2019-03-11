import re
import spacy

from METHODS import METHODS
from fuzzywuzzy import fuzz

nlp = spacy.load('en_core_web_sm')

test_ingredients = ['18 medium taco shells','2 pounds lean ground beef','1 (14 ounce) bottle ketchup','1 (8 ounce) package shredded Cheese','1 large tomato, diced','1 cup iceberg lettuce, shredded', '3 1/4 cups fusilli pasta','2 tablespoons butter','2 tablespoons all-purpose flour','2 cups milk','1 1/2 cups shredded Cheddar cheese, divided','3 teaspoons lemon juice','1/2 teaspoon mustard powder',' salt and ground black pepper to taste','15 ounces tuna packed in water, drained and flaked','1/4 cup dry bread crumbs']

ingred1 = ['18 medium taco shells','2 pounds lean ground beef','1 (14 ounce) bottle ketchup','1 (8 ounce) package shredded Cheese','1 large tomato, diced','1 cup iceberg lettuce, shredded']
directions1 = ['Preheat oven to 375 degrees F (190 degrees C).',
          'Warm taco shells for 5 minutes on the center rack in the preheated oven.',
          'In a medium skillet over medium high heat, brown the beef. Halfway through browning, pour in ketchup. Stir well and let simmer for 5 minutes.',
          'Spoon the meat mixture into the warm taco shells and top with Cheddar cheese. Return the filled taco shells to the preheated oven and bake until cheese is melted. Top each taco with a little tomato and lettuce.']

MEAT_SPECIFIC_VERBS = [ 'trim', 'trimmed']

def find_nouns(doc):
    nouns = []
    for tok in [tok for tok in doc if tok.dep_ == 'compound' and tok.pos_ != 'VERB']: # Get list of compounds in doc
        noun = doc[tok.i: tok.head.i + 1]
        nouns.append(str(noun))
    for tok in doc:
        if tok.pos_ == "NOUN" and len(tok.text) > 2:
            nouns.append(str(tok))
    return nouns


class Ingredient:
    def __init__(self, qty, unit, item, comments = None, qty_details = None, additional_prep = None):
        self.qty = qty
        self.qty_details = qty_details
        self.unit = unit
        self.item = item
        self.comments = comments
        self.additional_prep = additional_prep

    def show(self):
        print(' ')
        print('qty: ',self.qty,
              '\nqty_details: ',self.qty_details,
              '\nunit: ',self.unit,
              '\nitem: ',self.item,
              '\ncomment: ',self.comments, '\n\n')
        print(' ')
        print('--------------------------------')

UNITWORDS = set(['can','jar','pound','ounce','cup','packet', 'package', 'bottle','pinch','teaspoon','tablespoon','head','bunch','bundle','leaves','leaf','leave','sprig','piece','spoonful','pint','quart','gallon','stalk','spear','sheet','bar','cube','block','loaf','wheel','slice','ear','pod','clove','cluster'])
TOOLS = set(['pan','pot','oven','bowl','blender','wok','skillet','fryer','grill','steamer','cooker','range','maker','iron'])
TIME = set(['hour','minute','second','overnight'])
METHODS = set(METHODS)

def cut_s(string):
    s = string
    if s.endswith('s'): s = s[:-1]
    return(s)

def str_to_frac(string):
    t = string.split('/')
    return round(int(t[0])/int(t[1]),2)

def parse_additional_prep(item):
    if ',' in item:
        comment = item.split(',')[-1]
        doc = nlp(comment)
        for tok in doc:
            if tok.text in MEAT_SPECIFIC_VERBS:
                return ''
            if tok.pos_ == 'VERB':
                return ',' + comment
    return ''



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
        if qty == 0:
            qty = ''

        line = re.sub('[0-9]+\s*[^A-Za-z]*', '', line)

        # look for unit words
        if cut_s(line.split()[0]) in UNITWORDS:
            unit = line.split()[0]
            line = ' '.join(line.split()[1:])

        item = line
        # # split string on ',' for item and comment
        # if re.search('to taste', line):
        #     line = re.sub('to taste', ' ', line)
        #     comments += 'to taste'
        # line = line.split(',')
        # item = line[0]
        # try:
        #     comments += line[1]
        # except: pass
        additional_prep = parse_additional_prep(line)


        parsed_ingreds.append(Ingredient(qty,unit,item,comments,qty_details, additional_prep = additional_prep))

    return(parsed_ingreds)


# parsed = parse_ingredients(test_ingredients)

# for i in parsed:
#     i.show()

class Main_step:
    def __init__(self):
        self.source = None
        self.substeps = None

    def show(self):
        print("----------MAIN STEP--------------\n")
        print("Source: ", self.source)
        print(' ')
        for ss in self.substeps:
            ss.show()


class Sub_step:
    def __init__(self, ingredients = None, tools=None, time=None, method=None,source = None):
        self.source = source
        self.method = method
        self.ingredients= ingredients
        self.tools = tools
        self.time = time

    def show(self):
        print("     ----------SUB STEP--------------\n")
        print('     source: ', self.source)
        print('     method: ', self.method)
        print('     ingredients: ', self.ingredients)
        print('     tools: ', self.tools)
        print('     time: ', self.time)
        print(' ')

# INGREDS = parse_ingredients(ingreds)

def split_into_substeps(directions):
    split_steps = []

    for step in directions:
        main = Main_step()
        main.source = step
        parsed_substeps = []

        for substep in step.split('.')[:-1]:
            ss_obj = Sub_step()
            ss_obj.source = substep
            parsed_substeps.append(ss_obj)

        main.substeps = parsed_substeps
        split_steps.append(main)
    return split_steps

def substeps_with_addons(directions, ingredient_objs):
    split_steps = []
    ingredient_nouns = sorted(set([i.item for i in ingredient_objs]), key=len)

    for step in directions:
        main = Main_step()
        main.source = step
        parsed_substeps = []

        for substep in step.split('.')[:-1]:
            #actual step
            ss_obj = Sub_step()
            ss_obj.source = substep
            
            
            nouns = []
            doc = nlp(substep)
            nouns += find_nouns(doc)
        
            sorted_nouns = sorted(set(nouns), key=len, reverse=True)
            
            #ingredients in each step
            mappings = []
            for noun in sorted_nouns:
                for i in ingredient_nouns:
                    if fuzz.partial_ratio(noun, i) > 90 and len(noun) <= len(i):
                        mappings.append(noun)
            
            ss_obj.ingredients = mappings
            
            #find tools
            tools = []
            for word in substep.split():
                if cut_s(word).lower() in TOOLS:
                    tools.append(word)
            ss_obj.tools = tools
            
            #time
            time = []
            for i in range(len(substep.split())):
                word = substep.split()[i].lower()
                if cut_s(word) in TIME:
                    if word == 'overnight':
                        time.append('overnight')
                    else:
                        prev = ''
                        try:
                            prev = substep.split()[i-1]
                        except: 
                            prev = 'a couple'
                        time.append(prev + ' ' + word)
            ss_obj.time = time
            
            methods = []
            for word in substep.split():
                
                if word.capitalize() in METHODS:
                    methods.append(word)
            ss_obj.method = methods
            
            parsed_substeps.append(ss_obj)

        main.substeps = parsed_substeps
        split_steps.append(main)
    return split_steps

def compute_ingredient_name_mappings(ingredient_objs, steps):
    ingredient_nouns = sorted(set([i.item for i in ingredient_objs]), key=len)
    nouns = []
    for step in steps:
        for ss in step.substeps:
            doc = nlp(ss.source)
            nouns += find_nouns(doc)

    sorted_nouns = sorted(set(nouns), key=len, reverse=True)

    mappings = []
    for noun in sorted_nouns:
        for i in ingredient_nouns:
            if fuzz.partial_ratio(noun, i) > 90 and len(noun) <= len(i):
                mappings.append((noun, i))
    return mappings
