import pygame as pg


class Player:

    def __init__(self,x,y,x_s,y_s):
        self.pos = [x,y]
        self.size = [x_s,y_s]

    def draw(self,screen):
        white = (255, 255, 255)
        pg.draw.rect(screen, white, (self.pos, self.size))
        pg.display.update()

    def move(self,dir,screen):
        black = (0,0,0)
        speed = 10  # needs divide 30, 900, 1600
        pg.draw.rect(screen, black, (self.pos, self.size))
        if dir == "up":
            self.pos[1] -= speed
        elif dir == "down":
            self.pos[1] += speed
        elif dir == "right":
            self.pos[0] += speed
        elif dir == "left":
            self.pos[0] -= speed

    def edge_check(self,width,height,dir):
        if (self.pos[0] == 0 and dir == "left") \
                or (self.pos[0] == width - self.size[0] and dir == "right") \
                or (self.pos[1] == 0 and dir == "up") \
                or (self.pos[1] == height - self.size[1] and dir == "down"):
            return True
        return False

    def collision_check(self, all_blocks, dir, screen):
        for block in all_blocks:
            if (self.pos[0] == block.pos[0] + block.size[0] and dir == "left" and self.pos[1] == block.pos[1]) \
                    or (self.pos[0] == block.pos[0] - self.size[0] and dir == "right" and self.pos[1] == block.pos[1]) \
                    or (self.pos[1] == block.pos[1] + block.size[1] and dir == "up" and self.pos[0] == block.pos[0]) \
                    or (self.pos[1] == block.pos[1] - self.size[0] and dir == "down" and self.pos[0] == block.pos[0]):
                if block.type == "breakable":
                    block.remove(screen)
                return block.pos
        return None

    def on_lk(self,lk,dir,i):
        sz = 30
        if lk[0].pos[0] is not None:
            if (self.pos[0] == lk[i].pos[0] + sz and dir == "left" and self.pos[1] == lk[i].pos[1]) \
                    or (self.pos[0] == lk[i].pos[0] - sz and dir == "right" and self.pos[1] == lk[i].pos[1]) \
                    or (self.pos[1] == lk[i].pos[1] + sz and dir == "up" and self.pos[0] == lk[i].pos[0]) \
                    or (self.pos[1] == lk[i].pos[1] - sz and dir == "down" and self.pos[0] == lk[i].pos[0]):
                return True
        return False

    def exit_check(self, exit):
        if self.pos[0] == exit.pos[0] and self.pos[1] == exit.pos[1]:
            return True
        return False