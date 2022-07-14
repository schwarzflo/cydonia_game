import pygame as pg


class Mover:

    def __init__(self,x,y,x_s,y_s,dir,speed,type):
        self.pos = [x,y]
        self.size = [x_s,y_s]
        self.dir = dir
        self.speed = speed
        self.type = type    # distinguish between enemy and platform

    def draw(self,screen,color):
        orange = (209,148,24)
        pg.draw.rect(screen, color, (self.pos, self.size))
        if self.type == "platform":     # mark edge of movement direction; -1 because line draws one px too far
            if self.dir == "left":
                start_pos = self.pos
                end_pos = [self.pos[0], self.pos[1]+self.size[1] - 1]
            elif self.dir == "right":
                start_pos = [self.pos[0] + self.size[0], self.pos[1]]
                end_pos = [self.pos[0] + self.size[0], self.pos[1] + self.size[1] - 1]
            elif self.dir == "up":
                start_pos = self.pos
                end_pos = [self.pos[0] + self.size[0] - 1, self.pos[1]]
            elif self.dir == "down":
                start_pos = [self.pos[0], self.pos[1]+self.size[1]]
                end_pos = [self.pos[0] + self.size[0] - 1, self.pos[1] + self.size[1]]
            pg.draw.line(screen,orange,start_pos,end_pos,width=3)

    def move(self,screen):
        black = (0,0,0)  # needs divide 30, 900, 1600
        pg.draw.rect(screen, black, (self.pos, self.size))

        if self.dir == "up":
            self.pos[1] -= self.speed
        elif self.dir == "down":
            self.pos[1] += self.speed
        elif self.dir == "right":
            self.pos[0] += self.speed
        elif self.dir == "left":
            self.pos[0] -= self.speed

    def block_collision(self,block_list):
        for block in block_list:
            if (self.pos[0] == block.pos[0] + block.size[0] and self.dir == "left" and self.pos[1] == block.pos[1]) \
                    or (self.pos[0] == block.pos[0] - self.size[0] and self.dir == "right" and self.pos[1] == block.pos[1]) \
                    or (self.pos[1] == block.pos[1] + block.size[1] and self.dir == "up" and self.pos[0] == block.pos[0]) \
                    or (self.pos[1] == block.pos[1] - self.size[0] and self.dir == "down" and self.pos[0] == block.pos[0]):
                return True
        return False

    def edge_collision(self,width,height):
        if (self.pos[0] == 0 and self.dir == "left") \
                or (self.pos[0] == width - self.size[0] and self.dir == "right") \
                or (self.pos[1] == 0 and self.dir == "up") \
                or (self.pos[1] == height - self.size[1] and self.dir == "down"):
            return True
        return False


