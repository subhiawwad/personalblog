import pygame
import math
from textos import *
from pygame.locals import *
import pdb

class Message(pygame.sprite.Sprite):
    def __init__(self):
        self.textcolor = (0, 0, 0)
        self.color = (255, 250, 0)
        self.buf = []
        self.lines = 1
        self.screen = pygame.display.get_surface()
        self.surf = pygame.Surface((self.screen.get_width(), 130))
        self.surf.convert()
        self.surf.fill(self.color)
        self.surf.set_alpha(70)
        self.pos = (0,30)

        for string in self.buf:
            self.font = pygame.font.Font(None, 20)
            self.text = self.font.render(string, 1, self.textcolor)
            self.surf.fill(self.color)
            self.textpos = (10, 35)
            self.surf.blit(self.text, self.textpos)
    
    def put_text(self, texto):
        self.buf = self.insertar(texto) #no funciona bien, no se actualiza
        self.surf.fill(self.color)
        index = 0
        for string in self.buf:
            self.font = pygame.font.Font(None, 20)
            self.text = self.font.render(string, 1, self.textcolor)
            self.textpos = (10, 35+(20*index))
            self.surf.blit(self.text, self.textpos)
            index += 1

    def insertar(self, texto):
        if len(self.buf) < self.lines:
            self.buf.append(texto)
            return self.buf
        ret = []
        for i in range(self.lines):
            ret.append(0)
        for i in range(self.lines-1):
            ret[i+1] = self.buf[i]
        ret[0] = texto
        return ret
            


