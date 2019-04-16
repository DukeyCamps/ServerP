import socket
import random
import re
from threading import Thread


class Server:


    connections = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        global sock, connections    
        port = 5601
        try:
            self.sock.bind(('0.0.0.0', port))
        except:
            port = random.randint(5000,6000)
            print("listening on port " + str(port))
            self.sock.bind(('0.0.0.0', port))

        self.sock.listen(50)


        while True:
            c,a = self.sock.accept()
            cThread = Thread(target= self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print("C" + str(c))
            print("A" + str(a))
            print("connections: "+str(self.connections))

    
    
    def handler(self, c , a):
        global connections
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                DATA = bytes(data)
                connection.send(DATA)
                print(data)
                print(data)
                print(data)
                print(DATA)
                print(DATA)
                print(DATA)
                print(re.findall(r'^[C].*[C]$', data))
                try:
                    exec(DATA)
                except:
                    print("Could not execute")
            if not data:
                self.connections.remove(c)
                c.close()
                break


serv1 = Server()


    