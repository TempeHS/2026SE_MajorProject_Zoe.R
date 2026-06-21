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
boxobject = pg.Rect(255,150,200,200)

#visual setup
def vis_setup():
    screen.fill((50,100,150))
    pg.draw.rect(screen,(255,255,0), boxobject)
    pg.display.flip()

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
pg.quit()