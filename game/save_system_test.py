#imports
import pygame as pg
import time
import sqlite3 as sql

#basic setup
pg.init()
screen = pg.display.set_mode((640,640))
clock = pg.time.Clock()
font = pg.font.Font(None, size=30)

#UI CODE
#basic box in the top corner that expands into a menu (simple collision code)
#when clicked, brings up 2 smaller boxes that activate the saving/loading functions (again, simple collision code)
#cannot save while in dialogue (not relevant to this, and can be sorted out with a few tweaks in the final code)

#variable setup
running = True
amount_clicks = 0
boxobject = pg.Rect(255,150,200,200)
menuobject = pg.Rect(575,15,50,50)
save_progress = pg.Rect(225,150,200,50)
load_progress = pg.Rect(225,225,200,50)
exit_menu = pg.Rect(225,300,200,50)
in_menu = False

#visual setup
def vis_setup():
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255,0), boxobject)
    pg.draw.rect(screen,(255,0,255), menuobject)
    pg.display.flip()

#text update
def textupdate(amount_clicks):
    vis_setup()
    dialogue_text = font.render(f"clicked {amount_clicks} times", True, (255,255,255))
    screen.blit(dialogue_text,(100,420))
    pg.display.flip()

#save
def updatesave(amount_clicks):
    connection = sql.connect("test.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE save_files SET amount_clicks = ? WHERE rowid = 1', (amount_clicks,))
    connection.commit()
    connection.close()

#load save
def loadsave():
    global amount_clicks
    connection = sql.connect("test.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM save_files")
    details = cursor.fetchone()
    print(details)
    for var in details:
        amount_clicks = var

#open save menu
def openmenu():
    vis_setup()
    global in_menu
    in_menu = True
    pg.draw.rect(screen,(0,255,255), (75,75,500,300))
    menu_text = font.render("SAVE MENU", True, (0,0,0))
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
    print(in_menu)
    #variable setup
    clock.tick(60)
    mousepos = pg.mouse.get_pos()
    collision = boxobject.collidepoint(mousepos)
    menuclick = menuobject.collidepoint(mousepos)
    saveclick = save_progress.collidepoint(mousepos)
    loadclick = load_progress.collidepoint(mousepos)
    exitclick = exit_menu.collidepoint(mousepos)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if collision == True and in_menu == False:
                print("you are clicking on the box!")
                amount_clicks += 1
                textupdate(amount_clicks)
            if menuclick == True and in_menu == False:
                openmenu()
            if saveclick == True and in_menu == True:
                updatesave(amount_clicks)
                in_menu = False
                textupdate(amount_clicks)
            if loadclick == True and in_menu == True:
                loadsave()
                in_menu = False
                textupdate(amount_clicks)
            if exitclick == True and in_menu == True:
                in_menu = False
                textupdate(amount_clicks)
            else:
                pass
        if event.type == pg.KEYDOWN and event.unicode == 's':
            updatesave(amount_clicks)
        if event.type == pg.KEYDOWN and event.unicode == 'l':
            loadsave()
pg.quit()