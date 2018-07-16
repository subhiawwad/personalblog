import copy
import os
import utils
import pygame
from pygame.locals import *
import math


################ Wiimote control import WMD #############

import sys
sys.path.append('.')

from wmd.Common import *
from wmd.Config import CFG
from wmd.UI.UIManager import UIManager
from wmd.Wiimote.WMManager import WMManager
from wmd.EVDispatcher import EVDispatcher
from wmd.MotionSensing import MSManager
from wmd.Pointer import POManager
from wmd.CommandMapper import CommandMapper
import threading

###############Thread for wimote event###################

class wm_control (threading.Thread):
    def __init__(self, callback_acc, callback_button):
        self.cf = CFG
        self.ev = EVDispatcher(self.cf)
        self.wm = WMManager(self.cf, self.ev)

        self.ev.subscribe( WM_ACC, callback_acc ) 
        self.ev.subscribe( WM_BT, callback_button ) 

        threading.Thread.__init__(self)

    def run(self):
        if self.wm.connect() and self.wm.setup():
            self.wm.main_loop()

#########################################################

### clase Car, el coche del player ###
class Car(pygame.sprite.Sprite):
    """El coche del jugador principal"""

    def __init__(self, circuit, angle, crono, car = 'kart', indice=0, controles = (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a)):

        
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.conf = open(os.path.join('data','car',car,'conf.txt'))
        self.screen = pygame.display.get_surface()
        self.name = car
        self.circuit = circuit
        self.crono = crono
        #self.car_sound = utils.load_sound('car.wav')
        #self.car_sound_start = utils.load_sound('car_start.wav')
    #propiedades del player
    #cargando de fichero

        for line in self.conf.readlines():
            if line[0:3] == "img":
                self.car = line[4:-1] #imagen del coche
            elif line[0:3] == "max":
                self.maxSpeed = float(line[4:-1])  #velocidad maxima
                self.max_original = self.maxSpeed
            elif line[0:3] == "low":
                self.low = float(line[4:-1])   #velocidad fuera de pista
            elif line[0:3] == "acc":
                self.acc = float(line[4:-1])   #aceleracion
            elif line[0:3] == "fre":
                self.frenos = float(line[4:-1])  #aceleracion de frenado
            elif line[0:3] == "gir":
                self.giro = float(line[4:-1])  #angulo de giro
                self.giro_original = self.giro
        self.conf.close()

        self.angle = angle #angulo inicial

        self.car = os.path.join('car',car, car+str(indice)+'.png')
        self.image, self.rect = utils.load_image(self.car, -1)   #la imagen del coche
        self.centerx = self.screen.get_width()/2    #la posicion, se pone en el centro, solo se mueve el fondo
        self.centery = self.screen.get_height()/2

        if pygame.font:
            self.font = pygame.font.Font(None, 20)
            self.text = self.font.render(self.name, 1, (250,250,250,250))
            self.textpos = (self.rect.centerx-self.text.get_width()/2, self.rect.centery + self.image.get_height()/2)

        self.rect.center = (self.centerx, self.centery)
        self.original = copy.copy(self.image)
        self.sacar_color_car()
        self.speed = 0      #velocidad inicial
        self.dirx = math.cos(math.radians(self.angle)) #incremento de x e y
        self.diry = math.sin(math.radians(self.angle))
        self.derr = 0
        self.derrx = self.dirx
        self.derry = self.diry
        self.lap = 0
        self.record = 0
        #self.color = (255,255,255,255)

    #control del player
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

        self.red = 0

        #self.car_sound.play(-1)

    #controles
        self.kup = K_UP
        self.kdown = K_DOWN
        self.kleft = K_LEFT
        self.kright = K_RIGHT
        self.kbrake = K_a
        self.controls(controles)

        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.killed = None

        ################ wiimote control #############

        try:
            wii_control = wm_control(self.event_wii_acc, self.event_wii_button)
            self.wii_ev = wii_control.ev
            wii_control.start()
        except:
            self.wii_ev = None
            print "no se puede inicializar el wiimote...."

        ##############################################

    def controls(self, controles):
        """asigna las teclas de control, recibe las constantes de las teclas"""
        self.kup = controles[0]
        self.kdown = controles[1]
        self.kleft = controles[2]
        self.kright = controles[3]
        self.kbrake = controles[4]

    def lap_update(self):
        """mira si pasas por la linea de meta y actualiza las vueltas"""

        if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (255,0,0,255):
            self.red = 1
        elif self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,0,255,255) and self.red:
            if self.crono.inclap(1, self.circuit.laps) == 1:
                self.record = self.crono.get_time()
            self.lap += 1
            self.red = 0


    def update(self):
        """actualiza el coche"""
        if self.crono.state:
            if self.up == 1 and self.derr == 0:
                self.move_up()
            elif self.up == 2 and self.derr == 0:
                self.inercia(self.dirx, self.diry)
            if self.derr == 1:
                self.derrapar()
            elif self.down == 1:
                self.move_down()
            if self.left == 1 and self.speed > 0:
                self.rotate_left()
            elif self.left == 1 and self.down == 1 and self.speed == 0:
                self.rotate_right()
            elif self.right == 1 and self.speed >0:
                self.rotate_right()
            elif self.right == 1 and self.down == 1 and self.speed == 0:
                self.rotate_left()

        self.textpos = (self.rect.centerx-self.text.get_width()/2, self.rect.centery + self.image.get_height()/2)
        

    def move_up(self):
        """acelera el coche"""
        if self.speed >= self.maxSpeed:
            self.speed = self.maxSpeed
        else:
            self.speed = self.speed + self.acc
        
        if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,0,0,255):
            self.speed = self.low
            self.red = 0
        
        self.lap_update()

        self.circuit.scroll( -self.speed * self.dirx, self.speed * self.diry)
        if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,255,0,255):
            self.circuit.scroll( self.speed * self.dirx, -self.speed * self.diry)
            self.speed = 0
            
        self.derrx = self.dirx
        self.derry = self.diry

    def inercia(self, dirx, diry):
        """desacelera el coche"""
        if self.speed <= 0:
            self.speed = 0
        else:
            self.speed = self.speed - self.frenos
            
            if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,0,0,255) and self.speed > self.low:
                self.speed = self.low
    
            self.circuit.scroll(-self.speed * dirx, self.speed * diry)
            if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,255,0,255):
                self.circuit.scroll( self.speed * self.dirx, -self.speed * self.diry)
                self.speed = 0

            self.derrx = self.dirx
            self.derry = self.diry
        
        self.lap_update()

    def move_down(self):
        """marcha atras"""
        self.circuit.scroll(self.low * self.dirx, -self.low * self.diry)
            
    def derrapar(self):
        """derrapando"""
        if self.speed <= 0:
            self.speed = 0
        else:
            self.speed = self.speed - self.frenos*2
            
            if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,0,0,255) and self.speed > self.low:
                self.speed = self.low
    
            self.circuit.scroll(-self.speed * self.derrx, self.speed * self.derry)
            if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,255,0,255):
                self.circuit.scroll( -self.speed * self.derrx, -self.speed * self.derry)
                self.speed = 0


        self.lap_update()


    def rotate_left(self):
        """gira a la izquierda"""
        if self.speed == 0 and not self.down:
            return 0
        center = self.rect.center
        self.angle = self.angle + self.giro
        self.dirx = math.cos(math.radians(self.angle))
        self.diry = math.sin(math.radians(self.angle))
        if self.angle >= 360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center = center)

    def rotate_right(self):
        """gira a la derecha"""
        if self.speed == 0 and not self.down:
            return 0

        center = self.rect.center
        self.angle = self.angle - self.giro
        self.dirx = math.cos(math.radians(self.angle))
        self.diry = math.sin(math.radians(self.angle))
        if self.angle <= 0:
            self.angle = 360
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center = center)

    ##################### wiimote event ############################################
    def event_wii_acc(self, force):
        xforce = force['x']
        yforce = force['y']

        acc = math.fabs(((yforce - 130) / 15.0))
        self.giro = self.giro_original *(acc)
        if yforce > 131:
            self.right = 0
            self.left = 1
        elif yforce < 129:
            self.left = 0
            self.right = 1
        else:
            self.left = 0
            self.right = 0
        
        """
        acc = math.fabs(((xforce - 130) / 20.0))
        self.maxSpeed = self.max_original *(acc)
        
        if xforce > 131:
            self.down = 0
            self.up = 1
        elif xforce < 129 and self.speed == 0:
            self.up = 0
            self.down = 1
        else:
            if self.speed > 0:
                self.up = 2
                self.down = 0
        """

    def event_wii_button(self, button):
        key = button[0]
        event = button[1]
        if event == "DOWN" and key == "2":
            self.derr = 1
        if event == "UP" and key == "2":
            self.derr = 0
        if event == "DOWN" and key == "R":
            self.up = 1
        if event == "UP" and key == "R":
            self.up = 2
        if event == "DOWN" and key == "L":
            self.down = 1
        if event == "UP" and key == "L":
            self.down = 0


    ###############################################################################

    def event(self, event):
        if event.type == KEYDOWN and event.key == self.kup:
            self.up = 1
        if event.type == KEYUP and event.key == self.kup:
            self.up = 2
        if event.type == KEYDOWN and event.key == self.kdown:
            self.down = 1
        if event.type == KEYUP and event.key == self.kdown:
            self.down = 0
        if event.type == KEYDOWN and event.key == self.kleft:
            self.left = 1
        if event.type == KEYUP and event.key == self.kleft:
            self.left = 0
        if event.type == KEYDOWN and event.key == self.kright:
            self.right = 1
        if event.type == KEYUP and event.key == self.kright:
            self.right = 0
        if event.type == KEYDOWN and event.key == self.kbrake:
            self.derr = 1
        if event.type == KEYUP and event.key == self.kbrake:
            self.derr = 0


    def set_color(self, color):
        self.color = color
        """
        for i in range(0, self.image.get_width()):
            for j in range(0, self.image.get_height()):
                pix = self.image.get_at((i,j))
                if pix[0] > 100 and pix[1] < 10 and pix[2] < 10 and pix[3] == 255:
                    self.image.set_at((i,j), color)


        for i in range(0, self.original.get_width()):
            for j in range(0, self.original.get_height()):
                pix = self.original.get_at((i,j))
                if pix[0] > 100 and pix[1] < 10 and pix[2] < 10 and pix[3] == 255:
                    self.original.set_at((i,j), color)

        """

    def set_color_int(self, color):
        car_color = ((255,0,0,255),(0,255,0,255),(0,0,100,255),(255,255,0,255),(0,255,255,255),(0,0,0,255),\
        (160, 90, 190, 255), (230, 230, 230, 255), (255, 150, 0, 255), (67, 171, 0, 255), (14, 150,0, 255))
        self.set_color(car_color[color % len(car_color)])


    def stop(self):
        if self.wii_ev != None:
            self.wii_ev.send(EV_SHUTDOWN, '')
        #self.car_sound.stop()
        stop = 1

    def set_pos(self, x, y, angle = 0):
        self.circuit.rect.left = - (x-self.rect.centerx)
        self.circuit.rect.top = -(y - self.rect.centery)
        self.angle = angle

    def get_pos(self):
        return self.rect.centerx - self.circuit.rect.left ,\
         self.rect.centery - self.circuit.rect.top 
    
    def set_name(self, nombre):
        self.name = nombre
        if pygame.font:
            self.font = pygame.font.Font(None, 20)
            self.text = self.font.render(self.name, 1, (250,250,250,250))

    def sacar_color_car(self):
        """
        intenta sacar el color mas repetido de la imagen
        """
        repeticiones = 0
        color_key = self.original.get_at((0,0))
        pix2 = color_key
        pix3 = color_key
        pix3rep = 0
        for i in range(0, self.original.get_width()):
            for j in range(0, self.original.get_height()):
                pix = self.original.get_at((i,j))
                if pix != color_key:
                    if utils.color_parecido(pix2, pix):
                        repeticiones+=1
                    else:
                        pix2 = pix
                        repeticiones = 0
                    if repeticiones > pix3rep:
                        pix3 = pix
        if pix3 != (0,0,0,255):
            self.color = pix3
        else: self.color = (10,10,10,255)

        


        


