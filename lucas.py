# -*- coding:utf-8 -*-

import socket
import os
import sys
import time
import pickle
import Game

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

def initField():
	field = [[0 for x in range(5)] for y in range(5)] # Inicializa uma matriz 5x5, preenchida com 0s
	return field

def initPlayers():
	for i in range(num_players):
		if(i + 1 != mID):
			field = initField()
			player = Game.player(field, i+1)
			game.players.append(player)

def validxy(x, y):
    return (x < 5 and y < 5)

def makePlay():
	print('Qual o ID do jogador que você quer atacar?')
	validID = False
	while(validID = False)
	player = raw_input()
	try:
		player = int(player)
		validID = True
		if(player == mID):
			print("Tá tudo bem? Você não pode atacar a si mesmo :(")
			validID = False
		elif(player > num_players):
			print("Não há nenhum jogador com este ID.")
			validID = False
	except:
		print('Insira um ID válido. São aceitos números entre 1 e ' + str(num_players))


	x, y = 5, 5
	while(not validxy(x, y)):
		print('Insira a coordenada de ataque no eixo X:')
		x = raw_input()
		print('Insira a coordenada de ataque no eixo Y:')
		y = raw_input()

		try:
			x = int(x)
			y = int(y)

		except:
			print('Insira coordenadas válidas.')

	play = Game.message(False, False, player, x, y)
	send(play)


def receive(): #Recebimento com tratamento de Timeout
	try:
		data, address = socketReceiver.recvfrom(1024)
	except:
		print('Ocorreu um timeout na conexão. Reinicie o jogo.')
		sys.exit()

	data = pickle.loads(data)

	try:
		if (data.start != 'start'):
			print("Você recebeu dados de fontes desconhecidas na porta de recebimento. Por favor mude a porta e tente novamente.")
			sys.exit()
	except:
			sys.exit()

	return data, address

def send(message):
	message = pickle.dumps(message)
	socketSender.sendto(message, (next_ip, port))

###### CONFIGURAÇÃO DOS SOCKETS #######

my_name = socket.gethostname()
my_ip = socket.gethostbyname(my_name) #Pegando IP da máquina local
mID = 0 # machine ID
next_in_ring = ''
port = 5000
host = False
num_players = 3

socketSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para enviar dados
socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket para receber dados
socketReceiver.bind((my_ip, port))
#socketReceiver.settimeout(5) #set time out

######################################

os.system("clear")

###### TRATA ARGUMENTOS ##########
if(len(sys.argv) > 1):
	if(sys.argv[1] == 'h'):
		print('Você é a primeira máquina da partida.')
		host = True
	else:
		print('Argumento inválido. Use h para iniciar em modo host.')
		sys.exit()

###########################

#
# ###### CONEXÃO COM OUTRAS MÁQUINAS; CONFIGURAÇÃO DO ANEL ##########
#
# print("Qual máquina você quer conectar?")
# next_name = getnextmachine()
# next_ip = socket.gethostbyname(next_name)
#
# print("A proxima máquina no anel é: " + next_name + "(" + next_ip +")")
#
# #############################
#
#
# ####### ESTABELECE ANEL ###############
# if(host):
# 	#Mensagem inicial
# 	message = Game.message(False, True, next_name, mID)
# 	send(message)
#
# 	#Aguarda mensagem da última máquina
# 	data, address = receive()
# 	if(data.x != num_players - 1):
# 		print('Ocorreu um erro na configuração no anel. A 4a e última máquina deve se conectar ao host. Tente novamente.')
# 		sys.exit()
#
# 	mID = data.x + 1 #host tem mID = numero de jogadores
#
# 	#Envia segunda mensagem, para testar conexão do anel
# 	message = Game.message(False, True, next_name, 0)
# 	send(message)
# 	data, address = receive()
# 	if(data.control == True and data.x == mID - 1):
# 		print('Configuração da conexão finalizada. O ID da sua máquina é: ', mID)
# 	else:
# 		print('Ocorreu um erro na configuração do anel. Mensagem de testes mal sucedida. Tente novamente.')
# 		sys.exit()
#
# else:
# 	#Primeira mensagem, seta o ID das máquinas e realiza conexão inicial do anel
# 	data, address = receive()
# 	print (address)
# 	mID = data.x + 1 #Campo de coordenada x é usado para transportar o ID neste momento
# 	data.x += 1
# 	send(data)
#
# 	#Segunda mensagem, testa conexão do anel.
# 	data, address = receive()
# 	if(data.control == True and data.x == mID - 1):
# 		print('O ID da sua máquina é: ', mID)
# 		data.x += 1
# 		data.dest = next_name
# 		send(data)
# 	else:
# 		print('Ocorreu um erro na configuração do anel. Mensagem de testes mal sucedida. Tente novamente.')
# 		sys.exit()
#
# time.sleep(3)
# #######################################
#
######### CONFIGURAÇÃO INICIAL DO JOGO####
game = Game.create()

#Configura posição dos dois navios
game.createShip()
game.createShip()
game.printField()
print('Navios posicionados com sucesso.')

initPlayers()
print('Campos dos jogadores adversários:')
game.printField(game.players[0].field)
game.printField(game.players[1].field)
game.printField(game.players[2].field)

#######################

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
