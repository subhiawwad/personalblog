import os
import utils
import pygame
import math
from pygame.locals import *

###clase circuit, el circuito###
class Circuit(pygame.sprite.Sprite):
    def __init__(self, circuit, laps = 0):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
    #propiedades del circuito
        self.name = circuit[0:-4]
        self.ang = 0
        self.ctx = [] #aqui se guardan una serie de posiciones inciales, hasta el numero de players
        #[(x,y),(x,y)]
        self.fg = 0

        fullname = os.path.join('data', 'circuit', circuit)
        file = open(fullname, 'r')
        for line in file.readlines():
            if line[0:3] == "cbg":
                self.circuitbg = line[4:-1] #imagen del circuito real
            elif line[0:3] == "cfg":
                self.circuit = line[4:-1] #imagen del circuito b/g
            elif line[0:3] == "cf2":
                self.fg = line[4:-1]
            elif line[0:3] == "lap":
                self.laps = int(line[4:-1]) #vueltas para completar el circuito
            elif line[0:3] == "ang":
                self.ang = int(line[4:-1]) #angulo de la recta inicial
            elif line[0:3] == "ctx":
                self.ctx.append((int(line[4:line.find(",")]),int(line[line.find(",")+1:])))

        file.close()

        if laps != 0:
            self.laps = laps

        self.circuitbg = os.path.join('circuit', self.circuitbg)
        self.circuit = os.path.join('circuit', self.circuit)
        if self.fg:
            self.fg = os.path.join('circuit', self.fg)
            self.fg, self.fg_rect = utils.load_image(self.fg, -1)

        self.image, self.rect = utils.load_image(self.circuitbg)
        self.image.convert()
        self.bg, self.rectbg = utils.load_image(self.circuit)
        self.bg.convert()
        #self.get_center()
        self.get_center2()
        
    def scroll(self, x, y):
        newpos = self.rect.move(x, y)
        ret = 1
        if newpos.left > 0:
            newpos.left = 0
            ret = 0
        elif newpos.right < self.screen.get_width():
            newpos.right = self.screen.get_width()
            ret = 0
        if newpos.top > 0:
            newpos.top = 0
            ret = 0
        elif newpos.bottom < self.screen.get_height():
            newpos.bottom = self.screen.get_height()
            ret = 0

        self.rect = newpos
        self.rectbg = newpos
        return ret

    def getpix(self, posx, posy):
        realpos = (math.fabs(self.rect.left) + posx, math.fabs(self.rect.top - posy))
        realpos = (int(realpos[0]), int(realpos[1]))
        return self.bg.get_at(realpos)
    

    def get_center2(self):
        i = self.ctx[0][0]
        j = self.ctx[0][1]
        self.rect.left = -i + self.screen.get_width() / 2 
        self.rectbg.left = -i + self.screen.get_width() / 2
        self.rect.top = - j + self.screen.get_height() / 2
        self.rectbg.top = - j + self.screen.get_height() / 2
        return 0


    def get_init_angle(self):
        return self.ang
