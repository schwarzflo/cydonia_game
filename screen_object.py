import pygame as pg


class Object:

    def __init__(self,x,y,x_s,y_s):
        self.pos = [x,y]
        self.size = [x_s,y_s]

    def draw(self,screen,color):
        if self.pos[0] is not None:
            pg.draw.rect(screen, color, (self.pos, self.size))
            pg.display.update()

    def draw_b(self,screen,color):
        if self.pos[0] is not None:
            pg.draw.rect(screen, color, ([self.pos[0] + 8,self.pos[1] + 8], self.size))
            pg.display.update()