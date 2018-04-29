import re

light_keywords = ['light.?', 'bulb.?', 'switch(ed)?', 'on', 'off?', 'turn', 'put', '\\w+ite\\w+', '\\w+ight']

food_keywords = ['food', 'dinner', 'breakfast', 'morning', 'evening', 'lunch', 'eating', 'eat']

light_pattern = r'lights?|bulbs?|\w+ights?|\w+ite'
switch_pattern = r'\bon\b|\bof\b|\boff\b'

def show_matches(pattern, strings):
    for s in strings:
        if re.search(pattern, s):
            print("**", s)

        else:
            print(" ", s)
show_matches(light_pattern, 'light bulb lights bulbs white right weight money switch on'.split())

# show_matches(switch_pattern, ' on off done doff '.split())
