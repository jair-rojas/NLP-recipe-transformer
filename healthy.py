from parsers2 import *
from transforming import *
import re

HEALTHY = [('white rice','quinoa','quinoa',[],[]),
           ('vegetable oil','olive oil','oil',[],[]),
           ('butter','coconut oil','oil',[],[]),
           ('sour cream','greek yogurt','yogurt',[],[]),
           ('flour','coconut flour','flour',[],[]),
           ('sugar','stevia','stevia',[],[]),
           #('salt','himalayan salt','himalayan salt',[],[]),
           ('butter','margarine','margarine',[],[]),
           ('bacon', 'lean ham', 'ham',[],[]),
           ('pork','lean chicken breast','chicken',[],[]),
           ('dressing', 'dressing','dressing',[],[])]



def to_healthy(mappings, ingredients, steps):
    avocado = 0
    for i in ingredients:
        if re.search('salt', i.item):
            i.item = re.sub('salt','himalayan salt', i.item)
        if re.search('iceberg', i.item):
            i.item = re.sub('iceberg','romaine',i.item)
        if re.search('milk', i.item):
            i.item = re.sub('milk','almond milk',i.item)
        if re.search('flour', i.item):
            i.item = re.sub('flour','coconut flour',i.item)
        if re.search('avocado',i.item):
            avocado = 1
    for s in steps:
        for ss in s.substeps:
            if re.search('salt', ss.source):
                ss.source = re.sub('salt','himalayan salt', ss.source)
            if re.search('iceberg', ss.source):
                ss.source = re.sub('iceberg','romaine',ss.source)
            if re.search('milk', ss.source):
                ss.source = re.sub('milk','almond milk',ss.source)
            if re.search('flour', ss.source):
                ss.source = re.sub('flour','coconut flour', ss.source)

    if avocado == 0:
        steps = add_finishing_steps(steps,['Serve with sliced avocado'])
        ingredients.append(Ingredient(1,'','avocado'))

    sauce = HEALTHY[-1]
    #find the sauces
    transform = 0
    ingred_sauces = []
    for i in ingredients:
        if fuzz.partial_ratio(sauce[0], i.item.lower()) > 90: #matches first word of template to an ingredient
            transform = 1
            ingred_sauces.append(i)
            for m in mappings:
                    if fuzz.partial_ratio(sauce[0], m[1].lower()) > 90:  #matches long name in mappings
                        steps = swap_ingredient(sauce[2], m[0], steps) #swap short names in directions
    for i in ingred_sauces:
        ingredients.remove(i)
    if transform == 1:
        ingredients.append(Ingredient(1,'cup','olive oil'))
        ingredients.append(Ingredient(.5,'cup','balsamic vinegar'))
        ingredients.append(Ingredient(1,'sprig','parsley'))
        steps = add_prep_steps(steps, ['Prepare dressing by slowly mixing olive oil, balsamic vinegar, and parsley'])

    for template in HEALTHY[:-1]:
        for i in ingredients:
            if fuzz.partial_ratio(template[0], i.item.lower()) > 90: #matches first word of template to an ingredient
                transform = 1
                #print(i.item)
                i.item = template[1]
                for m in mappings:
                    if fuzz.partial_ratio(template[0], m[1].lower()) > 90:  #matches long name in mappings
                        steps = swap_ingredient(template[2], m[0], steps) #swap short names in directions
                steps = add_prep_steps(steps, template[3])
                steps = add_finishing_steps(steps, template[4])


    return(ingredients,steps)

                    
VEGETABLES = ['romaine lettuce','spinach','cauliflower','broccoli','cucumber','squash','corn','onion','bell pepper','carrot','zucchini']
UNHEALTHY = [('olive oil','melted butter','butter',['Melt butter by heating in pan or microwave until liquid'],[]),
             ('butter','pork fat','fat',[],[]),
             
]

#unhealthy
def to_unhealthy(mappings, ingredients, steps):
    ranch = 0
    veggies = []
    for i in ingredients:
        #print(i.item)
        if re.search('ranch',i.item):
            ranch == 1
        if re.search('salt', i.item):
            i.item = 'msg'
        for veg in VEGETABLES:
            if fuzz.partial_ratio(i.item, veg.lower()) > 90:
                veggies.append(i)
                    
    for s in steps:
        for ss in s.substeps:
            if re.search('salt', ss.source):
                ss.source = re.sub('salt', 'msg', ss.source)
    
    if len(veggies) > 0:
        if len(veggies) > 1:
            last = veggies[-1].item
            rest = [remove_descriptors(i).item for i in veggies[:-1]]
            if len(rest) > 1:
                rest = [i + ',' for i in rest]
            veggies = rest + ['and'] + [last]
            
        veg_str = ' '.join(veggies)
        steps = add_prep_steps(steps, ['Deep fry ' + veg_str + ' until crispy in deep fryer'])
    
    
    if ranch == 0:                
        steps = add_finishing_steps(steps, ['Top with ranch dressing'])
        ingredients.append(Ingredient(1, "bottle",'ranch'))
    if ranch == 1:
        steps = add_finishing_steps(steps, ['Top with instant ramen flavor packet and mix'])
        ingredients.append(Ingredient(1, "packet",'instant ramen soup base'))
        
    return(ingredients,steps)

