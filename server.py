import socket
import random
import re
from threading import Thread
import sys
import sqlite3
import time
_PORT_MIN_ = 5600
_PORT_MAX_ = 5605


class Client:
    username = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def findBroadcast(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.bind(("", 12164))

        while True:
            data, addr = client.recvfrom(1024)
            print("Connected.")
            if(len(data) > 5):
                return addr[0]




    def __init__(self, address):
        global username
        self.username = input("Please enter your name: ")
        print ("\033[A                              \033[A")
        print("Welcome, "+str(self.username))



        print("DukiClient started! trying on "+str(address))
        for x in range(_PORT_MIN_, _PORT_MAX_):
            try:
                self.sock.connect((self.findBroadcast(), x))
                break
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
            user_msg = input()
            print ("\033[A                              \033[A")
            self.sock.send(bytes("["+self.username+"]" + user_msg, 'utf-8'))


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
            broadcastThread = Thread(target=self.broadcaster)
            broadcastThread.daemon = True
            broadcastThread.start()

            while True:
                c,a = self.sock.accept()
                cThread = Thread(target= self.handler, args=(c,a))
                cThread.daemon = True
                cThread.start()
                self.connections.append(c)
                print("A" + str(a))
                print("connections: "+str(a[0]) + ':' + str(a[1]), "connected")


    def broadcaster(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        server.settimeout(0.2)
        server.bind(("", 15012))
        message = bytes('join me', 'utf-8')
        while True:
            try:
                server.sendto(message, ('<broadcast>', 12164))
                print("message sent!")
                time.sleep(1)
            except:
                print("Error : Broadcasting")


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
                    connection.send(bytes(sentenced_data , 'utf-8'))


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
