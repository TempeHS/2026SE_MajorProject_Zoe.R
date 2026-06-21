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
amount_clicks = 0
boxobject = pg.Rect(255,150,200,200)

#visual setup
def vis_setup():
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255,0), boxobject)
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
    textupdate(amount_clicks)

#main gameplay loop
vis_setup()
while running:
    #variable setup
    clock.tick(60)
    mousepos = pg.mouse.get_pos()
    collision = boxobject.collidepoint(mousepos)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN and collision == True:
            print("you are clicking on the box!")
            amount_clicks += 1
            textupdate(amount_clicks)
        if event.type == pg.KEYDOWN and event.unicode == 's':
            updatesave(amount_clicks)
        if event.type == pg.KEYDOWN and event.unicode == 'l':
            loadsave()
pg.quit()