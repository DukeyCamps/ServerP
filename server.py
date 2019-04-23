import socket
import random
import re
from threading import Thread
import sys
import sqlite3

_PORT_MIN_ = 5600
_PORT_MAX_ = 5605



class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, address):
        
        print("DukiClient started! trying on "+str(address))
        for x in range(_PORT_MIN_, _PORT_MAX_):
            try:
                self.sock.connect((address, x))
            except:
                pass
        inThread = Thread(target=self.sendMSG)
        inThread.daemon = True
        inThread.start()
        
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))


    def sendMSG(self):
        while True:
            self.sock.send(bytes(input(), 'utf-8'))


class Server:
    connections = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        global sock, connections    
        port = 5601
        try:    
            port = random.randint(_PORT_MIN_, _PORT_MAX_)
            self.sock.bind(('0.0.0.0', port))
        except:
            print("Error : Cannot bind port")
        self.sock.listen(50)
        print("DukiServer started! Trying on port "+str(port))


    def run(self):
            while True:
                c,a = self.sock.accept()
                cThread = Thread(target= self.handler, args=(c,a))
                cThread.daemon = True
                cThread.start()
                self.connections.append(c)
                print("A" + str(a))
                print("connections: "+str(a[0]) + ':' + str(a[1]), "connected")

    
    def handler(self, c , a):
        global connections
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                DATA = bytes(data)
            


                readable_data = str(data, 'utf-8')
                raw_command = ""
                REQUESTS = re.findall(r'.*[DM][i][MD].*', readable_data) 
                if len(REQUESTS) > 0:
                    splits = readable_data.split()
                    for splittie in splits[1:]:
                        raw_command += splittie + " "
                    if(raw_command == "help "):
                        connection.send(bytes("broadcast help\n", 'utf-8'))
                else:
                    sentenced_data = readable_data
                    sentenced_data = " ".join(sentenced_data.split())
                    connection.send(bytes('[global] ' + sentenced_data , 'utf-8'))


            if not data:
                self.connections.remove(c)
                c.close()
                print("connections: "+str(a[0]) + ':' + str(a[1]), "disconnected")
                break


if(len(sys.argv) > 1):
    Dukiclient = Client(sys.argv[1])
    Dukiclient.run()
else:   
    DukiServer = Server()
    DukiServer.run()