
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
			print('Nome de máquina inválido. Insira o nome de uma máquina ligada na rede e veja se a máquina está ligada.')
			machineName = raw_input()
	return machineName


my_ip = socket.gethostbyname(socket.gethostname()) #Pegando IP da máquina local
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
otherMachineName = getnextmachine()
next_in_ring = socket.gethostbyname(otherMachineName)

print("A proxima máquina no anel é: " + otherMachineName + "(" + next_in_ring +")")


if(host):
	socketSender.sendto(picmessage,(next_in_ring,port))

	#Aguarda mensagem da última máquina
	data, address = socketReceiver.recvfrom(1024)
	data = pickle.loads(data)

	#if(data.start == 'start'):


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
