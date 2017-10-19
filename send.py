import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Open UDP socket

print "UDP Target IP: ", UDP_IP
print "UDP Target Port: ", UDP_PORT

sock.sendto("Oi puto", (UDP_IP, UDP_PORT))
