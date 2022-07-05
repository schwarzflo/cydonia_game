import pygame as pg
import numpy as np
import json

pg.init()


def drawblocks(screen,blocks,type):
    grey = (125,125,125)
    grey_lock = (100,100,100)
    green = (0,255,0)
    black = (0,0,0)
    if type == "nb":
        for block in blocks:
            pg.draw.rect(screen,grey,(block,[30,30]))
    elif type == "b":
        for block in blocks:
            pg.draw.rect(screen,grey,(block,[30,30]))
            pg.draw.line(screen, black, (block[0], block[1]),
                         (block[0] + 30 - 1, block[1] + 30 - 1), width=2)
            pg.draw.line(screen, black, (block[0], block[1] + 30 - 1),
                         (block[0] + 30 - 1, block[1]), width=2)
    elif type == "lk":
        for block in blocks:
            pg.draw.rect(screen, grey_lock, (block[-1], [30, 30]))
            pg.draw.rect(screen, black, ([block[-1][0]+10,block[-1][1]+10], [10, 10]))
            if len(block) > 1: # check whether key is already there
                pg.draw.rect(screen, green, ([block[0][0]+10,block[0][1]+10], [10, 10]))



def drawplayer(screen,player):
    white = (255,255,255)
    pg.draw.rect(screen, white, (player, [30, 30]))


def del_player(screen,player):
    black = (0,0,0)
    pg.draw.rect(screen, black, (player, [30, 30]))


def drawexit(screen,exit):
    white = (255, 255, 255)
    pg.draw.rect(screen, white, (exit, [30, 30]),width=2)


def del_exit(screen,exit):
    black = (0, 0, 0)
    pg.draw.rect(screen, black, (exit, [30, 30]))


def get_block_pos(pos):

    pos[0] -= (pos[0] % 30)
    pos[1] -= (pos[1] % 30)

    return [pos[0],pos[1]]


def transf_to_dic(blocks,breakable,exit,player,key_lock):

    dic = {"player": player, "exit": exit, "blocks": blocks, "breakable": breakable, "key_lock": key_lock}
    return dic



HEIGHT = 900
WIDTH = 1440
BLACK = (0,0,0)
clock = pg.time.Clock()

running = True
draw = False
pl_tru = False
ex_tru = False
editing = False

exit = None
player = None

block_list = []
breakable_list = []
key_lock_list = []

edit = input("Want to edit an existing level? (y/n) ")

if edit == "y":
    lvlnr = int(input("Which level do you want to change? ")) - 1
    f = open("lvl_info", "r")
    data = json.load(f)
    f.close()
    exit = data[lvlnr]["exit"]
    player = data[lvlnr]["player"]
    block_list = data[lvlnr]["blocks"]
    breakable_list = data[lvlnr]["breakable"]
    key_lock_list = data[lvlnr]["key_lock"]
    editing = True

elif edit == "n":
    exit = None
    player = None
    block_list = []
    breakable_list = []
    key_lock_list = []

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Editor')

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
        if event.type == pg.KEYDOWN:
            pos = list(pg.mouse.get_pos())

            if event.key == pg.K_s:
                f = open("lvl_info", "r")
                data = json.load(f)
                f.close()
                if editing:
                    data[lvlnr] = transf_to_dic(block_list, breakable_list, exit, player, key_lock_list)
                else:
                    data.append(transf_to_dic(block_list, breakable_list, exit, player, key_lock_list))
                f = open("lvl_info", "w")
                f.write(json.dumps(data))
                f.close()

            if event.key == pg.K_b:
                block_pos = get_block_pos(pos)
                already_in = False
                for cnt, block in enumerate(breakable_list):
                    if block == block_pos:
                        breakable_list.remove(block_pos)
                        already_in = True
                        screen.fill(BLACK)
                        if player is not None:
                            drawplayer(screen, player)
                        if exit is not None:
                            drawexit(screen, exit)
                        break
                if not already_in:
                    breakable_list.append(block_pos)

            if event.key == pg.K_l:
                block_pos = get_block_pos(pos)
                already_in = False
                for cnt, block in enumerate(key_lock_list):
                    if block[-1] == block_pos:
                        key_lock_list.remove(block)
                        already_in = True
                        screen.fill(BLACK)
                if not already_in and (key_lock_list == [] or len(key_lock_list[-1]) == 2):
                    key_lock_list.append([block_pos])

            if event.key == pg.K_k and key_lock_list != [] and len(key_lock_list[-1]) == 1:
                block_pos = get_block_pos(pos)
                key_lock_list[-1].insert(0, block_pos)

            print(key_lock_list)



        if event.type == pg.MOUSEBUTTONUP:
            pos = list(pg.mouse.get_pos())
            if event.button == 1:
                block_pos = get_block_pos(pos)
                already_in = False
                for cnt, block in enumerate(block_list):
                    if block == block_pos:
                        block_list.remove(block_pos)
                        already_in = True
                        screen.fill(BLACK)
                        if player is not None:
                            drawplayer(screen, player)
                        if exit is not None:
                            drawexit(screen, exit)
                        break
                if not already_in:
                    block_list.append(block_pos)

            if event.button == 2:
                if pl_tru:
                    del_player(screen,player)
                player = get_block_pos(pos)
                drawplayer(screen, player)
                pl_tru = True
            if event.button == 3:
                if ex_tru:
                    del_exit(screen,exit)
                exit = get_block_pos(pos)
                drawexit(screen, exit)
                ex_tru = True

    drawblocks(screen,block_list,"nb")
    drawblocks(screen,breakable_list,"b")
    drawblocks(screen, key_lock_list, "lk")
    pg.display.update()
