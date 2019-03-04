from parsers2 import *
import random

ALWAYS_REPLACE_THESE_VEGETARIAN = [ 'meat', 'fish' ]

#Template key --> (item_to_remove, item_to_replace_with(long version), item_to_replace_with(short version), [prep_steps], [finshing_steps])

VEGETARIAN = [
    ('ground beef', 'tofu bricks', 'tofu', ['Place tofu bricks between two plates for 30 minutes until drained, then mash into a fine crumble', 'second prep step'], ['finishing step']),
    ('cheddar cheese', 'synthetic margarine', 'margarine', [], [])
]

HEALTHY = [
    ('vegetable oil', 'olive oil', 'olive oil', [], []),
    ('canola oil', 'olive oil', 'olive oil', [], []),
    ('butter', 'unsalted butter', 'butter', [], [])
]

IN_A_RUSH = [ 'aggressively', 'hastily', 'belligerently' ]

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

def replace_adverbs(INGREDIENTS, steps, replacements=IN_A_RUSH):
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

def transform_ingredients(mappings, ingredients, steps, style):
    if style == 'vegetarian':
        return sub(mappings, ingredients, steps, VEGETARIAN)
    if style == 'healthy':
        return sub(mappings, ingredients, steps, HEALTHY)
    if style == 'to_korean':
        pass
    if style == 'in_a_rush':
        return replace_adverbs(ingredients, steps, IN_A_RUSH)
