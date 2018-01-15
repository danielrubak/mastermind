from settings import *
import itertools, random, sys

def colorsPermute(colorsList, k):
    allRes = []
    for c in itertools.product(colorsList, repeat=k):
        allRes.append(c)
    return allRes

possible = colorsPermute(BALLCOLORS, 4)
results = [(right, wrong) for right in range(5) for wrong in range(5 - right) if not (right == 3 and wrong == 1)]
#pattern = [(0, 255, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0)]

def score(secret, guess):
	first = len([speg for speg, gpeg in zip(secret, guess) if speg == gpeg])
	return first, sum([min(secret.count(j), guess.count(j)) for j in BALLCOLORS]) - first

def solve(secrets, attemptfun, first=False):
	if first:
		guess = [(255, 0, 0), (255, 0, 0), (0, 255, 0), (0, 255, 0)]
	elif len(secrets) == 1:
		guess = secrets.pop()
	else:
		guess = max(possible, key=lambda x: min(sum(1 for s in secrets if score(s, x) != res) for res in results))
	sc = attemptfun(guess)
	if sc != (4, 0):
		secrets -= set(s for s in secrets if score(s, guess) != sc)
		solve(secrets, attemptfun)

def solver(pattern):
    global attemptCount
    attemptCount = 0
    globalGuess = []
    globalBlacks = []
    globalWhites = []
    if len(pattern) == 4:
        def attempt(guess):
            global attemptCount
            attemptCount += 1
            sc = score(pattern, guess)
            print(guess, '+'*sc[0] + '-'*sc[1])
            globalGuess.append(guess)
            globalBlacks.append(sc[0])
            globalWhites.append(sc[1])
            return sc
        solve(set(possible), attempt, True)
    return globalGuess, globalBlacks, globalWhites

#if __name__ == '__main__':
#    solver(pattern)
