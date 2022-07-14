import pygame as pg


class Object:

    def __init__(self,x,y,x_s,y_s):
        self.pos = [x,y]
        self.size = [x_s,y_s]

    def draw(self,screen,color):
            pg.draw.rect(screen, color, (self.pos, self.size))

    def draw_b(self,screen,color):
        if self.pos[0] is not None:     # check if empty input in lvl_info
            pg.draw.rect(screen, color, ([self.pos[0] + 10,self.pos[1] + 10], self.size))

    def draw_l(self,screen,color):
        black = (0,0,0)
        if self.pos[0] is not None:
            pg.draw.rect(screen, color, (self.pos, self.size))
            pg.draw.rect(screen, black, ([self.pos[0] + 10,self.pos[1] + 10], [10,10]))