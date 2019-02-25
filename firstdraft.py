# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 16:21:29 2019

@author: georg
"""

import re
import nltk
import spacy
   
class Ingredient:
    def __init__(self, qty, unit, item, comments = None, qty_option = None):
        self.qty = qty
        self.qty_option = qty_option
        self.unit = unit
        self.item = item
        self.comments = comments
    
    def i_print(self):
        print('qty: ',self.qty,
              '\nqty_opt: ',self.qty_option,
              '\nunit: ',self.unit,
              '\nitem: ',self.item,
              '\ncomment: ',self.comments, '\n\n')
        

ingred = ['1 1/2 pounds ground beef','1/4 cup water','1 (1 ounce) packet taco seasoning mix','12 (8 inch) flour tortillas, or more if needed', '1 (14 ounce) can refried beans','3 cups shredded Colby-Jack cheese','1 (8 ounce) jar taco sauce','1 cup shredded Colby-Jack cheese']

UNITWORDS = set(['can','jar','pound','ounce','cup','packet','bottle','pinch'])

def cut_s(string):
    s = string
    if s.endswith('s'): s = s[:-1]
    return(s)

def str_to_frac(string):
    t = string.split('/')
    return int(t[0])/int(t[1])

paren_pat = re.compile(r'\((.*?)\)')
def parse_ingred(ingreds):
    parsed_ingreds = []
    
    for line in ingreds:
        # all the vars we need for Ingredient class
        qty = 0
        qty_opt = ''
        unit = ''
        item = ''
        comments = ''
        
        # look for parentheses, take them out, place whats in them in the qty_option
        if re.search(paren_pat,line):
            qty_opt = re.search(paren_pat,line).group(0)
            qty_opt = qty_opt[1:len(qty_opt)-1]
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
        line = line.split(',')
        item = line[0]
        try:
            comments = line[1]
        except: pass
        
        parsed_ingreds.append(Ingredient(qty,unit,item,comments,qty_opt))
                
    return(parsed_ingreds)


recipe = ['Preheat oven to 375 degrees F (190 degrees C).',
          'Warm taco shells for 5 minutes on the center rack in the preheated oven.',
          'In a medium skillet over medium high heat, brown the beef. Halfway through browning, pour in ketchup. Stir well and let simmer for 5 minutes.',
          'Spoon the meat mixture into the warm taco shells and top with Cheddar cheese. Return the filled taco shells to the preheated oven and bake until cheese is melted. Top each taco with a little tomato and lettuce.']

METHODS = ['top','stir','simmer','mix','spoon','warm','preheat','bake','brown','pour','return']

sentences = []
for i in recipe:
    j = (i.split('.'))
    for y in j:
        if y == '': pass
        else: 
            if y[0] == ' ':
                y = y[1:]
            sentences.append(y)
        
            
for i in sentences[1:2]:
    doc = nlp(sentences[11])
def pwords(doc):
    for token in doc:
        print(token.text, token.pos_, token.dep_)
def pchunk(doc):
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
              chunk.root.head.text)
def pdep(doc):
    for token in doc:
        print(token.text, token.dep_, token.head.text, token.head.pos_, token.pos_,
          [child for child in token.children])


# recipe assumptions: they all start with a verb OR they start with a prep phrase in which case, verb appears after the comma
# and commas only exist if the sentence starts with a prep phrase
def find_ingred(line, ingreds):
    ingred_list = sorted(set([i.item for i in ingreds]), key=len)
    num_overlap = [len(set(line.split()).intersection(set(i.split()))) for i in ingred_list]
    if max(num_overlap) > 0:  #if we're able to match more than one word
        return ingred_list[num_overlap.index(max(num_overlap))]  #grab the first (and thus shortest) award name that matches max(num_overlap) times
    else:
        return None
    
    

class Step:
    def __init__(self, ingreds = None, tools=None, time=None, method=None, method_opt= None):
        self.ingreds= ingreds
        self.tools = tools
        self.time = time
        self.method=method
        self.method_opt = method_opt

def parse_recipe(recipe, ingreds):
    sentences = []
    for i in recipe:
        j = (i.split('.'))
        for y in j:
            if y == '': pass
            else: 
                if y[0] == ' ':
                    y = y[1:]
                sentences.append(y)
            
    sent2 = []
    for i in sentences:
        j = i.split('and')
        for z in range(len(j)):
            y = j[z]
            if y == '': pass
            else:
                if y[0] == ' ':
                    y = y[1:]
                indicator = 0
                for word in y.split():
                    if word.lower() in set(METHODS):
                        indicator = 1
                        break               
                if indicator == 1:
                    sent2.append(y)
                else:
                    if z == 0:
                        sent2.append(y)
                    else:
                        tmp = sent2[-1]
                        sent2 = sent2[:-1]
                        sent2.append(tmp + 'and ' + y)
    sentences = sent2            
    
#    steps = []
#    for line in sentences: 
#        print('working on: ', line)
#        doc = nlp(line)
#        nps = doc.noun_chunks
#        verb = None
#        ingredients = None
#        tool = None
#        for chunk in nps:
#            if chunk.root.head.pos_ != 'ADP':
#                print(chunk.root)
#                verb = chunk.root.head.text
#                if find_ingred(str(chunk.text), ingreds):
#                    ingredients= (find_ingred(str(chunk.text), ingreds))
#                else: 
#                     tool = str(chunk.text)   
#                break
#        steps.append(Step(ingreds = ingredients, method = verb, tools = tool))

        for line in sentences:
            g = line.split(',')
            splits = []
            for j in g:
                prev = 0
                doc = nlp(j)
                for i in range(len(doc)):
                    word = doc[i]
                    if word.pos_ == 'ADP': 
                        splits.append(doc[prev:i])
                        prev = i
                splits.append(doc[prev:])
            
            # identify the verb
            verb = ''
            for s in splits:
                ingred = []
                if s[0].pos_ == 'ADP': pass
                else: 
                    for j in s:
                        
                        if j.pos_ == 'VERB':
                            verb = j
                            break
                        else: pass
            if str(verb) == '':
                for s in splits:
                    if s[0].pos_ == 'ADP': pass
                    else: verb = s[0]
            
            print(splits)
            verbs = [verb]
            stack = [child for child in verb.children ]
            while stack != []:
                for child in stack:
                    stack.remove(child)
                    if child.pos_ == 'VERB':
                        index = 0
                        for s in splits:
                            if child.text in s.text: index = splits.index(s)                        
                        if splits[index][0].pos_ == 'ADP': pass
                        else: 
                            verbs.append(child)
                        for i in child.children:
                            stack.append(i)
            print(line,'-----', verbs)
            
                    
            
            
            
            
            
        
        


nlp = spacy.load('en')
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
for token in doc:
    print(token.text, token.pos_, token.dep_)    

class Parsed_Recipe:
    def __init__(self, ingred_string, recipe_string):
        self.ingredients = parse_ingred(ingred_string)
        self.recipe = parse_recipe(recipe_string)
