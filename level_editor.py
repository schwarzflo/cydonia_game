import pygame as pg
import numpy as np
import json

pg.init()


def drawblocks(screen,blocks,type):
    grey = (125,125,125)
    grey_lock = (100,100,100)
    green = (0,255,0)
    black = (0,0,0)
    red = (125,0,0)
    orange = (209,148,24)
    white = (255,255,255)
    standard_size = 30

    if type == "nb":
        for block in blocks:
            pg.draw.rect(screen,grey,(block,[standard_size,standard_size]))
    elif type == "b":
        for block in blocks:
            pg.draw.rect(screen,grey,(block,[standard_size,standard_size]))
            pg.draw.line(screen, black, (block[0], block[1]),
                         (block[0] + standard_size - 1, block[1] + standard_size - 1), width=2)
            pg.draw.line(screen, black, (block[0], block[1] + standard_size - 1),
                         (block[0] + standard_size - 1, block[1]), width=2)
    elif type == "lk":
        for block in blocks:
            pg.draw.rect(screen, grey_lock, (block[-1], [standard_size, standard_size]))
            pg.draw.rect(screen, black, ([block[-1][0]+10,block[-1][1]+10], [10, 10]))
            if len(block) > 1: # check whether key is already there
                pg.draw.rect(screen, green, ([block[0][0]+10,block[0][1]+10], [10, 10]))

    elif type == "e":
        margin = 5
        for block in blocks:
            pg.draw.rect(screen, red, (block[:2], [standard_size, standard_size]))
            if block[2] == "left":
                pa = [block[0] + margin, block[1] + standard_size / 2]
                pb = [block[0] + standard_size - margin, block[1] + margin]
                pc = [block[0] + standard_size - margin, block[1] + standard_size - 5]
            elif block[2] == "right":
                pa = [block[0] + standard_size - margin, block[1] + standard_size / 2]
                pb = [block[0] + margin, block[1] + margin]
                pc = [block[0] + margin, block[1] + standard_size - 5]
            elif block[2] == "up":
                pa = [block[0] + standard_size / 2, block[1] + margin]
                pb = [block[0] + margin, block[1] + standard_size - margin]
                pc = [block[0] + standard_size - margin, block[1] + standard_size - 5]
            elif block[2] == "down":
                pa = [block[0] + standard_size / 2, block[1] + standard_size - margin]
                pb = [block[0] + margin, block[1] + margin]
                pc = [block[0] + standard_size - margin, block[1] + margin]
            pg.draw.polygon(screen, black, (pa,pb,pc))

    elif type == "plat":
        for block in blocks:
            pg.draw.rect(screen, grey, (block[:2], [standard_size, standard_size]))
            if block[2] == "left":
                start_pos = block[:2]
                end_pos = [block[0], block[1]+standard_size - 1]
            elif block[2] == "right":
                start_pos = [block[0] + standard_size, block[1]]
                end_pos = [block[0] + standard_size, block[1] + standard_size - 1]
            elif block[2] == "up":
                start_pos = block[:2]
                end_pos = [block[0] + standard_size - 1, block[1]]
            elif block[2] == "down":
                start_pos = [block[0], block[1]+standard_size]
                end_pos = [block[0] + standard_size - 1, block[1] + standard_size]
            pg.draw.line(screen, orange, start_pos, end_pos, width=3)

    elif type == "las":
        for block in blocks:
            pg.draw.circle(screen, white, block[:2], standard_size / 2)
            pg.draw.circle(screen, white, block[:2], block[2], width=1)


def draw_exit_player(screen,exit,player):

    WHITE = (255, 255, 255)
    screen.fill(BLACK)
    if exit is not None:
        pg.draw.rect(screen, WHITE, (exit, [30, 30]), width=2)
    if player is not None:
        pg.draw.rect(screen, WHITE, (player, [30, 30]))


def drawcon(screen,key_lock_list):  # draw a red line between lock and key

    RED = (255,0,0)
    for kl in key_lock_list:
        if len(kl) == 2:
            xl = kl[1][0] - kl[0][0]    # x length of line

            corner = [kl[0][0] + xl, kl[0][1]]
            pg.draw.line(screen, RED, kl[0], corner)
            pg.draw.line(screen, RED, kl[1], corner)


def get_block_pos(pos):
    sz = 30
    pos[0] -= (pos[0] % sz)
    pos[1] -= (pos[1] % sz)

    return [pos[0],pos[1]]


def get_circ_pos(pos):
    sz = 30
    pos[0] = pos[0] - (pos[0] % sz) + sz/2
    pos[1] = pos[1] - (pos[1] % sz) + sz/2

    return [pos[0],pos[1]]


def transf_to_dic(blocks,breakable,exit,player,key_lock,enemy_list,platform_list,laser_list):

    dic = {"player": player, "exit": exit, "blocks": blocks, "breakable": breakable, "key_lock": key_lock, "enemies": enemy_list, "platforms": platform_list, "lasers": laser_list}
    return dic


def choose_nbr():
    choosing_speed = True
    speed = ""
    while choosing_speed:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_0:
                    speed += "0"
                elif event.key == pg.K_1:
                    speed += "1"
                elif event.key == pg.K_2:
                    speed += "2"
                elif event.key == pg.K_3:
                    speed += "3"
                elif event.key == pg.K_4:
                    speed += "4"
                elif event.key == pg.K_5:
                    speed += "5"
                elif event.key == pg.K_6:
                    speed += "6"
                elif event.key == pg.K_7:
                    speed += "7"
                elif event.key == pg.K_8:
                    speed += "8"
                elif event.key == pg.K_9:
                    speed += "9"
                elif event.key == pg.K_RETURN:
                    choosing_speed = False
    return int(speed)



HEIGHT = 900
WIDTH = 1440
BLACK = (0,0,0)
clock = pg.time.Clock()

running = True
draw = False
pl_tru = False
ex_tru = False
editing = False

block_list = []
breakable_list = []
key_lock_list = []
enemy_list = []

op = input("What operation do you wish to perform? (add - a / edit - e / delete - d)\n> ")

if op == "e":
    lvlnr = int(input("Which level do you want to change? ")) - 1
    f = open("lvl_info", "r")
    data = json.load(f)
    f.close()
    exit = data[lvlnr]["exit"]
    player = data[lvlnr]["player"]
    block_list = data[lvlnr]["blocks"]
    breakable_list = data[lvlnr]["breakable"]
    key_lock_list = data[lvlnr]["key_lock"]
    enemy_list = data[lvlnr]["enemies"]
    platform_list = data[lvlnr]["platforms"]
    laser_list = data[lvlnr]["lasers"]
    editing = True

elif op == "d":
    lvlnr = int(input("Which level do you want to delete? ")) - 1
    try:
        f = open("lvl_info", "r")
        data = json.load(f)
        f.close()
        del data[lvlnr]
        f = open("lvl_info", "w")
        f.write(json.dumps(data))
        f.close()
        print("Level removed successfully.")
    except:
        print("Something went wrong, check your data.")

elif op == "a":
    exit = None
    player = None
    block_list = []
    breakable_list = []
    key_lock_list = []
    enemy_list = []
    platform_list = []
    laser_list = []

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Editor')
keys = pg.key.get_pressed()
add_mover = False

while running and op != "d":

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
                    data[lvlnr] = transf_to_dic(block_list, breakable_list, exit, player, key_lock_list, enemy_list, platform_list, laser_list)
                    print(f"Level {lvlnr + 1} altered successfully.")
                else:
                    data.append(transf_to_dic(block_list, breakable_list, exit, player, key_lock_list, enemy_list, platform_list, laser_list))
                    print(f"New Level successfully added.")
                f = open("lvl_info", "w")
                f.write(json.dumps(data))
                f.close()
                running = False

            if event.key == pg.K_b:
                block_pos = get_block_pos(pos)
                already_in = False
                for cnt, block in enumerate(breakable_list):
                    if block == block_pos:
                        breakable_list.remove(block_pos)
                        already_in = True
                        screen.fill(BLACK)
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

            if event.key == pg.K_e:
                mover_list = enemy_list
                add_mover = True

            if event.key == pg.K_p:
                mover_list = platform_list
                add_mover = True

            if event.key == pg.K_c:
                circ_pos = get_circ_pos(pos)
                already_in = False
                for cnt, laser in enumerate(laser_list):
                    if laser[:2] == circ_pos:
                        laser_list.remove(laser)
                        already_in = True
                        screen.fill(BLACK)
                        break
                if not already_in:
                    choosing_rad = True
                    print("Waiting for sphere of influence, RETURN to end..")
                    rad = choose_nbr()
                    laser_list.append([circ_pos[0],circ_pos[1],rad])

            if add_mover:
                block_pos = get_block_pos(pos)
                already_in = False
                for cnt, block in enumerate(mover_list):
                    if block[:2] == block_pos:
                        mover_list.remove(block)
                        already_in = True
                        screen.fill(BLACK)
                if not already_in:
                    choosing_dir = True
                    print("Waiting for direction..")
                    while choosing_dir:
                        for event in pg.event.get():
                            if event.type == pg.KEYDOWN:
                                if event.key == pg.K_UP:
                                    direc = "up"
                                    choosing_dir = False
                                elif event.key == pg.K_DOWN:
                                    direc = "down"
                                    choosing_dir = False
                                elif event.key == pg.K_RIGHT:
                                    direc = "right"
                                    choosing_dir = False
                                elif event.key == pg.K_LEFT:
                                    direc = "left"
                                    choosing_dir = False
                    print("Waiting for speed, RETURN to end..")
                    speed = choose_nbr()
                    mover = [block_pos[0],block_pos[1],direc,speed]
                    mover_list.append(mover)
                add_mover = False


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
                        break
                if not already_in:
                    block_list.append(block_pos)

            if event.button == 2:
                player = get_block_pos(pos)
            if event.button == 3:
                exit = get_block_pos(pos)

    draw_exit_player(screen,exit,player)
    drawblocks(screen,block_list,"nb")
    drawblocks(screen,breakable_list,"b")
    drawblocks(screen, key_lock_list, "lk")
    drawblocks(screen, enemy_list, "e")
    drawblocks(screen, platform_list, "plat")
    drawblocks(screen, laser_list, "las")
    drawcon(screen,key_lock_list)
    pg.display.update()
