import pygame as pg
import time
import numpy as np


class Laser:

    def __init__(self,x,y,soi):
        self.pos = [x, y]
        self.soi = soi  # sphere of influence
        self.rad = 15  # gun radius
        self.on = False  # state of whether on or off
        self.firing = False # state of whether firing or not (included in on)
        self.laser_end = None   # end of laser
        self.fire_start = None

    def draw(self,screen,player):
        white = (255,255,255)
        red = (255,0,0)
        black = (0,0,0)
        margin = 5
        refire = 5  # seconds between laser firing
        shoot = 2   # aiming for 2 seconds, shooting for 3 seconds
        t = 100  # multiplier for line equation
        pg.draw.circle(screen, white, self.pos, self.rad)
        pg.draw.circle(screen,black,self.pos,self.rad - margin,width = 1)
        pg.draw.circle(screen,black,self.pos,self.rad - 2*margin,width = 1)

        curr_time = time.time()

        if self.player_in_soi(player) and not self.on:  # turn laser on
            cop = [player.pos[0] + player.size[0]/2,player.pos[1] + player.size[1]/2]   # center of player
            self.laser_end = list(np.array(self.pos) + t * (np.array(cop) - np.array(self.pos)))    # line equation
            self.on = True
            self.fire_start = curr_time

        if self.on and curr_time - self.fire_start >= refire:   # turn laser off
            self.on = False
            self.firing = False
            pg.draw.line(screen, black, self.pos, self.laser_end, width=3)   # erase laser
        elif self.on and curr_time - self.fire_start < shoot:   # aim laser
            pg.draw.line(screen, red, self.pos, self.laser_end, width=1)
        elif self.on and curr_time - self.fire_start >= shoot:  # shoot laser
            self.firing = True
            pg.draw.line(screen,red, self.pos, self.laser_end, width=2)

    def player_in_soi(self,player):
        ceq = (player.pos[0] - self.pos[0])**2 + (player.pos[1] - self.pos[1])**2   # left hand side of circle equation
        if np.sqrt(ceq) <= self.soi:
            return True
        else:
            return False