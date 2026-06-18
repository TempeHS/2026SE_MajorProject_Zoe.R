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
    try:
        with open(text_file) as file:
            for lines in file:
                row = lines.rstrip()
                data.append(row)
        file.close
    except FileNotFoundError:
        print("Dialogue data not found")

#dialogue
def dialogue(amount_clicks):
    blank_dialogue_box()
    print(data[amount_clicks])
    dialogue_text = font.render(data[amount_clicks], True, (255,255,255))
    screen.blit(dialogue_text,(100,420))
    print(amount_clicks)
    pg.display.flip()

#choice
def choice(player_choice):
    #in_choice variable had to be made global otherwise the code switching it from false to true didnt work
    #(I didn't check for in_dialogue, but I assume it'd be the same)
    global in_choice
    global in_dialogue
    global amount_clicks
    #for formatting the choices
    choice_1 = 0
    choice_2 = 0
    choices = []
    text_y = 0

    if amount_clicks >= len(data):
        in_dialogue = False
        print("dialogue finished")
        vis_setup()
    else:
        for line in data:
            if "> " in line:
                choices.append(line)
                del data[data.index(line)]
        for line in data:
            if "1- " in line:
                choice_1 +=1
            if "2- " in line:
                choice_2 +=1
        line = data[amount_clicks]
        blank_dialogue_box()
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
        #if the player chooses 'Y'
        elif "1- " in line:
            if player_choice != "Y" and amount_clicks + choice_1 < len(data):
                in_dialogue = False
                amount_clicks += choice_1
                dialogue_text = font.render(data[amount_clicks].strip("2- "), True, (255,255,255))
                screen.blit(dialogue_text,(100,420))   
                pg.display.flip()
                in_dialogue = True
                print(f"{amount_clicks} - Y line")
            elif player_choice == "Y":
                in_choice = False
                blank_dialogue_box()
                dialogue_text = font.render(data[amount_clicks].strip("1- "), True, (255,255,255))
                screen.blit(dialogue_text,(100,420))
                pg.display.flip()
            else:
                pass
        #if the player chooses 'N'
        elif "2- " in line:
            print(f"{amount_clicks} - N line")
            if player_choice != "N" and amount_clicks + choice_2 < len(data):
                in_dialogue = False
                amount_clicks += choice_2
                dialogue_text = font.render(data[amount_clicks].strip("1- "), True, (255,255,255))
                screen.blit(dialogue_text,(100,420))  
                pg.display.flip() 
                in_dialogue = True
            elif player_choice == "N":
                blank_dialogue_box()
                dialogue_text = font.render(data[amount_clicks].strip("2- "), True, (255,255,255))
                screen.blit(dialogue_text,(100,420))
                pg.display.flip()
            else:
                pass
        #regular dialogue code
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
                    choice(player_choice)
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
                choice(player_choice)
                amount_clicks+=1
                print(amount_clicks)
            #choice dialogue progression
            if event.type == pg.KEYDOWN and event.unicode == ' ' and in_choice == True:
                pass
            if event.type == pg.KEYDOWN and event.unicode == 'y' and in_choice == True:
                player_choice = "Y"
                in_choice = False
                choice(player_choice)
                amount_clicks+=1
            if event.type == pg.KEYDOWN and event.unicode == 'n' and in_choice == True:
                player_choice = "N"
                in_choice = False
                choice(player_choice)
                amount_clicks+=1
pg.quit()

#