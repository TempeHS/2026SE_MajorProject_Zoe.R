#imports
import pygame as pg
import time

#basic setup
pg.init()
screen = pg.display.set_mode((640,640))
clock = pg.time.Clock()
font = pg.font.Font(None, size=30)

#setting up variables
running = True
amount_clicks = 0
text_file = ""
data = []
in_dialogue = False
boxobject = pg.Rect(255,150,200,200)

#visual setup (clears screen completely)
def vis_setup():
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255,0), boxobject)
    pg.display.flip()

#setup for a blank dialogue box because the dialogue box sometimes disappearing was getting annoying
def blank_dialogue_box():
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255,0), boxobject)
    pg.draw.rect(screen,(0,0,0),(70,400,500,200))
    cont_text = font.render("press SPACE to continue", True, (255,255,255))
    screen.blit(cont_text, (100, 560))                
    pg.display.flip()

#get dialogue data
def get_dialogue_data(text_file):
    with open(text_file) as file:
        for line in file:
            row = line.rstrip()
            data.append(row)
    file.close

#dialogue
def dialogue(amount_clicks):
    blank_dialogue_box()
    print(data[amount_clicks])
    dialogue_text = font.render(data[amount_clicks], True, (255,255,255))
    screen.blit(dialogue_text,(100,420))
    print(amount_clicks)
    pg.display.flip()

def choice():
    pass

vis_setup()
#main gameplay loop
while running:
    #variable setup
    clock.tick(60)
    mousepos = pg.mouse.get_pos()
    collision = boxobject.collidepoint(mousepos)
    #event loops
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if collision == True and in_dialogue == False:
                if amount_clicks == 0:
                    get_dialogue_data("dialogue_placeholder")
                    in_dialogue = True
                    #brings the first line of dialogue up when the object is clicked rather than on the first space
                    dialogue(amount_clicks)
                    amount_clicks+=1
                else:
                    vis_setup()
                    dialogue_complete = font.render("You finished the dialogue!!! yay!!!", True, (255,255,255))
                    screen.blit(dialogue_complete,(100,420))
                    pg.display.flip()
        if in_dialogue == True:
            if amount_clicks >= len(data):
                in_dialogue = False
                print("dialogue finished")
                vis_setup()
            if event.type == pg.KEYDOWN and event.unicode == ' ':
                dialogue(amount_clicks)
                amount_clicks+=1
                
                
pg.quit()

#dialogue logic
#by default in_dialogue is set to false (player is not interacting with a set of dialogue)
#when the player clicks on the box object, it starts the dialogue (in_dialogue is set to true)
#as player presses a certain key (probably space), it goes through all the dialogue
#after all of the dialogue has finished, the dialogue disappears, in_dialogue is set to false
#after this, if the player tries interacting with the dialogue box it either does not produce dialogue (easier to code)
#or repeats the last line from the dialogue file and closes the dialogue

#set this up simply and then optimise it by changing it to OOP