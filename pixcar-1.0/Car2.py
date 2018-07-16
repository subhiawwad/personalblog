import copy
import os
import utils
import pygame
from pygame.locals import *
import math

### clase Car2, es el coche de los demas jugadores ###
class Car2(pygame.sprite.Sprite):

    def __init__(self, circuit, angle, crono, car = 'kart', indice=0):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.conf = open(os.path.join('data','car',car,'conf.txt'))
        self.screen = pygame.display.get_surface()
        self.name = "lan"
        self.circuit = circuit
        self.crono = crono
        #self.car_sound = utils.load_sound('car.wav')
        #self.car_sound_start = utils.load_sound('car_start.wav')
    #propiedades del player
    #cargando de fichero
        fullpath = os.path.join('data','car',car, car+str(indice)+'.png')

        for line in self.conf.readlines():
            if line[0:3] == "img":
                self.car = line[4:-1] #imagen del coche
            elif line[0:3] == "max":
                self.maxSpeed = float(line[4:-1])  #velocidad maxima
            elif line[0:3] == "low":
                self.low = float(line[4:-1])   #velocidad fuera de pista
            elif line[0:3] == "acc":
                self.acc = float(line[4:-1])   #aceleracion
            elif line[0:3] == "fre":
                self.frenos = float(line[4:-1])  #aceleracion de frenado
            elif line[0:3] == "gir":
                self.giro = float(line[4:-1])  #angulo de giro
        self.conf.close()

        self.angle = angle #angulo inicial

        self.car = os.path.join('car',car, car+str(indice)+'.png')
        self.image, self.rect = utils.load_image(self.car, -1)   #la imagen del coche

        self.centerx = self.screen.get_width()/2    #la posicion, se pone en el centro
        self.centery = self.screen.get_height()/2

        self.inix = math.fabs(self.circuit.rect.left)
        self.iniy = math.fabs(self.circuit.rect.top)

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

    #control del player
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

        self.red = 0

        #self.car_sound.play(-1)
        
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        #color del IA
        #self.set_color((0,0,190,255));

        if pygame.font:
            self.font = pygame.font.Font(None, 20)
            self.text = self.font.render(self.name, 1, (250,250,250,250))
            self.textpos = (self.rect.centerx-self.text.get_width()/2, self.rect.centery + self.image.get_height()/2)


        self.flag = 0
        self.killed = None


    def lap_update(self):
        """mira si pasas por la linea de meta y actualiza las vueltas"""

        if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (255,0,0,255):
            self.red = 1
        elif self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,0,255,255) and self.red:
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
            if self.left == 1:
                self.rotate_left()
            elif self.right == 1:
                self.rotate_right()

        self.difx = self.inix - math.fabs(self.circuit.rect.left)
        self.dify = self.iniy - math.fabs(self.circuit.rect.top)

        self.inix = math.fabs(self.circuit.rect.left)
        self.iniy = math.fabs(self.circuit.rect.top)

        self.rect.centerx = self.rect.centerx + self.difx
        self.rect.centery = self.rect.centery + self.dify
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
        
        self.rect.centerx = self.rect.centerx + self.dirx * self.speed
        self.rect.centery = self.rect.centery - self.diry * self.speed
    
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
            
            self.rect.centerx = self.rect.centerx + self.dirx * self.speed
            self.rect.centery = self.rect.centery - self.diry * self.speed

            self.derrx = self.dirx
            self.derry = self.diry
        
        self.lap_update()
        

    def move_down(self):
        """marcha atras"""
        self.rect.centerx = self.rect.centerx - self.dirx * self.low
        self.rect.centery = self.rect.centery + self.diry * self.low
        
          

    def derrapar(self):
        """derrapando"""
        if self.speed <= 0:
            self.speed = 0
        else:
            self.speed = self.speed - self.frenos
            
            if self.circuit.getpix(self.rect.centerx, self.rect.centery) == (0,0,0,255) and self.speed > self.low:
                self.speed = self.low
    
            self.rect.centerx = self.rect.centerx + self.derrx * self.speed
            self.rect.centery = self.rect.centery - self.derry * self.speed
        

        self.lap_update()


    def rotate_left(self):
        """gira a la izquierda"""
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
        center = self.rect.center
        self.angle = self.angle - self.giro
        self.dirx = math.cos(math.radians(self.angle))
        self.diry = math.sin(math.radians(self.angle))
        if self.angle <= 0:
            self.angle = 360
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center = center)

    def apply_angle(self):
        """gira el coche y lo pone con el angulo"""
        center = self.rect.center
        self.dirx = math.cos(math.radians(self.angle))
        self.diry = math.sin(math.radians(self.angle))
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center = center)

        

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
        #self.car_sound.stop()
        stop = 1


    def set_pos(self, x, y, angle = 0):
        self.rect.centerx = x + self.circuit.rect.left
        self.rect.centery = y + self.circuit.rect.top
        self.angle = angle
        self.apply_angle()

    def get_pos(self):
        return self.rect.centerx - self.circuit.rect.left ,\
         self.rect.centery - self.circuit.rect.top 
    
    def set_name(self,nombre):
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




