from parsers2 import *
from transforming import *
import random
import re

#new--------------------------------------------------
HERBS = ['oregano','basil','parsley','dill','scallion','green onion','cumin','paprika','mint','ginger']

def check_matches(steps,replacement):
    for s in steps:
        for ss in s.substeps:
            tmp = ss.source
            #print(tmp)
            if len(re.findall('match',tmp)) > 1:
                print(tmp)
                if re.search('and match',tmp):
                    tmp = re.sub('and match',replacement,tmp)
                    tmp = re.sub('match','',tmp)
                    ss.source=tmp
                else:
                    string = tmp.split()
                    indicator = 0
                    for idx in range(len(string)):
                        word = string[idx]
                        if word.lower() == 'match,': 
                            if indicator == 0:
                                indicator = 1
                                string[idx] = replacement+','
                            else:
                                string[idx] = ''
                        if word.lower() == 'match': 
                            if indicator == 0:
                                indicator = 1
                                string[idx] = replacement
                            else:
                                string[idx] = ''
                    string = [x for x in string if x != '']
                    tmp = ' '.join(string)
                    print(tmp)
                    ss.source=tmp
                            
            else:
                ss.source=re.sub('match',replacement,ss.source)
            ss.source=re.sub(' ,','',ss.source)
    return(steps)

KOREAN = [
    [('sauce','gochu-jang','gochu-jang',[],[]),('sauce','soy sauce','soy sauce',[],[])],
    (HERBS, 'scallion and ginger','scallion and ginger',['Slice ginger as thinly as possible. Wash scallions and remove stems. Discard outer layer'],['Sprinkle gochu-garu on top for extra spice']),
    ('sausage','spam','spam',[],[]),
    ('wine','rice wine','wine',[],[]),
    ('olive oil','vegetable oil','oil',[],[])
]
def koreanize(mappings, ingredients, steps):  
    garlic = 0
    chicken = 0
    beef = 0
    pork = 0
    marinate = 0
    for s in steps:
        for ss in s.substeps:
            if re.search('marinade', ss.source):
                marinate = 1
            if re.search('marinate', ss.source):
                marinate = 1
            if re.search('brine', ss.source):
                marinate = 1
                
    for ingred in ingredients:
        if re.search('garlic', ingred.item):
            garlic = 1
        if re.search('chicken', ingred.item):
            chicken  = 1
        if re.search('beef', ingred.item):
            if re.search('broth',ingred.item):pass
            else: beef = 1
        if re.search('pork', ingred.item):
            pork = 1
    
    if garlic == 0:
        steps = add_prep_steps(steps, ['Grill garlic on stove to serve on the side'])
    
    if marinate == 0:
        if chicken == 1:
            steps = add_prep_steps(steps, ['Create marinade by mixing soy sauce, soybean paste, and sesame oil','Marinate chicken in mixture for at least an hour (or overnight)'])
        if beef == 1:
            steps = add_prep_steps(steps, ['Create marinade by mixing soy sauce, soybean paste, and sesame oil','Marinate beef in mixture for at least an hour (or overnight)'])
        if pork == 1:
            steps = add_prep_steps(steps, ['Create marinade by mixing soy sauce, soybean paste, and sesame oil','Marinate pork in mixture for at least an hour (or overnight)'])
        ingredients.append(Ingredient(.5,'cup','soy sauce'))
        ingredients.append(Ingredient(2,'teaspoons','korean soybean paste'))
        ingredients.append(Ingredient(.5,'cup','sesame sauce'))
        
    rand = random.randint(1,2)
    sauce = KOREAN[0][rand-1]
    #find the sauces    
    transform = 0
    ingred_sauces = []
    for i in ingredients:
        if fuzz.partial_ratio(sauce[0], i.item.lower()) > 90: #matches first word of template to an ingredient
            transform = 1
            ingred_sauces.append(i)
            for m in mappings:
                    if fuzz.partial_ratio(sauce[0], m[1].lower()) > 90:  #matches long name in mappings
                        print(m[1])
                        steps = swap_ingredient(sauce[2], m[0], steps) #swap short names in directions
    for i in ingred_sauces:
        ingredients.remove(i)
    if transform == 1:
        ingredients.append(Ingredient(1,'bottle',sauce[1],))
            
    #herbs
    scallion = KOREAN[1]
    scal_ind = 0
    herbs = []
    for i in ingredients:
        for j in scallion[0]:
            if fuzz.partial_ratio(j, i.item.lower()) > 90: #matches first word of template to an ingredient
                transform = 1
                scal_ind= 1
                herbs.append(i)
                for m in mappings:
                    if fuzz.partial_ratio(j, m[1].lower()) > 90:  #matches long name in mappings
                        print(m[1],m[0])
                        steps = swap_ingredient('match', m[0], steps) #swap short names in directions
    steps = check_matches(steps,'scallion and ginger')
    steps = add_prep_steps(steps, scallion[3])
    steps = add_finishing_steps(steps, scallion[4])
    for i in herbs:
        ingredients.remove(i)
    if scal_ind == 1:
        ingredients.append(Ingredient(1,'bunch','scallions','finely chopped'))
        ingredients.append(Ingredient(1,unit= '',item = 'ginger',comments= 'thinly sliced'))
        ingredients.append(Ingredient(1,'teaspoon','gochu-garu'))
            
    
    #other stuff
    for template in KOREAN[2:]:
        for i in ingredients:
            if fuzz.partial_ratio(template[0], i.item.lower()) > 90: #matches first word of template to an ingredient
                transform = 1
                print(i.item)
                i.item = template[1]
                for m in mappings:
                    if fuzz.partial_ratio(template[0], m[1].lower()) > 90:  #matches long name in mappings
                        steps = swap_ingredient(template[2], m[0], steps) #swap short names in directions
                steps = add_prep_steps(steps, template[3])
                steps = add_finishing_steps(steps, template[4])

    #if no transformations so far
    if transform == 0: 
        steps = add_finishing_steps(steps,['Serve with side of kimchi and assorted store-bought banchan.'])
        ingredients.append(Ingredient(1,'tub','kimchi'))
        ingredients.append(Ingredient(1,'plate','banchan','assorted'))
    else:
        steps = add_finishing_steps(steps, ['Serve with side of assorted banchan'])
        ingredients.append(Ingredient(1,'plate','banchan','assorted'))

    return(ingredients,steps)


