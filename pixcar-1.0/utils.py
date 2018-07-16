import os, copy
import pygame
from pygame.locals import *

### funcion para cargar imagenes ###
def load_image(name, colorkey=None):
    try:
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
    

### funcion para cargar sonidos ###
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    try:
        fullname = os.path.join('data', name)
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound


##cambia algunos colores parecidos al rojo por el color determinado
def set_color_red(image, color):
    image = copy.copy(image)
    for i in range(0, image.get_width()):
        for j in range(0, image.get_height()):
            pix = image.get_at((i,j))
            if pix[0] > 100 and pix[1] < 10 and pix[2] < 10 and pix[3] == 255:
                image.set_at((i,j), color)
    return copy.copy(image)

def change_color(image, src, dst):
    """ cambia los pixels de color src a color dst """
    image = copy.copy(image)
    for i in range(0, image.get_width()):
        for j in range(0, image.get_height()):
            pix = image.get_at((i,j))
            if pix == src:
                image.set_at((i,j), dst)
    return copy.copy(image)

def change_all_minus(image, src, dst):
    """
        cambia todos los pixels menos los de color src a color dst
        todo lo que sea azul lo pone como rojo
    
    """
    image = copy.copy(image)
    for i in range(0, image.get_width()):
        for j in range(0, image.get_height()):
            pix = image.get_at((i,j))
            if pix != src:
                image.set_at((i,j), dst)
            if pix == (0,0,255,255):
                image.set_at((i,j), (255,0,0,255))
    return copy.copy(image)

def color_parecido(color1, color2):
    """
    devuelve true si los dos colores se parecen
    """
    vista = 50
    if color2[0] <= color1[0]+vista and color2[0] >= color1[0]-vista and \
    color2[1] <= color1[1]+vista and color2[1] >= color1[1]-vista and \
    color2[2] <= color1[2]+vista and color2[2] >= color1[2]-vista:
        return True
    else: return None
