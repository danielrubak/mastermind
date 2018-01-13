# Skeleton for a pygame Mastemind project
import pygame, sys, random, math
from pygame.locals import *
FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 400 # size of window's width in pixels
WINDOWHEIGHT = 790 # size of windows' height in pixels
REVEALSPEED = 16 # speed boxes' sliding reveals and covers
COLUMNS = 4 # number of columns of icons
ROWS = 12 # number of rows of icons
XMARGIN = 15
YMARGIN = 15

# define colors
BACKGROUND = (166, 124, 82)
EMPTYHOLE = (96, 56, 19)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BALLCOLORS = (RED, GREEN, BLUE, YELLOW, PURPLE, CYAN)
PINCOLORS = (WHITE, BLACK)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Mastermind")
font = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()

def main():
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event

    screen.fill(BACKGROUND)
    drawClearBoard()
    filledHoles = generateFilledHoles(False)
    currentRow = 0
    currentBall = 0
    # game loop
    running = True
    while running:
        mouseClicked = False
        selectedColor = None
        removeBall = False
        # keep loop running at the right speed
        clock.tick(FPS)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        if mouseClicked:
            if mousey > 725:
                print("DODAWANIE")
                for i in range(len(BALLCOLORS)):
                    if mousex>(45+(i*50)) and mousex < (95+(i*50)):
                        sqx = (mousex - (65+(i*50)))**2
                        sqy = (mousey - 745)**2
                        if sqx+sqy < 400:
                            selectedColor = BALLCOLORS[i]
                            break;
            if mousey < (690-(currentRow*50)) and mousey > (650-(currentRow*50)):
                if currentBall == 3 and mousex>310:
                    pygame.draw.rect(screen, BACKGROUND, (XMARGIN+295, YMARGIN+(635-currentRow*50), 60, 40))
                    currentRow += 1
                else:
                    print("USUWANIE")
                    removeBall = True

        if mouseClicked and selectedColor:
            row, ball = getStatus(filledHoles)
            if currentRow == row:
                pygame.draw.circle(screen, selectedColor, (XMARGIN+95+(ball*50), YMARGIN+(655-row*50)), 20)
                filledHoles[row][ball] = True
                currentBall = ball
                if ball == 3:
                      pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN+295, YMARGIN+(635-currentRow*50), 60, 40))
        pygame.display.flip()

def drawClearBoard():
    # first block
    pygame.draw.rect(screen, EMPTYHOLE, (XMARGIN, YMARGIN, WINDOWWIDTH-(2*XMARGIN), 60), 4)
    pygame.draw.line(screen, EMPTYHOLE, (75, 25), (75, 65), 4)
    for i in range(1,3):
        for j in range(1,3):
            pygame.draw.circle(screen, EMPTYHOLE, (XMARGIN+(i*20), YMARGIN+(j*20)), 9)
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

def generateFilledHoles(val):
    filledHoles = []
    for i in range(ROWS):
        filledHoles.append([val] * COLUMNS)
    return filledHoles

def getStatus(filledHoles):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if filledHoles[r][c] == False:
                return (r, c)

if __name__ == '__main__':
    main()
