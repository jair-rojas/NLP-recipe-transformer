from parsers2 import *
import random

ALWAYS_REPLACE_THESE_VEGETARIAN = [ 'meat', 'fish', 'beef' ]

#Template key --> (item_to_remove, item_to_replace_with(long version), item_to_replace_with(short version), [prep_steps], [finshing_steps])

TO_VEGETARIAN = [
    ('broth', 'vegetable stock', 'vegetable stock', [], []),

    ('ground beef', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid', 'Mash the drained tofu blocks into a fine crumble'], []),
    ('beef brisket', 'packaged tempeh, thinly sliced', 'tempeh', [], []),
    ('beef', 'packaged tempeh', 'tempeh', [], []),

    ('lamb', 'packaged tempeh', 'tempeh', [], []),

    ('ribs', 'packaged tempeh', 'tempeh', [], []),

    ('pork', 'packaged seitan', 'seitan', [], []),
    ('duck', 'packaged seitan', 'seitan', [], []),
    ('pheasant', 'packaged seitan', 'seitan', [], []),
    ('sheep', 'packaged seitan', 'seitan', [], []),
    ('rabbit', 'packaged seitan', 'seitan', [], []),
    ('venison', 'packaged seitan', 'seitan', [], []),
    ('goose', 'packaged seitan', 'seitan', [], []),

    ('sausage', 'vegeterian sausage', 'vegetarian sausage', [], []),

    ('tuna packed', 'vegan toona', 'toona', [], []),
    ('tuna in water', 'vegan toona', 'toona', [], []),
    ('tuna drained', 'vegan toona', 'toona', [], []),

    ('shrimp', 'vegan immitation shrimp', 'shrimp', [], []),
    ('crab', 'vegan immitation crab', 'crab', [], []),
    ('lobster', 'vegan immitation lobster', 'lobster', [], []),

    ('hot dog', 'vegan immitation hot dog', 'hot dog', [], []),

    ('ham', 'vegan ham', 'vegan ham', [], []),
    ('salami', 'vegan salami', 'vegan salami', [], []),

    ('bacon bits', 'veggie bacon bits', 'bacon bits', [], []),
    ('bacon', 'veggie bacon', 'bacon', [], []),

    ('chicken breasts', 'packages seitan', 'seitan', [], []),
    ('chicken wings', 'tempeh, cut into 1 inch strips', 'tempeh', [], []),
    ('chicken', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),

    ('turkey breasts', 'packages seitan', 'seitan', [], []),
    ('turkey wings', 'tempeh, cut into 1 inch strips', 'tempeh', [], []),
    ('turkey', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),

    ('salmon', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),
    ('cod', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),
    ('tilapia', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),
    ('fish', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),
    ('pollock', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),
    ('carp', 'tofu blocks', 'tofu', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid'], []),



    ('steak', 'tofu blocks', 'tofu steaks', ['Place each block of tofu onto a plate and place another plate on top. Set a 3 to 5 pound weight on top (a container filled with water works well). Press the tofu for 20 to 30 minutes, then drain off and discard the accumulated liquid', 'Slice tofu blocks into steaks'], []),
]

FROM_VEGETARIAN = [
        ('tofu', 'chicken breast', 'chicken', [], []),
        ('seitan', 'skirt steak', 'beef', [], []),
        ('tempeh', 'beef chuck', 'beef', [], []),
        ('bean', 'tuna packed in water, drained', 'tuna', [], []),
        ('lentil', 'tuna packed in water, drained', 'tuna', [], []),
        ('vegetable stock', 'beef broth', 'broth', [], []),
        ('vegan', 'chicken thighs, diced', 'chicken', [], []),
        ('veget', 'chicken thighs, diced', 'chicken', [], []),

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
                i.item = template[1] + i.additional_prep
                for m in mappings:
                    if fuzz.partial_ratio(template[0], m[1].lower()) > 90:  #matches long name in mappings
                        steps = swap_ingredient(template[2], m[0], steps) #swap short names in directions

                        if templates == TO_VEGETARIAN:  #catch indirect references like "meat", "fish"
                            for i in ALWAYS_REPLACE_THESE_VEGETARIAN:
                                steps = swap_ingredient(template[2], i, steps)

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
    # print("---------------------------")
    # print(ingredient.item)
    # pwords(doc)
    for tok in doc:
        if tok.pos_ == 'NOUN' or tok.pos_ == 'PROPN':
            base_ingredient += tok.text + tok.whitespace_
            found_start = True
        elif tok.text.lower() == 'and' and found_start == True:
            base_ingredient += tok.text + tok.whitespace_
            found_start = False
        elif tok.pos_ == 'PUNCT' and found_start == True:
            base_ingredient += tok.whitespace_
        elif found_start == True:
            break
    ingredient.item = base_ingredient
    # print(base_ingredient)
    return ingredient

def to_easy(mappings, ingredients, steps):
    ingredients = [remove_descriptors(i) for i in ingredients]
    # for i in ingredients:
    #     i.show()
    return ingredients, steps

def gather_base_ingredients(mappings):
    base_ingredients = [ mappings[0][0].lower() ]
    for m in mappings[1:]:
        already_in_list = [b for b in base_ingredients if fuzz.partial_ratio(m[0].lower(), b.lower()) > 90]
        if not already_in_list:
            base_ingredients.append(m[0].lower())
    return base_ingredients

def to_very_easy(mappings, ingredients, steps):
    ingredients, steps = to_easy(mappings, ingredients, steps)
    ingredient_base_strs = gather_base_ingredients(mappings)

    step_strs = []
    ingredient_list_str = ''
    for i in ingredient_base_strs[:-1]:
        ingredient_list_str += i + ', '
    ingredient_list_str += 'and ' + ingredient_base_strs[-1]

    step_strs.append('Place ' + ingredient_list_str + ' in a large blender and blend on high until smooth')
    step_strs.append('Pour mixture into a large bowl')
    step_strs.append('Microwave on high for 10 minutes')

    steps = []
    for s in step_strs:
        main = Main_step()
        sub = Sub_step()
        main.substeps = [sub]
        sub.source = s
        steps.append(main)
    return ingredients, steps

def to_stew(mappings, ingredients, steps):
    ingredients, steps = to_easy(mappings, ingredients, steps)
    ingredient_base_strs = gather_base_ingredients(mappings)

    step_strs = []
    ingredient_list_str = ''
    for i in ingredient_base_strs[:-1]:
        ingredient_list_str += i + ', '
    ingredient_list_str += 'and ' + ingredient_base_strs[-1]

    step_strs.append('Place ' + ingredient_list_str + ' in a large stew pot')
    step_strs.append('Fill the rest of the pot with water')
    step_strs.append('Cook over low heat for 4 hours, stirring occasionally')

    steps = []
    for s in step_strs:
        main = Main_step()
        sub = Sub_step()
        main.substeps = [sub]
        sub.source = s
        steps.append(main)
    return ingredients, steps

def transform_ingredients(mappings, ingredients, steps, style):
    if style == 'to_vegetarian':
        return sub(mappings, ingredients, steps, TO_VEGETARIAN)
    if style == 'from_vegetarian':
        ingredients, steps = sub(mappings, ingredients, steps, FROM_VEGETARIAN)
        ingredients.append(Ingredient(2, "tablespoons",'bacon bits'))
        steps = add_finishing_steps(steps, ['Top with bacon bits'])
        return ingredients, steps


    if style == 'to_easy':
        return to_easy(mappings, ingredients, steps)
    if style == 'to_very_easy':
        return to_very_easy(mappings, ingredients, steps)
    if style == 'stew':
        return to_stew(mappings, ingredients, steps)

    if style == 'hells_kitchen':
        return replace_adverbs(ingredients, steps, HELLS_KITCHEN)

    print("\nNo transform specified\n")
