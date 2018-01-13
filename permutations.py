import random
import itertools

def factorial(n):
    if n == 0:
        return 1
    else:
        return factorial(n-1)*n

def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]

def colorsPermute(colorsList):
    n = len(colorsList)
    fac = factorial(n)
    print("Factorial: ", fac, sep='')
    r = random.randint(0, fac)
    print("Random: ", r, sep='')
    i = 0
    for c in list(itertools.permutations(colorsList)):
        if i == r:
            print("I: ", i, sep='')
            return c
        i += 1

colours = ["red", "green", "blue", "yellow", "orange", "pink", "purple", "brown"]
print(colorsPermute(colours))
