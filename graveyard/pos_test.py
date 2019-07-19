import spacy
from spacy import displacy


nlp = spacy.load('en_core_web_sm')

ingred1 = ['18 medium taco shells',' salt and ground black pepper to taste', '2 pounds lean ground beef','1 (14 ounce) bottle ketchup','1 (8 ounce) package shredded Cheese','1 large tomato, diced','1 cup iceberg lettuce, shredded']
directions1 = ['Preheat oven to 375 degrees F (190 degrees C).',
          'Warm taco shells for 5 minutes on the center rack in the preheated oven.',
          'In a medium skillet over medium high heat, brown the beef. Halfway through browning, pour in ketchup. Stir well and let simmer for 5 minutes.',
          'Spoon the meat mixture into the warm taco shells and top with Cheddar cheese. Return the filled taco shells to the preheated oven and bake until cheese is melted. Top each taco with a little tomato and lettuce.']

directions2 = ['Preheat the oven to 350 degrees F (175 degrees C). ',
           'Bring a large pot of lightly salted water to a boil. Cook fusilli in the boiling water, stirring occasionally, until tender yet firm to the bite, about 12 minutes. ',
           'Meanwhile, melt butter in a saucepan over medium heat. Whisk in flour, stirring constantly for about 1 minute. Remove from heat and gradually pour in milk, whisking constantly the entire time to avoid lumps from forming. Return to heat and cook, stirring constantly, until slightly thickened, about 2 minutes. Stir in 1/2 of the Cheddar cheese. Add lemon juice, mustard powder, salt, and pepper and mix well. ',
           'Drain fusilli and fold into the sauce. Mix in tuna. Pour mixture into an 8-inch casserole dish and sprinkle with breadcrumbs. Top with remaining Cheddar cheese. ',
           'Bake in the preheated oven until cheese is melted and golden, about 30 minutes.' ]


# doc = nlp(directions1[3].split('.')[-3])

# doc = nlp("4 skinless, boneless chicken breast halves")
def pwords(doc):
    for token in doc:
        print(token.text, token.pos_, token.dep_)
# def pchunk(doc):
#     for chunk in doc.noun_chunks:
#         print(chunk.text, chunk.root.text, chunk.root.dep_,
#               chunk.root.head.text)
# def pdep(doc):
#     for token in doc:
#         print(token.text, token.dep_, token.head.text, token.head.pos_, token.pos_,
#           [child for child in token.children])

# def find_nouns(doc):
#     nouns = []
#     for tok in [tok for tok in doc if tok.dep_ == 'compound']: # Get list of compounds in doc
#         noun = doc[tok.i: tok.head.i + 1]
#         nouns.append(noun)
#     for tok in doc:
#         if tok.pos_ == "NOUN":
#             nouns.append(tok)
#     return nouns
#
# print(find_nouns(doc))
# pwords(doc)

doc = nlp("2 cooked, boneless chicken breast halves, shredded")#1 1/2 cups shredded Cheddar cheese, divided. iceberg lettuce, shredded. 15 ounces tuna packed in water, drained and flaked ")
# doc = nlp("2 skinless, boneless chicken breast halves")

# s = ''
# for i in directions2:
#     s += i + '\n '
#
# doc = nlp(s)

pwords(doc)



displacy.serve(doc, style='dep')
