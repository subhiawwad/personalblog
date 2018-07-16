#!/usr/bin/python

"""
Juego de coches al estilo de micromachines
con vista superior.
"""

#constantes
MENU = 0
JUEGO = 1
PAUSE = 2
NET = 3
sended =""
end = None
calificaciones = []
message = 0

import pdb

import os, sys 
import pygame
import math
import socket
from pygame.locals import *

#importaciones propias
import utils
from Car import *
from Car2 import *
from Crono import *
from Circuit import *
from Menu import *
from Mini import *
from Server import *
from Message import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

music = 0
### clase principal, main ###
def main():

#Inicializando todo
    pygame.init()
    screen = pygame.display.set_mode((800,600), pygame.DOUBLEBUF)
    pygame.display.set_caption('PiXCar')
    image, rect = utils.load_image("car.png",(255,255,255))
    pygame.display.set_icon(image)
    pygame.mouse.set_visible(0)
    
#el menu
    menu = Menu()
#   try:
#       pygame.mixer.init()
#       pygame.mixer.music.load('data/music.mp3')
#       pygame.mixer.music.play(-1, 2)
#       music=1
#   except:
#       music=0
    
    clock = pygame.time.Clock()
    modo = 0

#Bucle principal
#la variable modo indica el modo actual
#modo 0 indica menus, y modo 1 indica en juego, modo 2 indica pause
#para indicar el modo se usan las constantes MENU, JUEGO, PAUSE
    var = 0;
    mini = 0;

    while 1:
        clock.tick(40)
        #print clock.get_fps()
        #pygame.time.wait(1)
        
        if modo == MENU:
            modo, crono, car, circuit, allsprites, mini, sock = mainMenu(menu, screen,clock)
        elif modo == JUEGO:
            modo = modo1(menu, crono, car, circuit, allsprites, screen, mini)
        elif modo == NET:
            end = None
            modo = modo2(menu, crono, car, circuit, allsprites, screen, mini, sock)
        elif modo == PAUSE:
            modo = pause(screen)

        elif modo == QUIT:
            break
    
#Game Over

#modo menus
def mainMenu(menu, screen,clock):
    """modo menus"""
    modo = MENU
    zero4 = (0,0,0,0)
    car, crono, circuit, allsprites = zero4
    #juego en red, lista de otros jugadores
    netCars = []
    #numero de jugadores en red, sin contar yo
    netPlayers = 1
    mini = 0

    #Pintando todo
    screen.blit(menu.surf, (0,0))
    pygame.display.flip()

    #Manejando los enventos de entrada
    event = pygame.event.wait()
    if event.type == QUIT:
        return QUIT, 0,0,0,0,0,0
    elif event.type == KEYDOWN and event.key == K_ESCAPE:
        return QUIT, 0,0,0,0,0,0
    elif event.type == KEYDOWN and event.key == K_f:
        pygame.display.toggle_fullscreen()
                
    opt = menu.update(event)
    if opt == 1:
        modo = JUEGO
        car, car_color, circuit, crono, l = menu.load(clock)
        l.running = False
        carlist = []
        carlist.append(car)

        mini = Mini(circuit, carlist, 1)
        if(music):
            pygame.mixer.music.stop()

        car.set_color_int(1)
        mini.set_color(car.color)

        allsprites = pygame.sprite.OrderedUpdates((circuit))
        for i in carlist:
            allsprites.add(i)

        crono.uptime()

    if opt == 3:
        modo = NET
        global message

        sock, netPlayers, nick, macli, circuito, netCarName = menu.leer_datos()

        car, car_color, circuit, crono, l = menu.load(clock)
        message = Message()


        #si soy master envio al servidor el circuito y el numero de jugadores
        if macli == "master":
            try:
                sock.send(circuit.name+";"+str(circuit.laps)+":"+car.name)
                resp = recibir(sock,1) #confirmacion de circuito
                sock.send(str(netPlayers))
                resp = recibir(sock,2) #confirmacion numero de players y peticion de nombre, esperando a otros jugadores
                sock.send(nick+"\r\n")
                resp = recibir(sock, 1) #todos los nombres de jugadores, indexados
                players,colores, indices = parsear_players(resp[0])
            except Exception, inst:
                print "error en la conexion"
                print inst
                sys.exit(0)

        else:
            try:
                reps = recibir(sock,1) #peticion de nick
                sock.send(nick+"\r\n")
                resp = recibir(sock, 1) #todos los nombres de jugadores, indexados
                players,colores,indices = parsear_players(resp[0])
            except Exception, inst:
                print "error en la conexion"
                print inst
                sys.exit(0)
        
        nick = nick[0:nick.find(";")]

        #con este bucle se inicializan todos los coches de la red
        #la posicion la sabemos segun el orden en el vector de players
        miindex = players.index(nick)
        (x,y) = car.get_pos() #posicion inicial
        for i in players:
            index = players.index(i)
            if index == miindex:
                car.set_name(nick)
                car.set_pos(circuit.ctx[index][0], circuit.ctx[index][1],circuit.get_init_angle())
                car.set_color_int(players.index(i))
                netCars.append(car)
            else:
                car2 = Car2(circuit, circuit.get_init_angle(), crono, netCarName, indices[index])
                car2.set_pos(circuit.ctx[index][0], circuit.ctx[index][1], circuit.get_init_angle())
                car2.set_name(i)
                car2.set_color_int(int(players.index(i)))
                netCars.append(car2)
        carlist = copy.copy(netCars)
        #carlist.append(car)
        car2 = car
        car = carlist #a partir de aqui car contiene la lista de coches.

        mini = Mini(circuit, carlist, netPlayers)
        if(music):
            pygame.mixer.music.stop()

        #car2.set_color(car_color)
        mini.set_color(car2.color)

        allsprites = pygame.sprite.OrderedUpdates((circuit))
        for i in carlist:
            allsprites.add(i)

        sock.send("250: yo estoy listo")
        print "150: yo estoy listo"
        recibir(sock, 1) #espera READY
        
        RecibirServer(sock, car).start()
        l.running = False

        crono.uptime()

        return modo, crono, car, circuit, allsprites, mini, [sock,car2]


    elif opt == 2:
        return QUIT, 0,0,0,0,0,0

    return modo, crono, car, circuit, allsprites, mini, 0

#modo de juego 1
def modo1(menu, crono, car, circuit, allsprites, screen, mini):
    """modo de juego 1"""
    modo = JUEGO

    #Manejando los enventos de entrada
    for event in pygame.event.get():
        if event.type == QUIT:
            return QUIT
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            modo = MENU
            if(music):
                pygame.mixer.music.play(-1, 2)
            car.stop()
        elif event.type == KEYDOWN and event.key == K_p:
            modo = PAUSE
    
        #Eventos del player one
        car.event(event)
        
    #actualizando objetos
    mini.update()
    allsprites.update()
    if crono.update() == 1: #has llegado al final
        min = car.record / 60
        sec = (car.record % 60) / 1
        msec = ((car.record % 60) * 100) % 100
            
        record = '%(min)02d:%(sec)02d:%(msec)02d' %{'min': min, 'sec': sec, 'msec': msec}
        menu.Hof(car.name, circuit.name, record) #escribe el nombre
        menu.Show_Hof(circuit_name = circuit.name, index = record)
        modo = 0
        if(music):
            pygame.mixer.music.play(-1, 2)
        car.stop()
        allsprites.empty()

    #Pintando todo
    allsprites.draw(screen)
    screen.blit(car.text, car.textpos)
    screen.blit(crono.surf, crono.pos)
    screen.blit(mini.preview, mini.pos)
    if(circuit.fg):
        screen.blit(circuit.fg, circuit.rect)
    pygame.display.flip()
    #pygame.time.wait(1)

    return modo


#modo de juego 2, juego en red
def modo2(menu, crono, carlist, circuit, allsprites, screen, mini, sockcar):
    """modo de juego 2"""
    
    global sended
    global calificaciones
    global message
    modo = NET

    if end == True:
        sock.close()
        car.stop()
        allsprites.empty()
        muestra_HoF_net(calificaciones, screen)
        calificaciones = []

        modo = MENU
        return modo


    car = sockcar[1]
    sock = sockcar[0]
    #Manejando los enventos de entrada

    for event in pygame.event.get():
        if event.type == QUIT:
            try:
                sock.send("212: he terminado\r\n")
            except:
                print "ya estoy desconectado"
            sock.close()
            return QUIT
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pdb.set_trace
            modo = MENU
            try:
                sock.send("212: he terminado\r\n")
            except:
                print "ya estoy desconectado"
            sock.close()
            return modo
        #este modo no se si tendra sentido en el juego en red
        elif event.type == KEYDOWN and event.key == K_p:
            modo = PAUSE
    
        #Eventos del player one
        car.event(event)
    
    x,y = car.get_pos()
    tosend = "#"+str(x)+","+str(y)+","+str(car.angle)+"\r\n"
    if tosend != sended:
        try:
            sock.send(tosend)
        except Exception, inst:
            sock.close()
            car.stop()
            allsprites.empty()
            muestra_HoF_net(calificaciones,screen)
            calificaciones = []
            modo = MENU
            return modo
        
        sended = tosend

    
    #actualizando objetos
    mini.update()

    laps = car.lap 
    allsprites.update()
    #ahora comprobamos si hemos dado una vuelta, y en ese caso 
    #se lo contamos al servidor, que lo tendra que saber ,no?
    if(laps < car.lap):
        sock.send("251: vuelta Completada\r\n")

    crono.update()
    
    if car.record != 0: #has llegado al final
        min = car.record / 60
        sec = (car.record % 60) / 1
        msec = ((car.record % 60) * 100) % 100
            
        record = '%(min)02d:%(sec)02d:%(msec)02d' %{'min': min, 'sec': sec, 'msec': msec}
        sock.send("252: winner\r\n")
        car.record = 0
        #menu.Hof(car.name, circuit.name, record) #escribe el nombre
        #menu.Show_Hof(circuit_name = circuit.name, index = record)
    
    #Pintando todo
    allsprites.draw(screen)
    screen.blit(car.text, car.textpos)
    for i in carlist:
        screen.blit(i.text, i.textpos)
    screen.blit(crono.surf, crono.pos)
    screen.blit(message.surf, message.pos)
    screen.blit(mini.preview, mini.pos)
    pygame.display.flip()
    #pygame.time.wait(1)

    return modo

def pause(screen):
    """muestra un mensaje centrado de pausa y espera un evento de teclado"""
    modo = PAUSE

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    font = pygame.font.Font(None, 50)
    text = font.render("PAUSE", 1, (10, 10, 10))
    i,j = font.size("PAUSE")
    textpos = ((screen.get_width() - i)/2, (screen.get_height() - j)/2)
    background.fill((255,255,255))
    background.blit(text, textpos)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    event = pygame.event.wait()
    if event.type == KEYDOWN:
        modo = JUEGO
    return modo

def recibir(sock, num):
    """
    lee del socket el numero de cadenas indicado acabadas por \r\n
    y devuelve un vector con todas
    """
    resp = sock.recv(1024)
    ret = []
    #toda cadena tiene que acabar con \r\n
    while(resp[-2:] != "\r\n" or resp.count('\r\n') < num):
        resp = resp + sock.recv(1024)
    while(resp.find("\r\n") > 0):
        ret.append(resp[0:resp.find("\r\n")])
        resp = resp[resp.find("\r\n")+2:]

    return ret

def parsear_players(str):
    """
    lee una cadean del tipo :nick;carid:dos;carid:tres;carid:
    y devuelve un vector con los nicks y otro con los colores
    """
    ret = []
    colores = []
    indices = []
    nombres = str
    i = 0
    while(nombres != ":"):
        nombres = nombres[1:]
        ret.append(nombres[0:nombres.find(";")])
        colores.append(i)
        indices.append(int(nombres[nombres.find(";")+1:nombres.find(":")]))
        nombres = nombres[nombres.find(':'):]
        i+=1

    return ret, colores, indices



def muestra_HoF_net(vector, screen):
    """muestra la clasificacion"""
    background, background2 = utils.load_image('menu2.png')
    background = background.convert()
    bg = copy.copy(background)
    
    font = pygame.font.Font(None, 40)
    fontH = pygame.font.Font(None, 40)
    
    textH = fontH.render("Clasificacion", 1, (255, 255, 0))
    i,j = fontH.size("Clasificacion")
    textposH = ((screen.get_width() - i)/2, 150)
    background.blit(textH, textposH)

    text_rol = 0
    for player in vector:
        #TODO no me muestra las clasificaciones, pero si el encabezado
        text = font.render(player[0:], 1, (0, 250, 0))
        i,j = font.size(player)
        textpos = ((screen.get_width()-i)/2, 200+(text_rol*50))
        background.blit(text, textpos)
        text_rol+=1


    #se pone el nombre del circuito

    while 1:
        screen.blit(background, (0, 0))
        pygame.display.flip()

        #izquierda y derecha cambia de circuito
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            break

class RecibirServer(threading.Thread):
    def __init__(self, socket, carlist):
        self.sock = socket
        self.carlist = carlist
        self.buf = ""
        threading.Thread.__init__(self)
    def run(self):
        self.buf += self.sock.recv(1024)
        resp = []
        global calificaciones
        global message
        while(self.buf.find("\r\n") > 0):
            resp.append(self.buf[0:self.buf.find("\r\n")])
            self.buf = self.buf[self.buf.find("\r\n")+2:]

        index = 0
        end2 = None
        while resp[0][0:3] != "600":
            if resp[0][0:4] == "213:":
                logout = int(resp[0][4:resp[0][4:].find(":")+4])
                self.logout(logout)
                resp.remove(resp[0])

            for mens in resp:
                if mens[0:4] == "610:":
                    index+=1
                    print str(index)+" -> "+mens[4:]
                    calificaciones.append(str(index)+" -> "+mens[4:])
                    continue

                if mens[0:4] == "msg:":
                    message.put_text(mens[4:])

                if mens[0:4] == "600:":
                    end2 = True
                    break

                else:
                    self.aplicar_cambios(mens)
            
            if end2:
                break
                

            try:
                self.buf += self.sock.recv(1024)
                resp = []
                while(self.buf.find("\r\n") > 0):
                    resp.append(self.buf[0:self.buf.find("\r\n")])
                    self.buf = self.buf[self.buf.find("\r\n")+2:]
            except Exception, inst:
                print "El servidor se ha desconectado inesperadamente"
                print inst
                sys.exit(0)
            
            if(len(resp) == 0):
                break
        print "FUERA!!"
        end = True
        try:
            self.sock.send("212: he terminado\r\n")
        except:
            print "ya estoy desconectado"
            self.sock.close()



    def aplicar_cambios(self, mens):
        """
        parseo el mensaje por comas
        id,posx,posy,angulo
        """
        #esto es para quitar los # que se cuelan al llegar varios mensajes juntos
        if mens.find("#") > 0 :
            m = mens[0:mens.find("#")]

        else: m = mens
        vect = []
        if m.count(',') == 3:
            while(m.find(',') > 0):
                vect.append(m[0:m.find(',')])
                m = m[m.find(',')+1:]
            vect.append(m)
            car = self.carlist[int(vect[0])]
            car.set_pos(int(vect[1]),int(vect[2]),float(vect[3]))
        #esto es para quitar los # que se cuelan al llegar varios mensajes juntos
            if mens.find("#") > 0:
                self.aplicar_cambios(mens[mens.find("#")+1:])
    
    def logout(self, index):
        """
        se carga a un coche
        """
        #TODO
        #cuando alguien se desconecta lo pongo negro,
        #tendria que borrar el coche y poner una imagen de crash
        self.carlist[index].killed = True
        self.carlist[index].kill()
        self.carlist.remove(self.carlist[index])



    

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()

