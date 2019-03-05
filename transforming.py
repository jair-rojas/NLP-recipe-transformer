from parsers2 import *
import random

ALWAYS_REPLACE_THESE_VEGETARIAN = [ 'meat', 'fish' ]

#Template key --> (item_to_remove, item_to_replace_with(long version), item_to_replace_with(short version), [prep_steps], [finshing_steps])

TO_VEGETARIAN = [
    ('ground beef', 'tofu bricks', 'tofu', ['Place tofu bricks between two plates for 30 minutes until drained, then mash into a fine crumble', 'second prep step'], ['finishing step']),
    ('cheddar cheese', 'synthetic margarine', 'margarine', [], [])
]

FROM_VEGETARIAN = [

]

HEALTHY = [
    ('vegetable oil', 'olive oil', 'olive oil', [], []),
    ('canola oil', 'olive oil', 'olive oil', [], []),
    ('butter', 'unsalted butter', 'butter', [], [])
]

UNHEALTHY = [
    ('olive oil', 'vegetable oil', 'vegetable oil', [], []),
    ('butter', 'salted butter', 'butter', [], []),
    ('salt and pepper', 'lots of salt and pepper', 'salt and pepper', [], [])
]

HELLS_KITCHEN = [ 'aggressively', 'hastily', 'belligerently' ]

def show_mappings(mappings):
    for m in mappings:
        print(m[0], '--->', m[1])

def swap_ingredient(substitute, original, steps):
    for s in steps:
        for ss in s.substeps:
            ss.source = re.sub(original, substitute, ss.source)
    return steps

def add_prep_steps(steps, strs):
    prep = []
    for str in strs:
        main = Main_step()
        main.substeps = [Sub_step(source=str)]
        prep.append(main)
    return prep + steps

def add_finishing_steps(steps, strs):
    finish = []
    for str in strs:
        main = Main_step()
        main.substeps = [Sub_step(source=str)]
        finish.append(main)
    return steps + finish

#make substitutions based on templates
def sub(mappings, ingredients, steps, templates):
    show_mappings(mappings)
    for template in templates:
        for i in ingredients:

            if fuzz.partial_ratio(template[0], i.item.lower()) > 90: #matches first word of template to an ingredient
                print(i.item)
                i.item = template[1]
                for m in mappings:
                    if fuzz.partial_ratio(template[0], m[1].lower()) > 90:  #matches long name in mappings
                        steps = swap_ingredient(template[2], m[0], steps) #swap short names in directions
                steps = add_prep_steps(steps, template[3])
                steps = add_finishing_steps(steps, template[4])
    for step in steps:
        step.show()
    for i in ingredients:
        i.show()
    return ingredients, steps

def replace_adverbs(INGREDIENTS, steps, replacements=HELLS_KITCHEN):
    for step in steps:
        for ss in step.substeps:
            doc = nlp(ss.source)
            ss.source = ''
            for tok in doc:
                if tok.pos_ == "ADV" and tok.head.pos_ == "VERB":
                    # tok.text = replacements[random.randint(0,len(replacements)-1)]
                    ss.source += replacements[random.randint(0,len(replacements)-1)] + tok.whitespace_
                else:
                    ss.source += tok.text + tok.whitespace_
    return INGREDIENTS, steps

def pwords(doc):
    for token in doc:
        print(token.text, token.pos_, token.dep_)

def remove_descriptors(ingredient):
    doc = nlp(ingredient.item)
    base_ingredient = ''
    found_start = False
    print("---------------------------")
    print(ingredient.item)
    pwords(doc)
    for tok in doc:
        if tok.pos_ == 'NOUN' or tok.pos_ == 'PROPN':
            base_ingredient += tok.text + tok.whitespace_
            found_start = True
        elif tok.text.lower() == 'and' and found_start == True:
            base_ingredient += tok.text + tok.whitespace_
        elif tok.pos_ == 'PUNCT':
            base_ingredient += tok.whitespace_
        elif found_start == True:
            break
    ingredient.item = base_ingredient
    print(base_ingredient)
    return ingredient

def to_easy(mappings, ingredients, steps):
    ingredients = [remove_descriptors(i) for i in ingredients]
    # for i in ingredients:
    #     i.show()
    return ingredients, steps

def transform_ingredients(mappings, ingredients, steps, style):
    if style == 'to_vegetarian':
        return sub(mappings, ingredients, steps, TO_VEGETARIAN)
    if style == 'from_vegetarian':
        return sub(mappings, ingredients, steps, FROM_VEGETARIAN)

    if style == 'healthy':
        return sub(mappings, ingredients, steps, HEALTHY)
    if style == 'unhealthy':
        return sub(mappings, ingredients, steps, UNHEALTHY)

    if style == 'to_easy':
        return to_easy(mappings, ingredients, steps)

    if style == 'to_korean':
        pass
    if style == 'hells kitchen':
        return replace_adverbs(ingredients, steps, HELLS_KITCHEN)

    print("No transform specified")
