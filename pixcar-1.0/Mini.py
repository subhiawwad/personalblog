import pygame
import math
import os
import utils
import copy
from textos import *
from pygame.locals import *

class Mini:
    def __init__(self, circuit, car, n):
        self.circuit = circuit
        self.car = car
        self.n = n
        self.color = (255, 250, 0)
        self.screen = pygame.display.get_surface()
        self.fullpath = os.path.join(self.circuit.circuit[0:-4]+'-prev.png')
        self.preview, self.preview_rect = utils.load_image(self.fullpath, (0,0,0))
        self.circles = range(self.n)
        for i in range(0,self.n):
            self.circles[i] = Circle('circle.png', car[i])
        self.preview = pygame.transform.scale2x(self.preview)
        self.preview = utils.change_color(self.preview, (255,255,255, 255), (170, 170, 170, 255))
        self.preview = utils.change_all_minus(self.preview, (0,0,0, 255), (40, 40, 40, 200))
        self.pos = (0,self.screen.get_height()-self.preview.get_height())
        self.preview2 = copy.copy(self.preview)
        for i in self.circles:
            self.preview.blit(i.circle, (i.posx, i.posy))


#update
    def update(self):
        """ modifica la posicion del circulo, calculando donde esta el coche """
        self.preview = copy.copy(self.preview2)
        for i in self.circles:
            if i.car.killed == True:
                continue
            i.posx = self.preview.get_width()*(i.car.rect.centerx - self.circuit.rect.left) / self.circuit.image.get_width()
            i.posy = self.preview.get_height() *(i.car.rect.centery - self.circuit.rect.top) / self.circuit.image.get_height()
            i.posx = i.posx - i.circle.get_width()/2
            i.posy = i.posy - i.circle.get_height()/2
            self.preview.blit(i.circle, (i.posx, i.posy))
    
    def set_color(self, color):
        for i in self.circles:
            i.set_color()
        

class Circle:
    def __init__(self, imagen, car):
        self.circle, self.circle_rect = utils.load_image(imagen,(255,255,255))
        self.posx = 0
        self.posy = 0
        self.car = car
    def set_color(self):
        self.circle = utils.set_color_red(self.circle, self.car.color)

