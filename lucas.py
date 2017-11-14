
# -*- coding:utf-8 -*-

import socket
import os
import sys
import time
import pickle
import message

def getnextmachine():
	machineName = raw_input()
	validHost = False
	while validHost == False:
		try:
			test = socket.gethostbyname(machineName)
			validHost = True
		except:
			print('Nome de máquina inválido. Insira o nome de uma máquina conectada na rede e veja se ela está ligada.')
			machineName = raw_input()
	return machineName


my_name = socket.gethostname()
my_ip = socket.gethostbyname(my_name) #Pegando IP da máquina local
mID = 0 # machine ID
next_in_ring = ''
port = 5000
host = False

socketSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para enviar dados
socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para receber dados


socketReceiver.bind((my_ip, port))
os.system("clear")

if(len(sys.argv) > 1):
	if(sys.argv[1] == 'h'):
		print('Você é a primeira máquina da partida.')
		host = True
	else:
		print('Argumento inválido. Use h para iniciar em modo host.')
		sys.exit()

print("Qual máquina você quer conectar?")
next_name = getnextmachine()
next_ip = socket.gethostbyname(next_name)

print("A proxima máquina no anel é: " + next_name + "(" + next_ip +")")


if(host):
	message = Message(True, False, next_name, mID)
	message = pickle.dumps(message)
	socketSender.sendto(message, (next_ip, port))

	#Aguarda mensagem da última máquina
	data, address = socketReceiver.recvfrom(1024)
	data = pickle.loads(data)

	#if(data.start == 'start'):
else:
	data, address = socketReceiver.recvfrom(1024)
	print (address)
	mID = data.x + 1 #Campo de coordenada x é usado para transportar o ID neste momento
	print (mID)
	message = Message(True, False, next_name, mID)
	message = pickle.dumps(message)
	socketSender.sendto(message, (next_ip, port))


while(True):

	data,address = socketReceiver.recvfrom(1024)
	data = pickle.loads(data)
	print("Recebido de " +  socket.gethostbyaddr(address[0])[0] + ":")
	print(data.a)
	print(data.b)
	print(data.c)
	print(data.d)

	time.sleep(1)
	socketSender.sendto(pickle.dumps(data),(next_ip,port))
