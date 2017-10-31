# -*- coding:utf-8 -*-

import socket
import os

def packIp(ip):
    a,b,c,d= list(map(int, ip.split('.')))
    return (a, b, c, d)

def unpackIp(a,b,c,d):
    ip = [a,b,c,d]
    return('.'.join(map(str,ip)))

my_ip = socket.gethostbyname(socket.gethostname()) #pego nome da minha maquina, e dai pego o ip dela
next_in_ring = ''
port = 5000

socketSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para enviar dados
socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para receber dados
#é necessário ter dois sockets, pois o de recebimento sera 'binded' numa porta

socketReceiver.bind((my_ip,port)) #'binding' do socket
os.system("clear")

print("Qual maquina você quer conectar?")
otherMachineName = raw_input()
next_in_ring = socket.gethostbyname(otherMachineName)

print("A proxima máquina no anel é: " + otherMachineName + "(" + next_in_ring +")")
while(True):

	print("Digite uma mensagem para enviar:")
	message = raw_input()
	socketSender.sendto(message.encode(),(next_in_ring,port))

	data,address = socketReceiver.recvfrom(1024)
	data = data.decode()
	print("Recebido de " +  socket.gethostbyaddr(address[0])[0] + ":")
	print(data)
