import pygame

# define colors
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Button():
    def __init__(self, txt, location, action, bg=WHITE, fg=BLACK, size=(80, 30), font_name="Segoe Print", font_size=16, params=[]):
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

    def draw(self, screenName):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screenName.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = GREY  # mouseover color

    def call_back(self):
        return self.call_back_(*self.params)

def my_great_function():
    print("Great! " * 5)

def mousebuttondown(buttonsList):
    pos = pygame.mouse.get_pos()
    val = None
    returnButton = None
    for button in buttonsList:
        if button.rect.collidepoint(pos):
            val = button.call_back()
            returnButton = button
    return returnButton, val
