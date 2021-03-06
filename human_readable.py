arr1 = [ "2 cups shredded Cheddar cheese", "1 pound ground beef", "1/2 package taco seasoning mix"]
arr2 = [ "Preheat oven to 350 degrees F (175 degrees C). Line 2 baking sheets with parchment paper or silicone mat.",
		 "Spread Cheddar cheese into four 6-inch circles, placed 2 inches apart.",
		 "Bake in the preheated oven until cheese melts and is lightly brown, 6 to 8 minutes."]

from parsers2 import *

# removes any words if they appear twice in a row in a step
# we should try to use this at the very end
# takes in all the steps and spits out all the steps removing duplicates
def remove_dup(steps):
    def remove_comma(string):
        return(re.sub(',', '', string))

    for s in steps:
        for ss in s.substeps:
            split = ss.source.split()
            repeats = []
            for i in range(len(split)):
                word = split[i]
                wordnext = ''
                try:
                    wordnext = split[i+1]
                except:
                    pass
                if word == wordnext:
                    repeats.append(word)
            for i in repeats:
                split.remove(i)
            ss.source = ' ' + ' '.join(split)
    return(steps)


def reassemble(ingredients, steps):
	ingredient_strs = []

	steps = remove_dup(steps)

	for i in ingredients:
		i_str = str(i.qty) + ' '

		if i.qty_details:
			i_str +=  '('+ i.qty_details + ') '

		if i.unit:
			i_str += i.unit + ' '
		i_str += i.item
		ingredient_strs.append(i_str)

	step_strs = []

	for s in steps:
		main_step = ""
		for ss in s.substeps:
			main_step += ss.source + '.'
		step_strs.append(main_step)

	return ingredient_strs, step_strs

# Display the transformed recipe in a human-friendly format.
def human_readable(ingr, dire):
	print("Ingredients:")
	str1 = []
	for i in ingr:
		str1.append("	")
		str1.append(i)
		str1.append("\n")
	print(''.join(str1))

	print("Directions:")
	str2 = []
	step = 1
	for d in dire:
		str2.append("	%d. " % (step))
		str2.append(d)
		str2.append("\n")
		step += 1
	print(''.join(str2))

# human_readable(arr1, arr2)
