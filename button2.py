import pygame, sys
pygame.init()

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

class Button():
    def __init__(self, txt, location, action, bg=WHITE, fg=BLACK, size=(80, 30), font_name="Segoe Print", font_size=16, params=0):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size
        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)
        self.call_back_ = action
        self.params = params

    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = GREY  # mouseover color

    def call_back(self):
        return self.call_back_(*self.params)
        #return returnValue

def my_great_function(n):
    print("Great! " * n)
    return n

def my_fantastic_function(n, k):
    print("Fantastic! " * n)
    print("Fantastic! " * k)
    return k

def mousebuttondown():
    pos = pygame.mouse.get_pos()
    val = None
    returnButton = None
    for button in buttons:
        if button.rect.collidepoint(pos):
            val = button.call_back()
            returnButton = button
    print(returnButton, val)
    return returnButton, val

screen = pygame.display.set_mode((200, 200))
RED = (255, 0, 0)
BLUE = (0, 0, 255)

button_01 = Button("Great!", (60, 30), my_great_function, params=[3])
button_02 = Button("Fantastic!", (60, 70), my_fantastic_function, bg=(50, 200, 20), params=[1, 2])
buttons = [button_01, button_02]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button, val = mousebuttondown()
    for button in buttons:
        button.draw()
    pygame.display.flip()
    pygame.time.wait(40)
