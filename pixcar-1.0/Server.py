import socket
import threading
import pdb

"""
Servidor para pixcar

el primero que se conecta es el Master de la partida:
    Se le pide el nombre del circuito 500: y el numero de jugadores 501:
    El master esta incluido en este numero de jugadores
Se espera hasta que se conecten todos los jugadores especificados por el master:
    Cuando un jugador se conecta se envia el circuito 201:
    y el numero de jugadores 202:
Se pide a cada jugador su nick, y se comienza la partida

212 para finalizar la conexion

si se desconecta un cliente de forma inesperada se manda el mensaje
213:nick:LOG_OUT a los demas clientes, para que borren el coche indicado

#mensajes del cliente
250 para indicar que esta listo
251 para indicar que se ha dado una vuelta
252 para indicar que se ha completado el circuito

#mensajes para el cliente
600 conexion finalizada con exito
"""

class ControlCliente(threading.Thread):
    def __init__(self, server, index, nick):
        self.server = server
        self.index = index
        self.nick = nick
        self.finish = None
        threading.Thread.__init__(self)
    def run(self):
        resp = self.server.sock[self.index].recv(1024)
        while resp[0:3] != "212":
            try:
                if resp.find("\r\n")>0:
                    if resp[0]=="#":
                        self.server.send_all_minus(str(self.index)+","+resp[1:resp[1:].find("\r\n")+3], self.index)
                        resp = resp[resp.find("\r\n")+2:]
                        if resp != "":
                            continue
                    elif resp[0:3] == "251":
                        self.server.lap_update(self.index)
                        resp = resp[resp.find("\r\n")+2:]
                        if resp != "":
                            continue
                    elif resp[0:3] == "252" and not self.finish:
                        self.server.winner(self.index, self.nick)
                        self.finish = True
                        resp = resp[resp.find("\r\n")+2:]
                        if resp != "":
                            continue

                #TODO separar cadenas recibidas
                resp += self.server.sock[self.index].recv(1024)

            except:
                print str(self.nick[0:-2])+" : se ha desconectado inesperadamente"
                break
        #self.server.send_to("600: hasta luego\r\n", self.index)
        self.server.send_all_minus("213:"+str(self.index)+":LOG_OUT\r\n", self.index)
        self.server.remove(self.index)

class BroadCast(threading.Thread):
    def __init__(self, server):
        self.server = server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
    def run(self):
        self.s.bind(("",8080))
        while True:
            buf, addr = self.s.recvfrom(1024)
            self.s.sendto("PixCar server\r\n", addr)

        
class Server:
    #tengo que pasar un parametro para controlar si se crea en el cliente, que no se vuelva
    #a llamar
    def __init__(self, puerto = 12345, parametro=None):
        """
        abre un puerto en la maquina local, y espera cn conexiones
        """
        self.parametro = parametro
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ss.bind(("",puerto))
        except:
            puerto = puerto + 1
            print "error al conectar en localhost, probando con puerto 12346"
            try:
                self.ss.bind(("",puerto))
            except:
                return None
        self.ss.listen(10)
        self.cn = 0 #numero de jugadores
        self.sock = {} #cada jugador escribira en un socket
        self.addr = {} #direccion de cada jugador
        self.ready = []
        self.laps = []
        self.winners = []
        self.players = []
        self.max2 = 0
        self.first = 0
        BroadCast(self).start()
        self.esperandoMaster()

    def esperandoMaster(self):
        #esperamos al Master
        self.cn = 0 #numero de jugadores
        self.sock = {} #cada jugador escribira en un socket
        self.addr = {} #direccion de cada jugador
        self.ready = []
        self.laps = []
        self.winners = []
        self.players = []
        self.max2 = 0

        print "Esperando al Master"
        self.master, self.master_addr = self.ss.accept()
        self.master.send("500: Master conectado, nombre del circuito\r\n")
        print "Master conectado", self.master_addr
        print "Esperando circuito"
        #recivimos parametros de la partida
        self.circuit = self.master.recv(1024)
        self.master.send("501: circuit ok\r\n")
        print "circuito ok:", self.circuit
        print "Esperando numero de jugadores"
        self.cn = int(self.master.recv(1024))
        self.master.send("501: numero de jugadores ok\r\n")
        print "numero de jugadores ok:", self.cn
        #esperamos a que todos se conecten
        self.conecta()
        
    def conecta(self):
        self.sock[0] = self.master
        self.addr[0] = self.master_addr
        for i in range(1, self.cn):
            print "Esperando "+str(self.cn - i)+" jugadores"
            self.sock[i], self.addr[i] = self.ss.accept()
            self.sock[i].send("100: conexion establecida\r\n")
            self.sock[i].recv(1024) #recibimos la confirmacion del cliente para empezar a mandar
            self.sock[i].send("101: "+self.circuit+"\r\n")
            self.sock[i].send("102: "+str(self.cn)+"\r\n")
            self.sock[i].recv(1024) #esperamos a que lea el circuito y los jugadores

        print self.cn, "conexiones"
        #peticion de datos de los clientes
        #tengo que crear cn objetos de la clase cliente
        #con los datos de cada jugador
        jugadores = ""
        for i in self.sock.keys():
            self.sock[i].send("110: todos conectados, quien eres\r\n")
            resp = self.sock[i].recv(1024)
            print resp, "Conectado"
            self.players.append(resp[0:resp.find(";")])
            jugadores = jugadores + ":"+resp[0:-2]
        self.send_all(jugadores+":\r\n")

        for i in self.sock.keys():
            resp = self.sock[i].recv(1024)
            print self.players[i], "Listo"
            self.add_player_ready(i)

        for i in self.sock.keys():
            ControlCliente(self, i, self.players[i]).start()

        #self.send_all("READY!\r\n")

    def close_all(self):
        """
        cierra todas las conexiones
        """
        for i in self.sock.keys():
            self.sock[i].send("112: adios\r\n")
            self.sock[i].close()
            self.sock.pop(i)
        self.sock = 0
        self.addr = 0
        self.cn = 0
        self.esperandoMaster()

    def send_all_minus(self, str, index):
        """
        manda la cadena str a todos los clientes conectados menos al de indice index
        """
        for i in self.sock.keys():
            if i != index:
                try:
                    self.sock[i].send(str)
                except:
                    self.remove(i)

    def send_to(self, str, index):
        """
        manda la cadena str al cliente index solamente
        """
        self.sock[index].send(str)
    
    def send_all(self, str):
        """
        manda la cadena str a todos los clientes conectados
        """
        for i in self.sock.keys():
            self.sock[i].send(str)
    
    def remove(self, index):
        """
        borra un socket de conexion con clave index
        """
        self.cn = self.cn - 1
        self.sock[index].close()
        self.sock.pop(index)
        if self.cn == 0 and self.parametro:
            self.esperandoMaster()

    def add_player_ready(self, index):
        """
        anade el player index a los que estan listos para empezar
        """
        self.ready.append(index)
        if(len(self.ready) >= self.cn):
            self.send_all("READY!\r\n")
            print "READY enviado"
            for i in self.ready:
                self.laps.append(0)

    def lap_update(self, index):
        self.laps[index] += 1
        self.first = self.players[self.max()]
        self.send_all("msg:Primero "+self.first+"\r\n")
        print "Primero "+self.first

    def max(self):
        for i in self.laps:
            if i > self.laps[self.max2]:
                self.max2 = self.laps.index(i)
        return self.max2

    def winner(self, index, nick):
        self.winners.append(index)
        if (len(self.winners) == self.cn):
            for i in self.winners:
                self.send_all("610:"+self.players[i]+"\r\n")
            self.send_all("600: hasta luego\r\n")
            print "final de la carrera:"
            print self.winners

if __name__ == '__main__':
    ss = Server()
