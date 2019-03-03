from parsers2 import *
from transforming import *


#new--------------------------------------------------
HERBS = ['oregano','basil','parsley','dill','scallion','green onion','chili','cumin','paprika']

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
                                string[idx] = 'scallion,'
                            else:
                                string[idx] = ''
                        if word.lower() == 'match': 
                            if indicator == 0:
                                indicator = 1
                                string[idx] = 'scallion'
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
    ('sauce','gochu-jang','gochu-jang',[],[]),
    (HERBS, 'scallion','scallion',[],[]),
    ('ham','spam','spam',[],[]),
    ('wine','rice wine','rice wine',[],[]),
]
def koreanize(mappings, ingredients, steps):
    sauce = KOREAN[0]
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
    ingredients.append(Ingredient(1,'jar','gochu-jang',))
            
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
    steps = check_matches(steps,'scallion')
    for i in herbs:
        ingredients.remove(i)
    if scal_ind == 1:
        print('scallion')
        ingredients.append(Ingredient(1,'bunch','scallions','finely chopped'))
            
    
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
        steps = add_finishing_steps(steps,'Serve with side of kimchi and dollop of gochujang.')
        ingredients.append(Ingredient(1,'tub','kimchi'))
        ingredients.append(Ingredient(1,'jar','gochujang'))

    return(ingredients,steps)


