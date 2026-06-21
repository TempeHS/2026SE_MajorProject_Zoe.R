#imports
import pygame as pg
import time
import sqlite3 as sql

#basic setup
pg.init()
screen = pg.display.set_mode((640,640))
clock = pg.time.Clock()
font = pg.font.Font(None, size=30)

#variable setup
running = True
boxobject = pg.Rect(380,150,200,200)
boxobject2 = pg.Rect(60,150,200,200)
menuobject = pg.Rect(575,15,50,50)
save_progress = pg.Rect(225,150,200,50)
load_progress = pg.Rect(225,225,200,50)
exit_menu = pg.Rect(225,300,200,50)
amount_clicks = 0
in_menu = False
text_file = ""
data = []
choices = []
in_dialogue = False
in_choice = False
player_choice = ""
dialogue1complete = 0
dialogue2complete = 0

#visual setup
def vis_setup():
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255*dialogue1complete,0), boxobject)
    pg.draw.rect(screen,(255,255*dialogue2complete,255), boxobject2)
    pg.draw.rect(screen,(255,0,255), menuobject)
    pg.display.flip()
    
#setup for a blank dialogue box
def blank_dialogue_box():
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255*dialogue1complete,0), boxobject)
    pg.draw.rect(screen,(255,255*dialogue2complete,255), boxobject2)
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
    pg.display.flip()

#function for fixing an issue I was having
def choiceunique():
    global choices
    empty = []
    for c in choices:
        empty.append(c)
    choices.clear()
    print(empty)
    for choice in empty:
        if choice not in choices:
            choices.append(choice)

#choice
def choice(player_choice):
    #in_choice variable had to be made global otherwise the code switching it from false to true didnt work
    #(I didn't check for in_dialogue, but I assume it'd be the same)
    global in_choice
    global in_dialogue
    global amount_clicks
    global choices
    choiceunique()
    #for formatting the choices
    choice_1 = 0
    choice_2 = 0
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
            print(choices)
            for c in choices:
                text_y += 20
                choice_c = font.render(c, True, (255,255,255))
                screen.blit(choice_c,(100,430+text_y))
            dialogue_text = font.render(line.strip("* "), True, (255,255,255))
            screen.blit(dialogue_text,(100,420))
            #displays choices
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

#save
def updatesave(dialogue1complete,dialogue2complete): 
    connection = sql.connect("saves.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE save_files SET dialogue1complete = ?, dialogue2complete = ? WHERE rowid = 1', (dialogue1complete,dialogue2complete))
    connection.commit()
    connection.close()

#load save
def loadsave():
    global dialogue1complete
    global dialogue2complete
    connection = sql.connect("saves.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM save_files")
    details = cursor.fetchall()
    details = details[0]
    print(details)
    dialogue1complete = details[0]
    dialogue2complete = details[1]

#open save menu
def openmenu():
    vis_setup()
    global in_menu
    in_menu = True
    pg.draw.rect(screen,(0,255,255), (75,75,500,300))
    menu_text = font.render("MENU", True, (0,0,0))
    screen.blit(menu_text,(100,100))
    pg.draw.rect(screen,(255,0,255), save_progress)
    menu_text = font.render("SAVE", True, (0,0,0))
    screen.blit(menu_text,(290,170))
    pg.draw.rect(screen,(255,255,0), load_progress)
    menu_text = font.render("LOAD", True, (0,0,0))
    screen.blit(menu_text,(290,245))
    pg.draw.rect(screen,(255,255,255), exit_menu)
    menu_text = font.render("EXIT MENU", True, (0,0,0))
    screen.blit(menu_text,(265,320))
    pg.display.flip()

#main gameplay loop
vis_setup()
while running:
    #variable setup
    clock.tick(60)
    mousepos = pg.mouse.get_pos()
    collision = boxobject.collidepoint(mousepos)
    collision2 = boxobject2.collidepoint(mousepos)
    menuclick = menuobject.collidepoint(mousepos)
    saveclick = save_progress.collidepoint(mousepos)
    loadclick = load_progress.collidepoint(mousepos)
    exitclick = exit_menu.collidepoint(mousepos)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if collision == True and in_menu == False and in_dialogue == False:
                print(dialogue1complete)
                if dialogue1complete == 0:
                    dialogue1complete = 1
                    get_dialogue_data("dialogue_2")
                    in_dialogue = True
                    choice(player_choice)
                    amount_clicks+=1
                else:
                    vis_setup()
                    amount_clicks = 0
                    pg.display.flip()
            if collision2 == True and in_menu == False and in_dialogue == False:
                print(dialogue2complete)
                if dialogue2complete == 0:
                    dialogue2complete = 1
                    get_dialogue_data("dialogue_1")
                    in_dialogue = True
                    dialogue(amount_clicks)
                    amount_clicks+=1
                else:
                    vis_setup()
                    amount_clicks = 0
                    pg.display.flip()
            if menuclick == True and in_menu == False:
                openmenu()
            if saveclick == True and in_menu == True:
                updatesave(dialogue1complete, dialogue2complete)
                in_menu = False
                vis_setup()
            if loadclick == True and in_menu == True:
                loadsave()
                in_menu = False
                vis_setup()
            if exitclick == True and in_menu == True:
                in_menu = False
                vis_setup()
            else:
                pass
        if in_dialogue == True:
            if amount_clicks >= len(data):
                in_dialogue = False
                print("dialogue finished")
                vis_setup()
            #regular dialogue progression
            if event.type == pg.KEYDOWN and event.unicode == ' ' and in_choice == False:
                choice(player_choice)
                amount_clicks+=1
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