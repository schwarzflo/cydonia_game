import pygame as pg


class Player:

    def __init__(self,x,y,x_s,y_s,speed,dir):
        self.pos = [x,y]
        self.size = [x_s,y_s]
        self.speed = speed # needs divide 30, 900, 1600
        self.dir = dir

    def draw(self,screen):
        white = (255, 255, 255)
        pg.draw.rect(screen, white, (self.pos, self.size))

    def move(self,screen):
        black = (0,0,0)
        pg.draw.rect(screen, black, (self.pos, self.size))
        if self.dir == "up":
            self.pos[1] -= self.speed
        elif self.dir == "down":
            self.pos[1] += self.speed
        elif self.dir == "right":
            self.pos[0] += self.speed
        elif self.dir == "left":
            self.pos[0] -= self.speed

    def edge_check(self,width,height):
        if (self.pos[0] == 0 and self.dir == "left") \
                or (self.pos[0] == width - self.size[0] and self.dir == "right") \
                or (self.pos[1] == 0 and self.dir == "up") \
                or (self.pos[1] == height - self.size[1] and self.dir == "down"):
            return True
        return False

    def collision_check(self, all_blocks, screen):
        for block in all_blocks:
            if (self.pos[0] == block.pos[0] + block.size[0] and self.dir == "left" and self.pos[1] == block.pos[1]) \
                    or (self.pos[0] == block.pos[0] - self.size[0] and self.dir == "right" and self.pos[1] == block.pos[1]) \
                    or (self.pos[1] == block.pos[1] + block.size[1] and self.dir == "up" and self.pos[0] == block.pos[0]) \
                    or (self.pos[1] == block.pos[1] - self.size[0] and self.dir == "down" and self.pos[0] == block.pos[0]):
                if block.type == "breakable":
                    block.remove(screen)
                return block.pos
        return None

    def on_lk(self,lk,i):
        sz = 30
        if lk[0].pos[0] is not None:
            if (self.pos[0] == lk[i].pos[0] + sz and self.dir == "left" and self.pos[1] == lk[i].pos[1]) \
                    or (self.pos[0] == lk[i].pos[0] - sz and self.dir == "right" and self.pos[1] == lk[i].pos[1]) \
                    or (self.pos[1] == lk[i].pos[1] + sz and self.dir == "up" and self.pos[0] == lk[i].pos[0]) \
                    or (self.pos[1] == lk[i].pos[1] - sz and self.dir == "down" and self.pos[0] == lk[i].pos[0]):
                return True
        return False

    def exit_check(self, exit):
        if self.pos[0] == exit.pos[0] and self.pos[1] == exit.pos[1]:
            return True
        return False

    def enemy_collision(self, enemy): # can be made easier! blocks collide on edge, are never inside one another!
        # check for collision not head on
        if ((self.pos[0] > enemy.pos[0] and self.pos[0] < enemy.pos[0] + enemy.size[0]) and (self.pos[1] > enemy.pos[1] and self.pos[1] < enemy.pos[1] + enemy.size[1])) \
                or ((self.pos[0] > enemy.pos[0] and self.pos[0] < enemy.pos[0] + enemy.size[0]) and (self.pos[1] + self.size[1] > enemy.pos[1] and self.pos[1] + self.size[1] < enemy.pos[1] + enemy.size[1])) \
                or ((self.pos[0] + self.size[0] > enemy.pos[0] and self.pos[0] + self.size[0] < enemy.pos[0] + enemy.size[0]) and (self.pos[1] > enemy.pos[1] and self.pos[1] < enemy.pos[1] + enemy.size[1])) \
                or ((self.pos[0] + self.size[0] > enemy.pos[0] and self.pos[0] + self.size[0] < enemy.pos[0] + enemy.size[0]) and (self.pos[1] + self.size[1] > enemy.pos[1] and self.pos[1] + self.size[1] < enemy.pos[1] + enemy.size[1])):
            return True
        # check for collision head on
        elif self.pos[0] > enemy.pos[0] and self.pos[0] < enemy.pos[0] + enemy.size[0] and self.pos[1] == enemy.pos[1] \
            or self.pos[1] > enemy.pos[1] and self.pos[1] < enemy.pos[1] + enemy.size[1] and self.pos[0] == enemy.pos[0] \
            or self.pos[0] + self.size[0] > enemy.pos[0] and self.pos[0] + self.size[0] < enemy.pos[0] + enemy.size[0] and self.pos[1] == enemy.pos[1] \
            or self.pos[1] + self.size[1] > enemy.pos[1] and self.pos[1] + self.size[1] < enemy.pos[1] + enemy.size[1] and self.pos[0] == enemy.pos[0]:
            return True
        else:
            return False

    def platform_collision(self, platform):     # distinguish between the player moving (left,right,up,down) and the player standing still
        if (self.dir == "left" and self.pos[0] <= platform.pos[0] + platform.size[0] and self.pos[0] >= platform.pos[0] \
            and ((self.pos[1] <= platform.pos[1] and self.pos[1] + self.size[1] > platform.pos[1]) or (self.pos[1] < platform.pos[1] + platform.size[1] and self.pos[1] + self.size[1] >= platform.pos[1] + platform.size[1]))) \
            or (self.dir == "right" and self.pos[0] + self.size[0] >= platform.pos[0] and  self.pos[0] + self.size[0] <= platform.pos[0] + platform.size[0] \
            and ((self.pos[1] <= platform.pos[1] and self.pos[1] + self.size[1] > platform.pos[1]) or (self.pos[1] < platform.pos[1] + platform.size[1] and self.pos[1] + self.size[1] >= platform.pos[1] + platform.size[1]))) \
            or (self.dir == "up" and self.pos[1] <= platform.pos[1] + platform.size[1] and self.pos[1] >= platform.pos[1] \
            and ((self.pos[0] <= platform.pos[0] and self.pos[0] + self.size[0] > platform.pos[0]) or (self.pos[0] < platform.pos[0] + platform.size[0] and self.pos[0] + self.size[0] >= platform.pos[0] + platform.size[0]))) \
            or (self.dir == "down" and self.pos[1] + self.size[1] >= platform.pos[1] and  self.pos[1] + self.size[1] <= platform.pos[1] + platform.size[1] \
            and ((self.pos[0] <= platform.pos[0] and self.pos[0] + self.size[0] > platform.pos[0]) or (self.pos[0] < platform.pos[0] + platform.size[0] and self.pos[0] + self.size[0] >= platform.pos[0] + platform.size[0]))) \
            or (self.dir == "" and ((self.pos[1] == platform.pos[1] and self.pos[0] > platform.pos[0] and self.pos[0] < platform.pos[0] + platform.size[0]) \
                                    or (self.pos[1] == platform.pos[1] and self.pos[0] + self.size[0] > platform.pos[0] and self.pos[0] + self.size[0] < platform.pos[0] + platform.size[0]) \
                                    or (self.pos[0] == platform.pos[0] and self.pos[1] > platform.pos[1] and self.pos[1] < platform.pos[1] + platform.size[1]) \
                                    or (self.pos[0] == platform.pos[0] and self.pos[1] + self.size[1] > platform.pos[1] and self.pos[1] + self.size[1] < platform.pos[1] + platform.size[1]))):
            return True
        return False