import random
import itertools

def colorsPermute(colorsList, k, repeat=False):
    n = len(colorsList)
    i = 0
    if repeat == True:
        m = n**k
        r = random.randint(0, m)
        for c in itertools.product(colorsList, repeat=k):
            if i == r:
                return c
            i += 1
    else:
        m = 360
        r = random.randint(0, m)
        for c in list(itertools.permutations(colorsList, k)):
            if i == r:
                return c
            i += 1


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BALLCOLORS = (RED, GREEN, BLUE, YELLOW, PURPLE, CYAN)
#print(colorsPermute(BALLCOLORS, 4, True))
#print(colorsPermute(BALLCOLORS, 4, False))

pattern = []
tempPattern = colorsPermute(BALLCOLORS, 4, False)
for color in tempPattern:
    pattern.append(color)
#print("Patter:", pattern)
