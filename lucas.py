
# -*- coding:utf-8 -*-

import socket
import os
import time
import pickle

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

class Message (object):
	a = "a"
	b = "b"
	c = True
	d = ""
	def __init__ (self, d):
		self.d = d



print("A proxima máquina no anel é: " + otherMachineName + "(" + next_in_ring +")")
message= Message('d')
picmessage = pickle.dumps(message)

if(raw_input() == 'a'):
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
	socketSender.sendto(data = pickle.dumps(data),(next_in_ring,port))
