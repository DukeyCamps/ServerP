import socket
import time






server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", 44444))
message = bytes(str(get_ip()), 'utf-8')
for x in range(100):
    try:
        server.sendto(message, ('<broadcast>', 37010))
        print("message sent!")
        time.sleep(1)
    except:
        print('fuck')
