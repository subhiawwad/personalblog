import copy
import pygame
import socket
import sys
from pygame.locals import *
import utils
import Loading
from Car import *
from Crono import *
from Circuit import *
from textos import *
from Server import *

class loading(threading.Thread):
    def __init__(self,screen):
        self.font = pygame.font.Font(None, 60)
        self.screen = screen
        self.running = True
        self.loading = idioma.lang.loading
        self.loadimg = Loading.Loading(self.screen)
        threading.Thread.__init__(self)
    def run(self):
        points = 0
        index = 0
        while self.running:
            pygame.time.Clock().tick(40)
            if index % 10 == 0:
                points +=1
                points %= 4
                
                points2 = "   "
                if points == 1:
                    points2 = ".  "
                elif points == 2:
                    points2 = ".. "
                elif points == 3:
                    points2 = "..."
                    
            self.text = self.font.render(self.loading+points2, 1, (240,100,0))
            self.screen.fill((255,255,255))
            x,y = self.screen.get_rect().center
            x-= self.text.get_width() / 2
            y += self.loadimg.image.get_height() / 2
            self.screen.blit(self.text, (x,y))
            self.loadimg.update()
            self.screen.blit(self.loadimg.image, self.loadimg.rect)
            
            pygame.display.flip()
            index += 1

class Menu:
    """clase que gestiona y muestra el menu"""

    def __init__(self):
        """constructor"""

        self.laps = 0
        self.car = 'kart'
        self.car_color = (255,0,0,255)
        self.circuit = 'pixjuegos.txt'
        self.left = 0
        self.right = 0
        self.ok = 0
        self.up = 0
        self.down = 0
        self.opcion = 0
        self.numop = 5
        self.color = (255,0,0)
        self.textcolor = (255,255,255)
        self.textcolorsel = (0,250,0)
        self.screen = pygame.display.get_surface()
        self.surf, self.rect = utils.load_image('menu.png')
        self.orig = copy.copy(self.surf)
        self.surf.convert()
        self.text()
        self.controles = (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a)
        self.macli = ""
        self.n = 0
        
        self.s = None
        self.nick=""
        self.netColor = 1
            
    def update(self, event):
        """gestion de eventos"""
        pygame.key.set_repeat(200, 50)

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            return 0
        if event.type == KEYDOWN and event.key == K_UP:
            self.opcion = (self.opcion - 1) % self.numop
        if event.type == KEYDOWN and event.key == K_DOWN:
            self.opcion = (self.opcion + 1) % self.numop
        if event.type == KEYDOWN and event.key == K_RETURN:
            if self.opciones[self.opcion] == idioma.lang.play:
                if self.select_car() == 0:
                    if self.select_circuit():
                        return 1
            if self.opciones[self.opcion] == idioma.lang.multiplayer:
                self.macli = self.select_macli()
                if self.macli == idioma.lang.client:
                    self.macli_menu()
                elif self.macli == idioma.lang.server:
                    self.master_menu()
                else:
                    self.client_menu()

                return 3
            elif self.opciones[self.opcion] == idioma.lang.credits:
                self.credits()
                self.opcion = 0
            elif self.opciones[self.opcion] == idioma.lang.options:
                self.menu_opciones()
            elif self.opciones[self.opcion] == idioma.lang.hof:
                self.Show_Hof()
            elif self.opciones[self.opcion] == idioma.lang.quit:
                return 2

        #se muestran las opciones sobre self.surf
        self.surf = copy.copy(self.orig)
        font = pygame.font.Font(None, 36)
        i = 0
        for opt in self.opciones:
            color = self.textcolor
            if self.opcion == i:
                color = self.textcolorsel
            text = font.render(opt, 1, color)
            textpos = (50, (i+4) * 40)
            self.surf.blit(text, textpos)
            i += 1


    def text(self):
        """opciones del menu principal"""

        self.opciones = (idioma.lang.play, idioma.lang.multiplayer,idioma.lang.options, idioma.lang.hof, idioma.lang.credits, idioma.lang.quit)
        self.numop = len(self.opciones)

    def load(self,clock):
        """carga las clases crono, car y circuit, mostrando una pantalla intermedia durante el proceso\
 Se devuelven el objeto car, el color del coche, el circuito cargado y el crono"""

        crono = Crono(clock)
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        font = pygame.font.Font(None, 50)
        
        l = loading(self.screen)
        l.start()

        circuit = Circuit(self.circuit, self.laps)
        car = Car(circuit, circuit.get_init_angle(), crono, self.car, self.select,self.controles)

        return car, self.car_color, circuit, crono, l

    def credits(self):
        """opcion del menu que muestra los creditos"""
        cab = idioma.lang.credit_cab
        prod = ("PiX Juegos",)
        prog = ("danigm",)
        graf = ("danigm",)
        cred = (prod, prog, graf)
        background, background2 = utils.load_image('menu2.png')
        bg = copy.copy(background)
        background = background.convert()
        bg = copy.copy(background)
        font = pygame.font.Font(None, 30)
        fontH = pygame.font.Font(None, 40)
        
        background = copy.copy(bg)

        pos = 150
        h = 0
        for c in cab: #se ponen las cabeceras
            textH = fontH.render(c, 1, (255, 255, 0))
            i,j = fontH.size(c)
            textpos = ((self.screen.get_width() - i)/2, pos)
            background.blit(textH, textpos)
            cred1 = cred[h]
            for t in cred1: #se ponen los creditos por cada cabecera
                text = font.render(t, 1, (0, 250, 0))
                i,j = font.size(t)
                pos += 30
                textpos = ((self.screen.get_width() - i)/2, pos)
                background.blit(text, textpos)
            pos += 50
            h += 1
                    
            
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

        event = pygame.event.wait()
        while not (event.type == KEYDOWN and event.key == event.key == K_ESCAPE):
            event = pygame.event.wait()

    def menu_opciones(self):
        '''son las opciones disponibles en el menu, se llama a las diferentes funciones'''
        opciones = (idioma.lang.select_car, idioma.lang.language, idioma.lang.toggle_fs, idioma.lang.opt_controls)
        select = self.menu_opt(opciones, idioma.lang.options_h)
        if select == idioma.lang.select_car:
            self.select_car()
        elif select == idioma.lang.language:
            self.select_language()
        elif select == idioma.lang.toggle_fs:
            pygame.display.toggle_fullscreen()
        elif select == idioma.lang.opt_controls:
            self.controles = self.controls()

    def controls(self):
        """se muestran uno a uno los controles y se capturan las teclas"""

        cab = idioma.lang.controls
        controles = []
        
        background, background2 = utils.load_image('menu2.png')
        background = background.convert()
        bg = copy.copy(background)
        font = pygame.font.Font(None, 70)
        fontH = pygame.font.Font(None, 40)
        
        for texto in cab: #se muestran los controles uno a uno
            textH = fontH.render(texto, 1, (255, 255, 0))
            i,j = fontH.size(texto)
            textposH = ((self.screen.get_width() - i)/2, 150)
            background = copy.copy(bg)
            background.blit(textH, textposH)
            self.screen.blit(background, (0, 0))
            pygame.display.flip()
            event = pygame.event.wait() #se espera la pulsacion
            while not event.type == KEYDOWN:
                event = pygame.event.wait()
            controles.append(event.key) #se asigna la tecla pulsada

        return controles


    def select_language(self):
        '''funcion para elegir idioma'''

        opciones = ('es', 'en')
        select = self.menu_opt(opciones, idioma.lang.language)
        idioma.set_language(select)
        self.text()

    def select_circuit(self):
        '''se cargan los circuitos disponibles del fichero circuit.txt'''

        opciones = []
        fullname = os.path.join('data', 'circuit.txt')
        file = open (fullname, 'r')
        for line in file.readlines():
            opciones.append(line[0:-1])
        file.close()
        select = self.menu_opt_circuit(opciones, idioma.lang.select_circuit)
        if select == 0:
            return 0
        else:
            self.circuit =  select + '.txt'
            return 1
        
    def select_car(self, car=None):
        '''se cargan los coches disponibles del fichero car.txt'''

        opciones = []
        fullname = os.path.join('data','car','car.txt')
        file = open (fullname, 'r')
        for line in file.readlines():
            opciones.append(line[0:-1])
        file.close()
        select = self.menu_opt_car(opciones, idioma.lang.select_car, car)
        if select:
            self.car = select
        else: return 1
        return 0

    
    def menu_opt(self, opciones, titulo):
        '''recibe un vector de opciones y devuelve la opcion seleccionada'''

        pygame.key.set_repeat(200, 50)
        self.opcion = 0
        while 1:
            self.surf = copy.copy(self.orig)
            font = pygame.font.Font(None, 40)
            i = 0
            text = font.render(titulo, 1, (255,255,0))
            textpos = (50, (i+4) * 40)
            self.surf.blit(text, textpos)
            i += 1
            font = pygame.font.Font(None, 36)
            for opt in opciones:
                color = self.textcolor
                if self.opcion == i-1:
                    color = self.textcolorsel
                text = font.render(str(opt), 1, color)
                textpos = (50, (i+4) * 40)
                self.surf.blit(text, textpos)
                i += 1
            self.screen.blit(self.surf, (0, 0))
            pygame.display.flip()
            
            event = pygame.event.wait()
            if event.type == KEYUP and event.key == K_ESCAPE:
                self.opcion = 0
                return 0
            if event.type == KEYDOWN and event.key == K_UP:
                self.opcion = (self.opcion - 1) % len(opciones)
            if event.type == KEYDOWN and event.key == K_DOWN:
                self.opcion = (self.opcion + 1) % len(opciones)
            if event.type == KEYDOWN and event.key == K_RETURN:
                ret = self.opcion
                self.opcion = 0
                return opciones[ret]



    def menu_opt_car(self, opciones, titulo,carx=None):
        '''muestra el coche y puedes seleccionar el color'''

        pygame.key.set_repeat(200, 50)
        self.select = 0
        self.opcion = 0
        #car_color = [(255,0,0,255),(0,255,0,255),(0,0,100,255),(255,255,0,255),(0,255,255,255),(0,0,0,255),\
#(160, 90, 190, 255), (230, 230, 230, 255), (255, 150, 0, 255), (67, 171, 0, 255), (14, 150,0, 255)]
        if carx != None:
            self.opcion = opciones.index(carx)
        conf = open(os.path.join('data','car',opciones[self.opcion],'conf.txt'))
        for line in conf:
            if(line[0:3] == "num"):
                num = int(line[4:-1])
        conf.close()
        fullpath = os.path.join('car', opciones[self.opcion], opciones[self.opcion]+str(self.select)+'.png')
        preview, preview_rect = utils.load_image(fullpath, -1)
        preview.convert()
        preview2 = copy.copy(preview)
        angulo = 0
        c = 0
        
        while 1:
            for event in pygame.event.get():
                if event.type == KEYUP and event.key == K_ESCAPE:
                    self.opcion = 0
                    return 0
        
                if event.type == KEYDOWN and event.key == K_UP and carx == None:
                    self.select = 0
                    self.opcion = (self.opcion - 1) % len(opciones)
                    #cargando preview
                    conf = open(os.path.join('data','car',opciones[self.opcion],'conf.txt'))
                    for line in conf:
                        if(line[0:3] == "num"):
                            num = int(line[4:-1])
                    conf.close()
                    fullpath = os.path.join('car', opciones[self.opcion], opciones[self.opcion]+str(self.select)+'.png')
                    preview, preview_rect = utils.load_image(fullpath, -1)
                    preview.convert()
                    preview2 = copy.copy(preview)

                if event.type == KEYDOWN and event.key == K_DOWN and carx == None:
                    self.select = 0
                    self.opcion = (self.opcion + 1) % len(opciones)
                    #cargando preview
                    conf = open(os.path.join('data','car',opciones[self.opcion],'conf.txt'))
                    for line in conf:
                        if(line[0:3] == "num"):
                            num = int(line[4:-1])
                    conf.close()

                    fullpath = os.path.join('car', opciones[self.opcion], opciones[self.opcion]+str(self.select)+'.png')
                    preview, preview_rect = utils.load_image(fullpath, -1)
                    preview.convert()
                    preview2 = copy.copy(preview)

                if event.type == KEYDOWN and event.key == K_RETURN:
                    return opciones[self.opcion]
                
                #pulsando derecha se cambia el color
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    self.select = (self.select+1) % num
                    fullpath = os.path.join('car', opciones[self.opcion], opciones[self.opcion]+str(self.select)+'.png')
                    preview, preview_rect = utils.load_image(fullpath, -1)
                    preview.convert()
                    preview2 = copy.copy(preview)

                #pulsando izquierda tambien
                if event.type == KEYDOWN and event.key == K_LEFT:
                    self.select = (self.select -1) % num
                    fullpath = os.path.join('car', opciones[self.opcion], opciones[self.opcion]+str(self.select)+'.png')
                    preview, preview_rect = utils.load_image(fullpath, -1)
                    preview.convert()
                    preview2 = copy.copy(preview)
                    
            #fin del for de eventos         

            #pintando todo en el menu
            self.surf = copy.copy(self.orig)
            font = pygame.font.Font(None, 40)
            i = 0
            text = font.render(titulo, 1, (255,255,0))
            textpos = (50, (i+4) * 40)
            self.surf.blit(text, textpos)
            i += 1
            font = pygame.font.Font(None, 36)
            for opt in opciones:
                color = self.textcolor
                if self.opcion == i-1:
                    color = self.textcolorsel
                text = font.render('< ' + opt + ' >', 1, color)
                textpos = (50, (i+4) * 40)
                self.surf.blit(text, textpos)
                i += 1
            
            self.screen.blit(self.surf, (0, 0))

            #spin la preview#
            center = preview_rect.center
            angulo = angulo + 4
            if angulo >= 360:
                angulo = 0
            preview = pygame.transform.rotate(preview2, angulo)
            pos = (350 - preview.get_width()/2, 250 - preview.get_height()/2)
            #spin#

            self.screen.blit(preview, pos)
            pygame.display.flip()
            pygame.time.wait(50)

        #fin del while
        
        
    def menu_opt_circuit(self, opciones, titulo):
        '''muestra el circuito y puedes seleccionar el numero de vueltas'''

        pygame.key.set_repeat(200, 50)

        self.opcion = 0
        fullpath = os.path.join('circuit', opciones[self.opcion]+'-prev.png')
        preview, preview_rect = utils.load_image(fullpath, (0,0,0))
        #preview = pygame.transform.scale(preview, (100,100))
        preview.convert()
        angulo = 0
        c = 0

        font = pygame.font.Font(None, 40)
        lfont = pygame.font.Font(None, 30)
        ltext = lfont.render("laps:"+ str(self.laps), 1, (0,255,0,255))

        
        while 1:
            for event in pygame.event.get():
                if event.type == KEYUP and event.key == K_ESCAPE:
                    self.opcion = 0
                    return 0
        
                if event.type == KEYDOWN and event.key == K_UP:
                    self.opcion = (self.opcion - 1) % len(opciones)
                    self.laps = 0
                    #cargando preview
                    fullpath = os.path.join('circuit', opciones[self.opcion]+'-prev.png')
                    preview, preview_rect = utils.load_image(fullpath, (0,0,0))
                    #preview = pygame.transform.scale(preview, (100,100))
                    preview.convert()
                    
                    preview2 = copy.copy(preview)

                if event.type == KEYDOWN and event.key == K_DOWN:
                    self.opcion = (self.opcion + 1) % len(opciones)
                    self.laps = 0
                    #cargando preview
                    fullpath = os.path.join('circuit', opciones[self.opcion]+'-prev.png')
                    preview, preview_rect = utils.load_image(fullpath, (0,0,0))
                    #preview = pygame.transform.scale(preview, (100,100))
                    preview.convert()
                    

                #pulsando derecha se incrementan las vueltas
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    self.laps += 1
                        #pulsando izquierda se decrementan
                if event.type == KEYDOWN and event.key == K_LEFT:
                    self.left = 1
                    if self.laps > 0:
                        self.laps -= 1

                if event.type == KEYDOWN and event.key == K_RETURN:
                    return opciones[self.opcion]

            #fin del for de eventos         

            #pintando todo en el menu
            self.surf = copy.copy(self.orig)
            i = 0
            text = font.render(titulo, 1, (255,255,0))
            textpos = (50, (i+4) * 40)
            self.surf.blit(text, textpos)
            i += 1
            font = pygame.font.Font(None, 36)
            for opt in opciones:
                color = self.textcolor
                if self.opcion == i-1:
                    color = self.textcolorsel
                text = font.render('< ' + opt + ' >', 1, color)
                textpos = (50, (i+4) * 40)
                self.surf.blit(text, textpos)
                i += 1
            
            self.screen.blit(self.surf, (0, 0))

            #spin la preview#
            center = preview_rect.center
            pos = (350 - preview.get_width()/2, 250 - preview.get_height()/2)

            self.screen.blit(preview, pos)
            ltext = lfont.render("laps:"+ str(self.laps), 1, (0,255,0,255))

            self.screen.blit(ltext, pos)
            pygame.display.flip()
            pygame.time.wait(50)

        #fin del while

    def Hof(self, car, circuit, record):
        """pide el nombre para guardar el record"""
        
            #se cargan del fichero todos los records para saber si se ha superado.
        fullname = os.path.join('data','hof.txt')
    
        file = open(fullname)
        lock = 0
        rec = [] #lista auxiliar para poner los tiempos dentro de cada circuito ordenados
        for line in file.readlines():
            if line[0:3] == 'cir':
                if lock:
                    lock = 0
                if line[4:-1] == circuit:
                    lock = 1
            elif line[0:3] == 'new' and lock:
                #nuevo record
                time = line[4:12]
                rec.append(time)
        file.close()

        escribir = 0
        if len(rec) < 10:
            escribir = 1
        else:
            for i in rec:
                if record < i:
                    escribir = 1

        if not escribir:
            return 0
        
        pygame.key.set_repeat(200, 50)
        cab = idioma.lang.hof
        background, background2 = utils.load_image('menu2.png')
        background = background.convert()
        bg = copy.copy(background)
        font = pygame.font.Font(None, 70)
        fontH = pygame.font.Font(None, 40)
        
        texto = 'Record: %(record)s. %(head)s:' %{'record': record, 'head': idioma.lang.name}
        
        textH = fontH.render(texto, 1, (255, 255, 0))
        i,j = fontH.size(texto)
        textposH = ((self.screen.get_width() - i)/2, 150)

        string = ""
        while 1:
            background = copy.copy(bg)
            text = font.render(string, 1, (0, 250, 0))
            i,j = fontH.size(texto)
            textpos = ((self.screen.get_width()-i)/2, (self.screen.get_height()-j)/2)
            
            background.blit(textH, textposH)
            background.blit(text, textpos)
            
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

            keys = pygame.event.wait()
            if keys.type == KEYDOWN and keys.key == K_ESCAPE:
                return 0
            elif keys.type == KEYDOWN and keys.key == K_BACKSPACE:
                string = string[0:-1]
            elif keys.type == KEYDOWN and keys.key == K_RETURN:
                self.writeHof(circuit, string, car, record)
                return 0
            elif keys.type == KEYDOWN and keys.key == K_SPACE:
                string = string + ' '
            elif keys.type == KEYDOWN:
                key = keys.key
                string = string + keys.unicode
                    
            
    def writeHof(self, circuit, name, car, time):
        """escribe el record en el fichero de record hof.txt"""

        fullname = os.path.join('data','hof.txt')
        fullname2 = os.path.join('data','hof2.txt')
        file = open(fullname, 'r')
        file2 = open(fullname2, 'w')

        puesto = 0
        line = file.readline()
        while line:
            if line[0:3] == 'cir':
                file2.write(line)
                if line[4:-1] == circuit:
                    file2.write('new:%-20s %-15s %-25s\n' %(time, car, name))
                    puesto = 1
                    
            elif line[0:3] == 'end' and puesto == 0:
                file2.write(str('cir:' + circuit + '\n'))
                file2.write('new:%-20s %-15s %-25s\n' %(time, car, name))
                file2.write(line)
                puesto = 1

            else:
                file2.write(line)

            line = file.readline()

        file.close()
        file2.close()
        os.remove(fullname)
        os.rename(fullname2, fullname)

    ###muestra los record del fichero hof.txt###
    def Show_Hof(self, circuit_name = None, index = None):
        """muestra los records por circuito"""

        fullname = os.path.join('data','hof.txt')
        background, background2 = utils.load_image('menu2.png')
        background = background.convert()
        bg = copy.copy(background)
        

        #se carga del fichero en la lista cab
        #antes de cada nombre de circuito hay un None y despues todos los records
    
        file = open(fullname)
        cab = [] #lista con el archivo de tiempos
        rec = [] #lista auxiliar para poner los tiempos dentro de cada circuito ordenados
        for line in file.readlines():
            if line[0:3] == 'cir':
                #nuevo circuito
                rec.sort()
                for i in rec:
                    cab.append(i)
                rec = []
                cab.append(None)
                cab.append(line[4:-1])
            elif line[0:3] == 'new':
                #nuevo record
                time = line[4:12]
                rec.append(line[4:-1])
            elif line[0:3] == 'end':
                #fin de fichero
                rec.sort()
                for i in rec:
                    cab.append(i)

                cab.append(None)
                
        file.close()

        circuit = 1

        if circuit_name != None:
            while circuit_name != cab[circuit]:
                circuit = self.nextcircuit(cab, circuit)

        #se pone el nombre del circuito
        background = self.puttext(bg, cab, circuit, index)

        while 1:
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

            #izquierda y derecha cambia de circuito
            event = pygame.event.wait()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                break
            elif event.type == KEYDOWN and event.key == K_LEFT:
                circuit = self.prevcircuit(cab, circuit)
                background = self.puttext(bg, cab, circuit, index)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                circuit = self.nextcircuit(cab, circuit)
                background = self.puttext(bg, cab, circuit, index)

    def nextcircuit(self, cab, circuit):
        """devuelve el indice del circuito segun el formato de cab"""

        if cab == [None]:
            return circuit
        while circuit < len(cab):
            circuit += 1
            if circuit+1 == len(cab):
                return self.nextcircuit(cab, -1)
            if cab[circuit] == None:
                return circuit+1
 
    def prevcircuit(self, cab, circuit):
        """devuelve el indice del circuito segun el formato de cab"""
        
        if cab == [None]:
            return circuit
        circuit -= 1
        while circuit > 0:
            circuit -= 1
            if cab[circuit] == None:
                return circuit+1
        if circuit <= 0:
            return self.prevcircuit(cab, len(cab)-1)
            
    def puttext(self, bg, cab, circuit, index):
        """funcion auxiliar para poner el texto en el HOF"""
        """devuelve una superficie con el texto de los records"""

        background = copy.copy(bg)
        font = pygame.font.Font(None, 30)
        fontH = pygame.font.Font(None, 40)

        #se pone la cabecera
        texto = idioma.lang.hof
        textH = fontH.render(texto, 1, (255, 255, 0))
        i,j = fontH.size(texto)
        textpos = ((self.screen.get_width() - i)/2, 150)
        background.blit(textH, textpos)

        color = (0, 250, 0)
        color2 = (250, 250, 0)

        if cab == [None]:
            return background

        c = circuit
        textH = fontH.render('< ' + cab[c] + ' >', 1, (255, 255, 0))
        i,j = fontH.size('< '+cab[c]+' >')
        textpos = ((self.screen.get_width() - i)/2, 180)
        background.blit(textH, textpos)

        pos = 180
        t = c + 1
        l,j = font.size(cab[t])
        d = 1
        while cab[t] != None and d < 11: #se muestran todos los records
            record = cab[t][0:8]
            if index == record:
                text = font.render(str(d) + '. ' + cab[t], 1, color2)
            else:
                text = font.render(str(d) + '. ' + cab[t], 1, color)
            i,j = font.size(str(d) + '. ' + cab[t])
            pos += 30
            textpos = ((self.screen.get_width() - l)/2, pos)
            background.blit(text, textpos)
            t += 1
            d += 1
        return background
    
    def get_car(self):
        return self.car

    def select_macli(self):
        '''funcion para elegir si eres master o cliente'''

        opciones = (idioma.lang.client,idioma.lang.server)
        select = self.menu_opt(opciones, idioma.lang.master_or_client)
        return select

    def master_menu(self):
        Servidor().start()
        if self.select_car() == 0:
            self.select_circuit()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.n = int(self.menu_opt(range(1,10), idioma.lang.number_of_players))
        self.nick = self.recibir_teclado(idioma.lang.nick)
        self.nick = self.nick+";"+str(self.select)
    
        try:
            self.s.connect(("", 12345))
            resp = self.s.recv(1024)
        except Exception, inst:
            print "imposible conectar con el servidor *"
            print inst
            sys.exit(0)

        self.macli = "master"

    def macli_menu(self):
        addr = 0
        dgram = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dgram.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        dgram.settimeout(5)
        try:
            dgram.sendto("where are you?\r\n",('<broadcast>',8080))
            buf, addr = dgram.recvfrom(1024)
        except:
            print "no encuentro el servidor, pon la ip"
        dgram.close()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if addr == 0:
            servidor = self.recibir_teclado(idioma.lang.server_ip)
        else: servidor = addr[0]
        try:
            self.s.connect((servidor, 12345))
            resp = self.s.recv(1024)
            if resp[0:4] == "500:":
                self.macli = "master"
                self.master_menu2()
            else:
                self.s.send("200: cliente Ok\r\n")
                self.client_menu()
        except Exception, inst:
            print "imposible conectar con el servidor **"
            print inst
            sys.exit(0)

    def master_menu2(self):
        if self.select_car() == 0:
            self.select_circuit()
        
        self.n = int(self.recibir_teclado2(idioma.lang.number_of_players))
        self.nick = self.recibir_teclado(idioma.lang.nick)
        self.nick = self.nick+";"+str(self.select)
        
    def client_menu(self):
        n = 0
        try:
            resp = self.recibir(self.s,2)
            self.s.send("200: recibido OK\r\n")
            self.circuit = resp[0][5:resp[0][5:].find(";")+5]+".txt" #circuito;vueltas:coche
            self.laps = int(resp[0][resp[0][5:].find(";")+6:resp[0][5:].find(":")+5])
            self.car = resp[0][resp[0][5:].find(":")+6:]
            self.n = int(resp[1][5:])
        except Exception, inst:
            print "imposible conectar con el servidor ***"
            print inst
            sys.exit(0)
        self.select_car(self.car)
        self.nick = self.recibir_teclado(idioma.lang.nick)
        self.nick = self.nick+";"+str(self.select)

    def leer_datos(self):
        if self.macli == "master":
            return self.s, self.n, self.nick, self.macli, 0, self.car
        else:
            return self.s, self.n, self.nick, self.macli, self.circuit, self.car


    def recibir(self,sock, num):
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

    def recibir_teclado2(self, texto):
        """y un numero, que se incrementa con los cursores"""

        pygame.key.set_repeat(200, 50)
        background, background2 = utils.load_image('menu2.png')
        background = background.convert()
        bg = copy.copy(background)
        font = pygame.font.Font(None, 90)
        fontH = pygame.font.Font(None, 40)
        
        textH = fontH.render(texto, 1, (255, 255, 0))
        i,j = fontH.size(texto)
        textposH = ((self.screen.get_width() - i)/2, 150)

        n = 2
        string = "< "+str(n)+" >"
        while 1:
            string = "< "+str(n)+" >"
            background = copy.copy(bg)
            text = font.render(string, 1, (0, 250, 0))
            i,j = font.size(string)
            textpos = ((self.screen.get_width()-i)/2, (self.screen.get_height()-j)/2)
            
            background.blit(textH, textposH)
            background.blit(text, textpos)
            
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

            keys = pygame.event.wait()
            if keys.type == KEYDOWN and keys.key == K_ESCAPE:
                return 0
            elif keys.type == KEYDOWN and keys.key == K_RETURN:
                return n
            elif keys.type == KEYDOWN and keys.key == K_UP:
                n += 1
            elif keys.type == KEYDOWN and keys.key == K_DOWN:
                if n > 1:
                    n -= 1
            elif keys.type == KEYDOWN and keys.key == K_RIGHT:
                n += 1
            elif keys.type == KEYDOWN and keys.key == K_LEFT:
                if n > 1:
                    n -= 1
        
                    
        return n

    def recibir_teclado(self, texto):
        """muestra el texto, y devuelve lo tecleado como una cadena"""

        pygame.key.set_repeat(200, 50)
        background, background2 = utils.load_image('menu2.png')
        background = background.convert()
        bg = copy.copy(background)
        font = pygame.font.Font(None, 70)
        fontH = pygame.font.Font(None, 40)
        
        textH = fontH.render(texto, 1, (255, 255, 0))
        i,j = fontH.size(texto)
        textposH = ((self.screen.get_width() - i)/2, 150)

        string = ""
        while 1:
            background = copy.copy(bg)
            text = font.render(string, 1, (0, 250, 0))
            i,j = font.size(string)
            textpos = ((self.screen.get_width()-i)/2, (self.screen.get_height()-j)/2)
            
            background.blit(textH, textposH)
            background.blit(text, textpos)
            
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

            keys = pygame.event.wait()
            if keys.type == KEYDOWN and keys.key == K_ESCAPE:
                return 0
            elif keys.type == KEYDOWN and keys.key == K_BACKSPACE:
                string = string[0:-1]
            elif keys.type == KEYDOWN and keys.key == K_RETURN:
                return string
            elif keys.type == KEYDOWN and keys.key == K_SPACE:
                string = string + ' '
            elif keys.type == KEYDOWN:
                key = keys.key
                string = string + keys.unicode
                    
        return string


    
class Servidor(threading.Thread):
    def __init__(self):
        self.ss = None
        threading.Thread.__init__(self)
    def run(self):
        self.ss = Server()


