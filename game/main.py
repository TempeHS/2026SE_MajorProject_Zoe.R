#ok whatever i'm starting from scratch
import pygame as pg
import time

#initialises pygame
pg.init()
screen = pg.display.set_mode((640,640))
smiley = pg.image.load('you-are-an-idiot.png').convert_alpha()
clock = pg.time.Clock()
font = pg.font.Font(None, size=30)

running = True
x=-500
while running:
    #sets the screen colour
    screen.fill((100,100,100))
    #caps the framerate at 60fps
    clock.tick(60)
    #sets smiley position
    screen.blit(smiley, (x, 0))
    x+=1
    #render text
    text = font.render("test game :3", True, (0,0,0))
    screen.blit(text,(250,25))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    pg.display.flip()
pg.quit()