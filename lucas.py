
# -*- coding:utf-8 -*-

import socket
import os
import sys
import time
import pickle
import message

my_ip = socket.gethostbyname(socket.gethostname()) #pego nome da minha maquina, e dai pego o ip dela
next_in_ring = ''
port = 5000
host = False

socketSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para enviar dados
socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para receber dados
#é necessário ter dois sockets, pois o de recebimento sera 'binded' numa porta

socketReceiver.bind((my_ip,port)) #'binding' do socket
os.system("clear")

print("Qual maquina você quer conectar?")
otherMachineName = raw_input()
next_in_ring = socket.gethostbyname(otherMachineName)


print("A proxima máquina no anel é: " + otherMachineName + "(" + next_in_ring +")")
massage= Message('d')
picmessage = pickle.dumps(massage)

if(len(sys.argv) > 1):
	if(sys.argv[1] == 'h'):
		print('Você é a primeira máquina da partida.')
		host = True
		socketSender.sendto(picmessage,(next_in_ring,port))


while(True):

	data,address = socketReceiver.recvfrom(1024)
	data = pickle.loads(data)
	print("Recebido de " +  socket.gethostbyaddr(address[0])[0] + ":")
	print(data.a)
	print(data.b)
	print(data.c)
	print(data.d)

	time.sleep(1)
	socketSender.sendto(pickle.dumps(data),(next_in_ring,port))
