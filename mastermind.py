# Skeleton for a pygame Mastemind project
import pygame, sys, random, math, time
from pygame.locals import *
from permutations import colorsPermute
from knuthSolver import solver
from button import *
from settings import *

def quitGameFunction():
    return False

def startGameFunction():
    gameIntro(False)
    gameLoop(True)

def gameIntro(runMode):
    startButton = Button("Start game", (200, 100), startGameFunction, bg=GREEN, size = (150, 30))
    challangeAI = Button("Challange the computer", (200, 200), computerLoop, bg=EMPTYHOLE, size = (200, 30), params=[True])
    closeButton = Button("Exit", (200, 300), quitGameFunction, bg=RED, size = (150, 30))
    buttons = [startButton, challangeAI, closeButton]
    while runMode:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button, val = mousebuttondown(buttons)
                if button == closeButton:
                    runMode = val
        screen.fill(BACKGROUND)
        for button in buttons:
            button.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()

def gameLoop(runMode):
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event

    buttons = []
    pattern = []
    screen.fill(BACKGROUND)
    buttons = drawClearBoard(buttons)
    filledHoles = generateFilledHoles(False)
    currentRow = 0
    currentBall = 0
    whites = 0
    blacks = 0

    tempPattern = colorsPermute(BALLCOLORS, 4, False)
    for color in tempPattern:
        pattern.append(color)
    print("Patter:", pattern)

    # game loop
    while runMode:
        if currentRow == ROWS or blacks == 4:
            time.sleep(5)
            runMode = False
            gameIntro(True)
        else:
            mouseClicked = False
            selectedColor = None
            removeBall = False
            # keep loop running at the right speed
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button, val = mousebuttondown(buttons)
                    if button != None:
                        if button == checkButton:
                            blacks, whites = val[0], val[1]
                            setPins(blacks, whites, currentRow)
                            buttons.remove(checkButton)
                            pygame.draw.rect(screen, BACKGROUND, (XMARGIN+280, YMARGIN+(635-currentRow*50), 80, 40))
                            currentRow += 1
                            if blacks == 4:
                                # first block
                                pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN, YMARGIN, WINDOWWIDTH-(2*XMARGIN), 60), 4)
                                for i in range (COLUMNS):
                                    pygame.draw.circle(screen, pattern[i], (XMARGIN+95+(i*50), YMARGIN+30), 20)

            if mouseClicked:
                if mousey > 725:
                    # adding new ball to the next free hole
                    for i in range(len(BALLCOLORS)):
                        if mousex>(45+(i*50)) and mousex < (95+(i*50)):
                            sqx = (mousex - (65+(i*50)))**2
                            sqy = (mousey - 745)**2
                            if sqx+sqy < 400:
                                selectedColor = BALLCOLORS[i]
                                break;
                if mousey < (690-(currentRow*50)) and mousey > (650-(currentRow*50)):
                    if mousex<310:
                        # removing ball from hole
                        removeBall = True

            if mouseClicked and selectedColor:
                row, ball = getStatus(filledHoles)
                if currentRow == row:
                    pygame.draw.circle(screen, selectedColor, (XMARGIN+95+(ball*50), YMARGIN+(655-row*50)), 20)
                    filledHoles[row][ball] = (True, selectedColor)
                    currentBall = ball
                    if ball == 3:
                          checkButton = Button("Check", (335, YMARGIN+(655-currentRow*50)), getSolutionEvaluation, bg=EMPTYHOLE, fg=WHITE, size = (70, 40), params=[pattern, filledHoles, row])
                          buttons.append(checkButton)

            if mouseClicked and removeBall:
                row, ball = getStatus(filledHoles)
                pygame.draw.circle(screen, EMPTYHOLE, (XMARGIN+95+(currentBall*50), YMARGIN+(655-currentRow*50)), 20)
                if currentBall == 3:
                    buttons.remove(checkButton)
                    del checkButton
                    pygame.draw.rect(screen, BACKGROUND, (XMARGIN+280, YMARGIN+(635-currentRow*50), 80, 40))
                filledHoles[currentRow][currentBall] = (False, None)
                currentBall -= 1
            for button in buttons:
                button.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()

def computerSolver(runMode, myPattern):
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.draw.rect(screen, BACKGROUND, (XMARGIN+120, YMARGIN+420, 130, 30))
    buttons = []
    pattern = []
    screen.fill(BACKGROUND)
    buttons = drawClearBoard(buttons)
    filledHoles = generateFilledHoles(False)
    currentRow = 0
    currentBall = 0
    whites = 0
    blacks = 0

    tempPattern, blacksList, whitesList = solver(myPattern)
    # first block
    for i in range (COLUMNS):
        pygame.draw.circle(screen, myPattern[i], (XMARGIN+95+(i*50), YMARGIN+30), 20)

    for row in range(len(tempPattern)):
        colors = tempPattern[row]
        blacks = blacksList[row]
        whites = whitesList[row]
        for i in range(1,3):
            for j in range(1,3):
                if blacks:
                    pygame.draw.circle(screen, BLACK, (XMARGIN+(i*20), YMARGIN+(625-row*50)+(j*20)), 9)
                    blacks -= 1
                elif whites:
                    pygame.draw.circle(screen, WHITE, (XMARGIN+(i*20), YMARGIN+(625-row*50)+(j*20)), 9)
                    whites -= 1
                else:
                    pygame.draw.circle(screen, EMPTYHOLE, (XMARGIN+(i*20), YMARGIN+(625-row*50)+(j*20)), 9)
        for i in range (COLUMNS):
            pygame.draw.circle(screen, colors[i], (XMARGIN+95+(i*50), YMARGIN+(655-row*50)), 20)

    while(runMode):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button, val = mousebuttondown(buttons)
        for button in buttons:
            button.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()

def computerLoop(runMode):
    selectedColor = None
    removeBall = False
    currentRow = 0
    currentBall = 0
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN, YMARGIN+270, WINDOWWIDTH-(2*XMARGIN), 60), 4)
    for i in range (COLUMNS):
        pygame.draw.circle(screen, EMPTYHOLE, (XMARGIN+110+(i*50), YMARGIN+(300)), 20)
    pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN, YMARGIN+350, WINDOWWIDTH-(2*XMARGIN), 60), 4)
    i = 1
    for color in BALLCOLORS:
        pygame.draw.circle(screen, color, (XMARGIN+(i*50), YMARGIN+380), 20)
        i += 1
    buttons = []
    filledHoles = []
    filledHoles.append([(False, None)] * COLUMNS)

    while runMode:
        mouseClicked = False
        selectedColor = None
        removeBall = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                print(mousex,mousey)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button, val = mousebuttondown(buttons)
                if button:
                    if button == acceptButton:
                        myPattern = []
                        for i in range(4):
                            crap, color = filledHoles[0][i]
                            myPattern.append(color)
                        computerSolver(True, myPattern)

        if mouseClicked:
            if mousey > 375 and mousey < 415:
                # adding new ball to the next free hole
                for i in range(len(BALLCOLORS)):
                    if mousex>(45+(i*50)) and mousex < (85+(i*50)):
                        sqx = (mousex - (65+(i*50)))**2
                        sqy = (mousey - 395)**2
                        if sqx+sqy < 400:
                            selectedColor = BALLCOLORS[i]
                            break;
            if mousey < 335 and mousey > 295:
                if mousex<315:
                    # removing ball from hole
                    removeBall = True

        if mouseClicked and selectedColor:
            for c in range(COLUMNS):
                if filledHoles[0][c] == (False, None):
                    ball = c
                    break;
            pygame.draw.circle(screen, selectedColor, (XMARGIN+110+(ball*50), YMARGIN+300), 20)
            filledHoles[0][ball] = (True, selectedColor)
            currentBall = ball
            if ball == 3:
                acceptButton = Button("Accept Pattern", (200, 450), tempFcn, bg=EMPTYHOLE, fg=WHITE, size = (130, 30))
                buttons.append(acceptButton)

        if mouseClicked and removeBall:
            pygame.draw.circle(screen, EMPTYHOLE, (XMARGIN+110+(currentBall*50), YMARGIN+300), 20)
            if currentBall == 3:
                buttons.remove(acceptButton)
                del acceptButton
                pygame.draw.rect(screen, BACKGROUND, (XMARGIN+120, YMARGIN+420, 130, 30))
            filledHoles[currentRow][currentBall] = (False, None)
            currentBall -= 1
        for button in buttons:
            button.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()

def drawClearBoard(buttonsList):
    # first block
    pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN, YMARGIN, WINDOWWIDTH-(2*XMARGIN), 60), 4)
    for i in range (COLUMNS):
        pygame.draw.circle(screen, GRAY, (XMARGIN+95+(i*50), YMARGIN+30), 20)

    # second block
    pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN, YMARGIN+75, WINDOWWIDTH-(2*XMARGIN), 610), 4)
    pygame.draw.line(screen, EMPTYHOLE, (75, 100), (75, 690), 4)
    for row in range(ROWS):
        for i in range(1,3):
            for j in range(1,3):
                pygame.draw.circle(screen, EMPTYHOLE, (XMARGIN+(i*20), YMARGIN+(625-row*50)+(j*20)), 9)
        for i in range (COLUMNS):
            pygame.draw.circle(screen, EMPTYHOLE, (XMARGIN+95+(i*50), YMARGIN+(655-row*50)), 20)
    # third block
    pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN, YMARGIN+700, WINDOWWIDTH-(2*XMARGIN), 60), 4)
    i = 1
    for color in BALLCOLORS:
        pygame.draw.circle(screen, color, (XMARGIN+(i*50), YMARGIN+730), 20)
        i += 1
    # bottom buttons
    backToMenuButton = Button("Back to menu", (90, 793), gameIntro, bg=EMPTYHOLE, fg=WHITE, size = (130, 26), params=[True])
    buttonsList.append(backToMenuButton)
    newGameButton = Button("New game", (300, 793), gameLoop, bg=EMPTYHOLE, fg=WHITE, size = (130, 26), params=[True])
    buttonsList.append(newGameButton)
    print(buttonsList)
    return buttonsList

def generateFilledHoles(val):
    filledHoles = []
    for i in range(ROWS):
        filledHoles.append([(val, None)] * COLUMNS)
    return filledHoles

def getStatus(filledHoles):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if filledHoles[r][c] == (False, None):
                return (r, c)

def getSolutionEvaluation(pattern, filledHoles, row):
    blacks, whites = 0, 0
    guess = []
    for c in range(COLUMNS):
        temp, colors = filledHoles[row][c]
        guess.append(colors)
    colorsChecked = []
    tempGuess = list(guess)
    tempCode = list(pattern)
    for i in range(4):
        if guess[i] == pattern[i]:
            blacks += 1
            tempGuess[i] = "X"
            tempCode[i] = "X"

    for j in range(4):
        if tempGuess[j] in tempCode and tempGuess[j] != "X" and tempGuess[j] not in colorsChecked:
            if tempCode.count(guess[j]) > tempGuess.count(tempGuess[j]):
                whites += tempGuess.count(tempGuess[j])
            else:
                whites += tempCode.count(tempGuess[j])
            colorsChecked.append(tempGuess[j])
    return blacks, whites

def setPins(blacks, whites, row):
    colors = []
    while blacks:
        colors.append(BLACK)
        blacks -= 1
    while whites:
        colors.append(WHITE)
        whites -= 1
    while len(colors)<4:
        colors.append(EMPTYHOLE)
    color = 0
    for i in range(1,3):
        for j in range(1,3):
            pygame.draw.circle(screen, colors[color], (XMARGIN+(j*20), YMARGIN+(625-row*50)+(i*20)), 9)
            color += 1

def tempFcn():
    print()

if __name__ == '__main__':
    # initialize pygame and create window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Mastermind")
    clock = pygame.time.Clock()
    gameIntro(True)
