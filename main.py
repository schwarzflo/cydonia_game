import pygame as pg
import block as bl
import player as pl
import exit as ex
import numpy as np
import json
import screen_object as so

# FIX THE FACT THAT BREAKABLE DOES NOT OCCUR IN FIRST LEVEL, THIS FUCKS WITH EDITING EXISTING LEVEL


def get_all_blocks(lvl_data,sz,type): #type defines the type of object of which there are multiple

    if type not in lvl_data:
        return []
    all_blocks = []
    am = len(lvl_data[type])
    for i in range(am):
        all_blocks.append(bl.Block(lvl_data[type][i][0], lvl_data[type][i][1], sz, sz, type))
    return all_blocks


def get_player(lvl_data,sz):

    return pl.Player(lvl_data[0],lvl_data[1],sz,sz)


def get_exit(lvl_data,sz):

    return ex.Exit(lvl_data[0],lvl_data[1],sz,sz)


def get_lk(lvl_data,sz):
    print(lvl_data)
    am = len(lvl_data)
    sz_button = 14
    all_lk = []
    if lvl_data != []:
        for i in range(am):
            all_lk.append([so.Object(lvl_data[i][0][0],lvl_data[i][0][1],sz_button,sz_button),so.Object(lvl_data[i][1][0],lvl_data[i][1][1],sz,sz)]) # plus 8 to make button smaller
    return all_lk


def drawlvl(all_blocks,all_lk,screen):

    for block in all_blocks:
        block.draw(screen)

    if all_lk != []:
        for key_lock in all_lk:
            for cnt, object in enumerate(key_lock):
                if cnt == 0:
                    color = (0,255,0)
                    object.draw_b(screen, color)
                else:
                    color = (125, 125, 125)
                    object.draw(screen,color)

    pg.display.update()


def in_block(pos, block):

    if pos[0] > block.pos[0] \
        and pos[0] < block.pos[0] + block.size[0] \
        and pos[1] > block.pos[1] \
        and pos[1] < block.pos[1] + block.size[1]:
        return True
    return False


pg.init()

sz = 30
HEIGHT = 900
WIDTH = 1440
buttonHeight = 600
buttonWidth = 250
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Cydonia')
clock = pg.time.Clock()
game = True

pg.font.init()
my_lvl_font = pg.font.SysFont('Times New Roman', 30)
my_title_font = pg.font.SysFont('Times New Roman', 100)
my_button_font = pg.font.SysFont('Times New Roman', 50)
title_surface = my_title_font.render('CYDONIA', False, WHITE)
ButSet_surface = my_button_font.render('Settings', False, WHITE)
ButEd_surface = my_button_font.render('Editor', False, WHITE)
ButNG_surface = my_button_font.render('New Game', False, WHITE)
surfaces = [title_surface,ButSet_surface,ButEd_surface,ButNG_surface]

tw = title_surface.get_width()

f = open("lvl_info", "r")
lvls = json.load(f)
f.close()
in_lvls = False

buttonSettings = so.Object(200,buttonHeight,buttonWidth,100)
buttonEditor = so.Object(WIDTH/2-buttonWidth/2,buttonHeight,buttonWidth,100)
buttonNewGame = so.Object(WIDTH-buttonWidth-200,buttonHeight,buttonWidth,100)

buttonEditor.draw(screen, RED)
buttonSettings.draw(screen, RED)
buttonNewGame.draw(screen, RED)

screen.blit(title_surface, (WIDTH / 2 - tw / 2, 200))
screen.blit(ButSet_surface, (200 + buttonWidth / 2 - ButSet_surface.get_width()/2, 625))
screen.blit(ButEd_surface, (WIDTH/2 - ButEd_surface.get_width()/2, 625))
screen.blit(ButNG_surface, (WIDTH-buttonWidth-200 + buttonWidth / 2 - ButNG_surface.get_width()/2, 625))

pg.display.update()


while game:


    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
        if event.type == pg.MOUSEBUTTONUP:
            pos = list(pg.mouse.get_pos())
            if in_block(pos,buttonNewGame):
                in_lvls = True

    if in_lvls:

        for cnt, lvl in enumerate(lvls,1):
            lvl_surface = my_lvl_font.render(f"Level {cnt}", False, WHITE)
            same_lvl = True

            while same_lvl:
                screen.fill(BLACK)
                all_blocks = get_all_blocks(lvl,sz,"blocks")
                player = get_player(lvl["player"],sz)
                exit = get_exit(lvl["exit"],sz)
                all_breakable = get_all_blocks(lvl,sz,"breakable")
                lks = False
                all_lk = get_lk(lvl["key_lock"],sz)     # only prepare lock key pair if it exists

                same_lvl = False  # dont replay level by default
                moving = False
                playing = True
                drawlvl(all_blocks, all_lk, screen)
                exit.draw(screen)

                while playing:

                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            quit()
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_UP and not moving:
                                dir = "up"
                                moving = True
                            if event.key == pg.K_DOWN and not moving:
                                dir = "down"
                                moving = True
                            if event.key == pg.K_RIGHT and not moving:
                                dir = "right"
                                moving = True
                            if event.key == pg.K_LEFT and not moving:
                                dir = "left"
                                moving = True
                            if event.key == pg.K_r:
                                playing = False
                                same_lvl = True
                            if event.key == pg.K_n:
                                playing = False

                    if player.edge_check(WIDTH, HEIGHT, dir):  # edge of window
                        moving = False
                        dir = ""

                    if player.collision_check(all_blocks, dir, screen) is not None:  # collision with solid blocks
                        moving = False
                        dir = ""

                    coll_block = player.collision_check(all_breakable, dir, screen)
                    #print(coll_block)
                    if coll_block is not None:  # collision with breakable blocks
                        moving = False
                        dir = ""
                        for br in all_breakable: # remove breakable block from list
                            if br.pos == coll_block:
                                all_breakable.remove(br)

                    if all_lk != []: #if no lock key exists, dont check for collision!
                        for lk in all_lk: #check whether you hit a key
                            if player.on_lk(lk, dir, 1) is True:
                                moving = False
                                dir = ""
                            elif player.on_lk(lk, dir, 0) is True:
                                so.Object(lk[1].pos[0],lk[1].pos[1],lk[1].size[0],lk[1].size[1]).draw(screen,BLACK) #create black square to remove block from screen
                                all_lk.remove(lk)
                                break

                    if player.exit_check(exit):  # exit reached
                        moving = False
                        dir = ""
                        playing = False

                    if moving:  # move player
                        player.move(dir, screen)

                    player.draw(screen)
                    drawlvl(all_breakable, all_lk, screen)
                    screen.blit(lvl_surface, (WIDTH - lvl_surface.get_width(), HEIGHT - 30))
                    clock.tick(50)
