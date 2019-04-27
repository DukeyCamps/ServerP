import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 37010))
while True:
    data, addr = client.recvfrom(1024)
    print(data)
    print("received message: %s"%data)
    print("from: %s"%str(addr))
    if(len(data) > 5):
        break
