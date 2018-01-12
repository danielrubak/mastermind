import random

def validateInput():
    inputGuess = input("Enter your guess as 4 letters e.g. XXXX:")

    while True:
        if len(inputGuess) != 4:
           inputGuess = input("Enter your guess as 4 letters e.g. XXXX:")
        else:
            wordList = list( inputGuess.upper() )

            invalidLetters = False
            for letter in wordList:
                if letter not in ['R','G','Y','B','W']:
                    invalidLetters = True

            if invalidLetters == True:
                print("Possible colours are R G Y B W")
                inputGuess = input("Enter your guess as 4 letters e.g. XXXX:")

            else:
                return wordList

guessesRemaining = 12
code = []
guess = []
correctPosition = 0
correctColour = 0

for i in range(4):
    code.append(random.choice(['R','G','Y','B','W']))

print("Guess my sequence of four colours, in the correct order.")
print("\nPossible colours are R G Y B W")

while guessesRemaining > 0:

    correctPosition = 0
    correctColour = 0
    lettersChecked = []

    guess = validateInput()
    guessesRemaining -= 1 # Deduct one guess

    tempGuess = list(guess)
    tempCode = list(code)

    for i in range(4):
        if guess[i] == code[i]:
            correctPosition += 1
            tempGuess[i] = "X"
            tempCode[i] = "X"

    for j in range(4):

        if tempGuess[j] in tempCode and tempGuess[j] != "X" and tempGuess[j] not in lettersChecked:

            if tempCode.count(guess[j]) > tempGuess.count(tempGuess[j]):
                correctColour += tempGuess.count(tempGuess[j])

            else:
                correctColour += tempCode.count(tempGuess[j])

            lettersChecked.append(tempGuess[j])

    if correctPosition > 0:
        print("You had",correctPosition,"correct colours in the correct place")
    if correctColour > 0:
        print("You had",correctColour,"correct colours in the wrong place")

    if correctPosition == 0 and correctColour == 0:
        print("No correct colours")

    if correctPosition == 4:
        print("You won in",12-guessesRemaining,"guesses, congratulations!")
        guessesRemaining = 0

    print()

print("Thanks for playing")
