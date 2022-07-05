import pygame as pg

class Exit:

    def __init__(self,x,y,x_s,y_s):
        self.pos = [x,y]
        self.size = [x_s,y_s]

    def draw(self,screen):
        white = (255, 255, 255)
        pg.draw.rect(screen, white, (self.pos, self.size),width = 1)
        pg.display.update()