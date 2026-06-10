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
amount_clicks = 0
while running:
    #sets the screen colour
    screen.fill((100,100,100))
    #caps the framerate at 60fps
    clock.tick(60)
    #sets smiley position
    # screen.blit(smiley, (x, 0))
    #get mouse position
    mousepos = pg.mouse.get_pos()
    #checks to see if left click has been pressed
    # mclick = pg.mouse.get_pressed()[0]
    #basic rectangle to detect for collisions
    target = pg.Rect(300,0,160,280)
    #detects mouse collisions
    collision = target.collidepoint(mousepos)
    mcollision = False
    # if collision == True and mclick == True:
    #     mcollision = True
    #     amount_clicks += 1
    #     print(f"clicked {amount_clicks} times")
    #draws rectangle
    pg.draw.rect(screen,(255*mcollision,255,0),target)
    # x+=1
    #render text
    text = font.render("test game", True, (0,0,0))
    text2 = font.render("(it's a little ugly but that's ok :3)", True, (0,0,0))
    screen.blit(text,(250,25))
    screen.blit(text2,(150,50))
    #game quitting event 
    #(prevents the game from freezing)
    for event in pg.event.get():
        #checks if the mouse is being clicked over a specific object
        if event.type == pg.MOUSEBUTTONDOWN:
            if collision == True:
                amount_clicks +=1
                print(f"clicked {amount_clicks} times")
                mcollision = True
        if event.type == pg.QUIT:
            running = False
    #updates display
    pg.display.flip()
pg.quit()

#TEST GAME FUNCTIONS
#displays object
#sets screen colour
#moves object across screen
#detects collisions (specifically for the mouse but this can be modified for other objects too)
#detects clicks on certain objects (in TWO different ways :0)
#counts the amount of mouse clicks on objects