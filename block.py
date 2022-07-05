import pygame as pg

class Block:

    def __init__(self,x,y,x_s,y_s,type):
        self.pos = [x,y]
        self.size = [x_s,y_s]
        self.type = type

    def draw(self,screen):
        grey = (125, 125, 125)
        black = (0,0,0)
        if self.type == "blocks":
            pg.draw.rect(screen, grey, (self.pos, self.size))
        elif self.type == "breakable":
            pg.draw.rect(screen, grey, (self.pos, self.size))
            pg.draw.line(screen, black, (self.pos[0],self.pos[1]),
                         (self.pos[0]+self.size[0]-1,self.pos[1]+self.size[1]-1),width = 2)
            pg.draw.line(screen, black, (self.pos[0], self.pos[1] + self.size[1]-1),
                         (self.pos[0] + self.size[0]-1, self.pos[1]),width = 2)
        pg.display.update()

    def remove(self,screen):
        black = (0, 0, 0)
        pg.draw.rect(screen, black, (self.pos, self.size))