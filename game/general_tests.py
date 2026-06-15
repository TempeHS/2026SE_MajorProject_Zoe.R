#general tests of some basic pygame features
#(and hopefully the most disorganised these files will get)
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
data = []
with open("dialogue_placeholder") as file:
    for line in file:
        row = line.rstrip()
        data.append(row)
file.close()

while running:
    #sets the screen colour
    #caps the framerate at 60fps
    clock.tick(60)
    #sets smiley position
    # screen.blit(smiley, (x, 0))
    #get mouse position
    mousepos = pg.mouse.get_pos()
    #checks to see if left click has been pressed
    # mclick = pg.mouse.get_pressed()[0]
    #basic rectangle to detect for collisions
    target = pg.Rect(225,150,200,200)
    dialoguebox = pg.Rect(250,100,100,100)
    #detects mouse collisions
    collision = target.collidepoint(mousepos)
    in_dialogue = False
    # mcollision = False
    # if collision == True and mclick == True:
    #     mcollision = True
    #     amount_clicks += 1
    #     print(f"clicked {amount_clicks} times")
    #draws rectangle
    # x+=1
    #render text
    #game quitting event 
    #(prevents the game from freezing)
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255,0),target)
    for event in pg.event.get():
        #checks if the mouse is being clicked over a specific object
        if event.type == pg.MOUSEBUTTONDOWN:
            if collision == True:
                if amount_clicks <= len(data) - 1:
                    print(data[amount_clicks])
                    pg.draw.rect(screen,(255,0,255),dialoguebox)
                    text3 = font.render(data[amount_clicks], True, (0,0,0))
                    screen.blit(text3,(150,50))
                else:
                    print(data[len(data) - 1])
                amount_clicks +=1
        #testing for if keys are pressed
        if event.type == pg.KEYDOWN:
            text = font.render("test game", True, (0,0,0))
            screen.blit(text,(250,25))
            print(event)
        if event.type == pg.KEYUP:
            text2 = font.render("(it's a little ugly but that's ok :3)", True, (0,0,0))
            screen.blit(text2,(150,50))
        if event.type == pg.QUIT:
            running = False
        pg.display.flip()
    #updates display
pg.quit()

#TEST GAME FUNCTIONS
#displays object
#sets screen colour
#moves object across screen
#detects collisions (specifically for the mouse but this can be modified for other objects too)
#detects clicks on certain objects (in TWO different ways :0)
#counts the amount of mouse clicks on objects
#basic dialogue system

#basic dialogue system works for testing, but will probably need to be optimised a bit to make it work for multiple objects
#(probably by turning it into a function)