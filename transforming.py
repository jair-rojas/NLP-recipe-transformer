from parsers2 import *

ALWAYS_REPLACE_THESE = [ 'meat', 'fish' ]

#Template key --> (item_to_remove, item_to_replace_with(long version), item_to_replace_with(short version), [prep_steps], [finshing_steps])

VEGETARIAN = [
    ('ground beef', 'tofu bricks', 'tofu', ['Place tofu bricks between two plates for 30 minutes until drained, then mash into a fine crumble', 'Profit???'], ['Serve on a recycled paper plate']),
    ('cheddar cheese', 'synthetic margarine', 'margarine', [], [])
]

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

def transform_ingredients(mappings, ingredients, steps, style):
    if style == 'vegetarian':
        return sub(mappings, ingredients, steps, VEGETARIAN)
