import pdb
import pygame
import math
import time
from textos import *
from pygame.locals import *

class Crono:
    def __init__(self, clock):
        self.time = 0
        self.lap = -1
        self.textcolor = (0, 0, 0)
        self.color = (255, 250, 0)
        self.string = ""
        self.screen = pygame.display.get_surface()
        self.surf = pygame.Surface((self.screen.get_width(), 30))
        self.surf.convert()
        self.surf.fill(self.color)
        self.surf.set_alpha(150)
        self.inc = 0
        self.min = 0
        self.sec = 0
        self.state = 0
        self.pos = (0,(self.screen.get_height() - 150)/2)
        self.fps = 40
        self.clock = clock
        self.inicial = time.time()

#estado inicial
        if pygame.font:
            self.font = pygame.font.Font(None, 36)
            self.text = self.font.render(idioma.lang.time + ' %(var).01f ' %{'var': self.time*1.0 / self.fps} + idioma.lang.lap +' %(lap)d    '+ idioma.lang.ready %{'lap': self.lap}, 1, self.textcolor)
            self.surf.fill(self.color)
            self.textpos = (self.surf.get_width()/2, 5)
            self.surf.blit(self.text, self.textpos)

#update
    def update(self):
    #inicio
        if self.inc != 0:
            self.sec = time.time() - self.inicial
        if self.sec > 60:
            self.min +=1
            self.sec -= 60
            self.inicial = time.time()
        if self.state == 0:
            self.sec = time.time() - self.inicial
            texto = idioma.lang.ready + ' %(ready)d' %{'ready': int(3 - self.sec)}

            self.text = self.font.render(texto, 1, self.textcolor)
            self.textpos = ((self.surf.get_width() - self.font.size(texto)[0])/2, 5)
            self.surf.fill(self.color)
            self.surf.blit(self.text, self.textpos)
            if self.sec >= 3:
                self.crono_reset()
                self.crono_start()
    #corriendo
        else:
        #has acabado
            if self.inc == 0:
                texto = idioma.lang.complete + ' %(min)02d:%(var)02.02f  ' %{'min': self.min, 'var': self.sec} + idioma.lang.lap +' %(lap)d' %{'lap': self.lap}
                self.pos = (0,(self.screen.get_height() - 150)/2)
                self.textpos = ((self.surf.get_width() - self.font.size(texto)[0])/2, 5)
                self.text = self.font.render(texto, 1, (210, 10, 10))
            #se esperan 3 segundos
                
                if time.time()-self.inicial > self.sec + 3:
                    return 1

            
        #en carrera
            else:
                self.textpos = (5, 5)
                self.pos = (0,0)
                self.text = self.font.render( idioma.lang.time + ' %(min)02d:%(var)02.01f  ' %{'min': self.min, 'var': self.sec} +idioma.lang.lap+' %(lap)d   %(text)s' %{'lap': self.lap, 'text': self.string}, 1, self.textcolor)
            self.surf.fill(self.color)
            self.surf.blit(self.text, self.textpos)

    def uptime(self):
        self.inicial = time.time()

    def inclap(self, lap, total):
        self.lap += lap
        if self.lap == total:
            self.inc = 0
            return 1

    def crono_start(self):
        self.inicial = time.time()
        self.inc = 1
        self.state = 1

    def crono_stop(self):
        self.inc = 0
        self.state = 0

    def crono_reset(self):
        self.min = 0
        self.sec = 0
        self.inicial = time.time()
        self.state = 1

    def crono_state(self):
        return self.state

    def crono_settext(self, text):
        self.string = text

    def get_time(self):
        return (self.min * 60 + self.sec)
    def get_fps(self):
        if self.clock.get_fps()>0:
            return self.clock.get_fps()
        else:
            return self.fps
