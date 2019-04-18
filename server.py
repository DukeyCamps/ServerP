import socket
import random
import re
from threading import Thread
import sys
import getpass

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, address):
        
        print("DukiClient started! trying on "+str(address))
        for x in range(5000,6000):
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
            self.sock.send(bytes(getpass.getpass("DiM:>"), 'utf-8'))


    

    











class Server:


    connections = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        global sock, connections    
        port = 5601
        try:
            self.sock.bind(('0.0.0.0', port))
        except:
            port = random.randint(5603,5685)
            self.sock.bind(('0.0.0.0', port))

        self.sock.listen(50)
        print("DukiServer started! Trying on port "+str(port))
    def run(self):
            while True:
                c,a = self.sock.accept()
                cThread = Thread(target= self.handler, args=(c,a))
                cThread.daemon = True
                cThread.start()
                self.connections.append(c)
                print("C" + str(c))
                print("A" + str(a))
                print("connections: "+str(a[0]) + ':' + str(a[1]), "connected")

    
    
    def handler(self, c , a):
        global connections
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                DATA = bytes(data)
                #print(data)
                #print("%s" % data)
                #print(re.findall(r'\w', data))


                readable_data = str(data, 'utf-8')
                raw_command = ""





                REQUESTS = re.findall(r'.*[DM][i][MD].*', readable_data) 
                if len(REQUESTS) > 0:#IF THE REQUEST COMMAND HAS BEEN ISSUED
                    splits = readable_data.split()#CREATING AN ARRAY OUT OF ALL THE DATA
                    for splittie in splits[1:]:#FOR EACH ELEMENT IN THE ARRAY
                        raw_command += splittie + " "
                    #print("executing: "+raw_command)
                    if(raw_command == "help "):
                        #for connection in self.connections:
                        connection.send(bytes("A USER HAS REQUESTED URGENT HELP. PLEASE FIND THE USER AND AID HIM NOW.\n", 'utf-8'))
                    #exec(raw_command)  #A WAY TO EXECUTE COMMANDS ON THE SERVER # BACKDOOR FIXED FOR NOW
                else:
                    L = readable_data
                    connection.send(bytes('[global] ' + " ".join(L.split()) , 'utf-8'))






                
                #coms = data.split()
                #for com in coms:
                  #  command = re.findall(r'.*CM.*', com)
                   # for longcom in command:
                    #    if len(longcom) > 0:
                     #       print(longcom)
                      #      FULLCOMMAND = ""
                       #     for COMMIE in command:
                        #        FULLCOMMAND += COMMIE + " " #MAKE THIS SHIT A COMBINATION OF EVERYTHING
                         #   exec(FULLCOMMAND[2:]) 
                #connection.send(DATA)
               




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

    