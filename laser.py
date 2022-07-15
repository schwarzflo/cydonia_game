import pygame as pg
import time
import numpy as np


class Laser:

    def __init__(self,x,y,soi):
        self.pos = [x, y]
        self.soi = soi  # sphere of influence
        self.rad = 15  # gun radius
        self.firing = False  # state of firing or not
        self.laser_end = None   # end of laser
        self.fire_start = None

    def draw(self,screen,player):
        white = (255,255,255)
        red = (255,0,0)
        black = (0,0,0)
        margin = 5
        pg.draw.circle(screen, white, self.pos, self.rad)
        pg.draw.circle(screen,black,self.pos,self.rad - margin,width = 1)
        pg.draw.circle(screen,black,self.pos,self.rad - 2*margin,width = 1)

        curr_time = time.time()
        if self.fire_start is not None and curr_time - self.fire_start >= 3:    # 3 seconds between laser firing
            self.firing = False

        if self.player_in_soi(player) and not self.firing:
            if self.laser_end is not None:
                pg.draw.line(screen, black, self.pos, self.laser_end)
            self.laser_end = [player.pos[0] + player.size[0]/2,player.pos[1] + player.size[1]/2]
            self.firing = True
            self.fire_start = time.time()

        if self.firing:
            pg.draw.line(screen,red, self.pos, self.laser_end)

    def player_in_soi(self,player):
        return True