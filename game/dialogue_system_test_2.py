#a copy of the dialogue system tests where I attempted to fix the issues i was having by putting each category of dialogue into different lists
#(the key word here is attempted)

#I copied this code over while I was working on it in my main dialogue file, so some of the parts are quite unfinished
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
in_choice = False
player_choice = ""
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
        for lines in file:
            row = lines.rstrip()
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

#choice
def choice(amount_clicks, player_choice):
    #in_choice variable had to be made global otherwise the code switching it from false to true didnt work
    #(I didn't check for in_dialogue, but I assume it'd be the same)
    global in_choice
    global in_dialogue
    #for formatting the choices
    choices = []
    choice_1_dialogue = []
    choice_2_dialogue = []
    text_y = 0

    if amount_clicks >= len(data):
        in_dialogue = False
        print("dialogue finished")
        vis_setup()
    else:
        #i know the double for loop is the least optimal way to do this
        #but i can't get it to locate and delete every instance of a certain character
        #because like the index value keeps changing
        for line in data:
            for line in data:
                if "> " in line:
                    choices.append(line)
                    del data[data.index(line)]
                if "1. " in line:
                    choice_1_dialogue.append(line)
                    del data[data.index(line)]
                if "2. " in line:
                    choice_2_dialogue.append(line)
                    del data[data.index(line)]
        line = data[amount_clicks]
        blank_dialogue_box()
        #if the player chooses 'Y'
        if player_choice == "Y":
            print(amount_clicks)
            print(choice_1_dialogue)
            print("player chose y")
            
            blank_dialogue_box()
            dialogue_text = font.render(choice_1_dialogue[amount_clicks], True, (255,255,255))
            screen.blit(dialogue_text,(100,420))
            pg.display.flip()
        #if the player chooses 'N'
        elif player_choice == "N":
            blank_dialogue_box()
            dialogue_text = font.render(choice_2_dialogue[amount_clicks], True, (255,255,255))
            screen.blit(dialogue_text,(100,420))
            pg.display.flip()
        #checks for the question indicator
        if "* " in line:
            in_choice = True
            blank_dialogue_box()
            dialogue_text = font.render(line.strip("* "), True, (255,255,255))
            screen.blit(dialogue_text,(100,420))
            #displays choices
            for c in choices:
                text_y += 20
                choice_c = font.render(c, True, (255,255,255))
                screen.blit(choice_c,(100,430+text_y))
            pg.display.flip() 
            print(in_choice)
        else:
            blank_dialogue_box()
            dialogue_text = font.render(data[amount_clicks], True, (255,255,255))
            screen.blit(dialogue_text,(100,420))
            pg.display.flip()


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
                    get_dialogue_data("dialogue_choice")
                    in_dialogue = True
                    #brings the first line of dialogue up when the object is clicked rather than on the first space
                    choice(amount_clicks, player_choice)
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
            #regular dialogue progression
            if event.type == pg.KEYDOWN and event.unicode == ' ' and in_choice == False:
                choice(amount_clicks, player_choice)
                amount_clicks+=1
            #choice dialogue progression
            if event.type == pg.KEYDOWN and event.unicode == ' ' and in_choice == True:
                pass
            if event.type == pg.KEYDOWN and event.unicode == 'y' and in_choice == True:
                player_choice = "Y"
                in_choice = False
                amount_clicks=0
                choice(amount_clicks, player_choice)
            if event.type == pg.KEYDOWN and event.unicode == 'n' and in_choice == True:
                player_choice = "N"
                in_choice = False
                amount_clicks=0
                choice(amount_clicks, player_choice)
pg.quit()

#TO DO - CHOICES
#find out how to skip dialogue entirely instead of giving a blank box - aughgkhgjhgh
#need to figure out a way to temporarily disable pressing space to skip