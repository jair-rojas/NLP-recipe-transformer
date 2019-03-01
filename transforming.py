from parsers2 import *

ALWAYS_REPLACE_THESE = [ 'meat', 'fish' ]

vegetarian = [ ('ground beef', 'finely crushed tofu', 'tofu', '') ]

def show_mappings(mappings):
    for m in mappings:
        print(m[0], '--->', m[1])

def swap_ingredient(substitute, original, steps):
    for s in steps:
        for ss in s.substeps:
            ss.source = re.sub(original, substitute, ss.source)
    return steps

#make substitutions based on templates
def sub(mappings, ingredients, steps):
    show_mappings(mappings)
    template = vegetarian[0]
    for i in ingredients:
        if fuzz.partial_ratio(template[0], i.item) > 95: #matches first word of template to an ingredient
            print(i.item)
            i.item = template[1]
            for m in mappings:
                if fuzz.partial_ratio(template[0], m[1]) > 95:  #matches long name in mappings
                    steps = swap_ingredient(template[2], m[0], steps) #swap short names in directions
    for step in steps:
        step.show()
    for i in ingredients:
        i.show()
    return ingredients, steps
