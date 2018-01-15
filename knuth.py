from itertools import product

possible = [''.join(secret) for secret in product('ABCDEF', repeat=4)]
print("Possible:",possible,"	len(possible):",len(possible))
results = [(right, wrong) for right in range(5) for wrong in range(5 - right) if not (right == 3 and wrong == 1)]
print("Result:",results,"	len(results):",len(results))

def score(secret, guess):
	first = len([speg for speg, gpeg in zip(secret, guess) if speg == gpeg])
	return first, sum([min(secret.count(j), guess.count(j)) for j in 'ABCDEF']) - first

def solve(secrets, attemptfun, first=False):
	if first:
		guess = 'AABB'
	elif len(secrets) == 1:
		guess = secrets.pop()
	else:
		guess = max(possible, key=lambda x: min(sum(1 for s in secrets if score(s, x) != res) for res in results))

	sc = attemptfun(guess)

	if sc != (4, 0):
		secrets -= set(s for s in secrets if score(s, guess) != sc)
		solve(secrets, attemptfun)

if __name__ == '__main__':
    import sys
    secret = len(sys.argv) > 1 and sys.argv[1] or input("Please enter a code (four characters, A-F): ")
    if len(secret) == 4 and not (set(secret) - set('ABCDEF')):
        print("Solving...")
        attemptCount = 0
        def attempt(guess):
            global attemptCount
            attemptCount += 1
            sc = score(secret, guess)
            print(guess, '+'*sc[0] + '-'*sc[1])
            return sc
        solve(set(possible), attempt, True)
        print("It took ",str(attemptCount)," attempts.",sep='')
    else:
        print(secret, " is not a well-formed mastermind code.",sep='')
