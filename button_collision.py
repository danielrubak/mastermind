import pygame
import sys

def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = [200, 200]
    bg = [255, 255, 255]

    screen = pygame.display.set_mode(size)

    button = pygame.Rect(100, 100, 50, 50) # creates a rect object
    # The rect method is similar to a list but with a few added perks
    # for example if you want the position of the button you can simpy type
    # button.x or button.y or if you want size you can type button.width or
    # height. you can also get the top, left, right and bottom of an object
    # with button.right, left, top, and bottom

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() # gets mouse position

                # checks if mouse position is over the button
                # note this method is constantly looking for collisions
                # the only reason you dont see an evet activated when you
                #hover over the button is because the method is bellow the
                # mousedown event if it were outside it would be called the
                # the moment the mouse hovers over the button

                if button.collidepoint(mouse_pos):
                    # pritns current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))

        screen.fill(bg)
        pygame.draw.rect(screen, [255, 0, 0], button) # draw objects down here
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()
