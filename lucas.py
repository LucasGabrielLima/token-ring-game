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
    game.players_left = 0
    for i in range(num_players):
        if(i + 1 != mID):
            field = initField()
            player = Game.player(field, i+1)
            player.ship_count = 2
            game.players.append(player)
            game.players_left += 1

def validxy(x, y):
    return (x < 5 and y < 5)

def makePlay():
    print('Qual o ID do jogador que você quer atacar?')
    validID = False
    while(validID == False):
        player = raw_input()
        try:
            player = int(player)
            validID = True
            if(player == mID):
                print("Tá tudo bem? Você não pode atacar a si mesmo :(")
                validID = False
            elif(player > num_players or player < 1):
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
    play.attack = True
    return play


def receive(): #Recebimento com tratamento de Timeout
    try:
        data, address = socketReceiver.recvfrom(2048)
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

def sendToken(token):
    send(token)
    has_token = False

def getPlayerByID(mID):
    for i in range(len(game.players)):
        if(game.players[i].mID == mID):
            return i

def checkForHit(play):
    if(play.hit == True):
        print('Você atingiu um navio!')
        game.players[getPlayerByID(play.dest)].field[play.x][play.y] = -1
        return True
    else:
        print('Água! Você errou :(')
        return False

def checkForKill(play):
    if(play.kill == True and play.origin == my_name):
        print('Você destruiu um navio do jogador adversário!!!')
        orientation = play.orientation
        dest = play.dest
        x = play.x
        y = play.y
        game.players[getPlayerByID(play.dest)].ships -= 1

        if(game.players[getPlayerByID(play.dest)].ships == 0):
            game.players_left -= 1
            if(game.players_left == 0):
                print('Você venceU!!! Parabéns!!! Uhul!!! VAMO DALEEEE!!!')
                time.sleep(3)
                exit()

        if(orientation == 'h'):
            for i in range(0, 3):
                game.players[getPlayerByID(play.dest)].field[x + i][y] = -1

        elif(orientation == 'v'):
            for i in range(0, 3):
                game.players[getPlayerByID(play.dest)].field[x][y + i] = -1

        message = Game.message(False, True, 'all', x, y) #Envia mensagem a todos os jogadores informando a morte de um navio
        message.orientation = orientation
        message.player = dest
        message.mID = play.dest
        message.kill = True
        send(message)

def sendPlay(play):
    send(play)

	socket.settimeout(5) # Seta o timeout da mensagem
    play, address = receive()
    i = 0
    while(play.seen == False and i < 3):
        send(play)
        i += 1
        play, address = receive()

    if(play.seen == False):
        print('Ocorreu um erro na conexão. Reinicie o jogo.')
        sys.exit()

	socket.settimeout(None) # Retira o timeout para que ele não ocorra enquanto a vez dos outros jogadores

    checkForHit(play)
    checkForKill(play)

def attacked(play):
    play.seen = True
    x = play.x
    y = play.y

    print('Você foi atacado na posição (' + str(x) + ', ' + str(y) + ').')

    if(game.field[x][y] > 0):
        play.hit = True
        ship = game.field[x][y]
        print('O navio ' + str(ship) + ' foi atingido.')
        game.field[x][y] = -1

        if(ship == 1):
            game.ship1_lives -= 1
            if(game.ship1_lives == 0):
                print('O navio ' + str(ship) + ' foi destruido')
                game.ship_count -= 1
                play.kill = True
                play.orientation = game.ship1_orientation
                play.x = game.ship1x
                play.y = game.ship1y

                if(game.ship_count == 0):
                    print('Seus navios foram destruídos. Você foi eliminado :(')
                    print('noob')

        else:
            game.ship2_lives -= 1
            if(game.ship2_lives == 0):
                print('O navio ' + str(ship) + ' foi destruido')
                game.ship_count -= 1
                play.kill = True
                play.orientation = game.ship2_orientation
                play.x = game.ship2x
                play.y = game.ship2y


                if(game.ship_count == 0):
                    play.dead = True
                    print('Seus navios foram destruídos. Você foi eliminado :(')
                    print('noob')

        printGame()


def printGame():
    print('Seu ID é: ' + str(mID))
    game.printField()
    print('')

    print('Campos adversários:')
    for i in range(len(game.players)):
        print('Jogador ' + str(game.players[i].mID) + ':')
        game.printField(game.players[i].field)



###### CONFIGURAÇÃO DOS SOCKETS #######

my_name = socket.gethostname()
my_ip = socket.gethostbyname(my_name) #Pegando IP da máquina local
mID = 0 # machine ID
next_in_ring = ''
port = 5005
host = False
num_players = 4
has_token = False

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


###### CONEXÃO COM OUTRAS MÁQUINAS; CONFIGURAÇÃO DO ANEL ##########

print("Qual máquina você quer conectar?")
next_name = getnextmachine()
next_ip = socket.gethostbyname(next_name)

print("A proxima máquina no anel é: " + next_name + "(" + next_ip +")")

#############################


####### ESTABELECE ANEL ###############
if(host):
    #Mensagem inicial
    message = Game.message(False, True, next_name, mID)
    send(message)

    #Aguarda mensagem da última máquina
    data, address = receive()
    if(data.x != num_players - 1):
        print('Ocorreu um erro na configuração no anel. A 4a e última máquina deve se conectar ao host. Tente novamente.')
        sys.exit()

    mID = data.x + 1 #host tem mID = numero de jogadores

    #Envia segunda mensagem, para testar conexão do anel
    message = Game.message(False, True, next_name, 0)
    send(message)
    data, address = receive()
    if(data.control == True and data.x == mID - 1):
        print('Configuração da conexão finalizada. O ID da sua máquina é: ' + str(mID))
    else:
        print('Ocorreu um erro na configuração do anel. Mensagem de testes mal sucedida. Tente novamente.')
        sys.exit()

else:
    #Primeira mensagem, seta o ID das máquinas e realiza conexão inicial do anel
    data, address = receive()
    print (address)
    mID = data.x + 1 #Campo de coordenada x é usado para transportar o ID neste momento
    data.x += 1
    send(data)

    #Segunda mensagem, testa conexão do anel.
    data, address = receive()
    if(data.control == True and data.x == mID - 1):
        print('O ID da sua máquina é: ' + str(mID))
        data.x += 1
        data.dest = next_name
        send(data)
    else:
        print('Ocorreu um erro na configuração do anel. Mensagem de testes mal sucedida. Tente novamente.')
        sys.exit()

time.sleep(3)
#######################################

######### CONFIGURAÇÃO INICIAL DO JOGO####
game = Game.create()

#Configura posição dos dois navios
game.createShip()
game.createShip()
game.printField()
print('Navios posicionados com sucesso.')

#Configura adversários
initPlayers()
print('Campos adversários:')
for i in range(len(game.players)):
    print('Jogador ' + str(game.players[i].mID) + ':')
    game.printField(game.players[i].field)

#######################

#######CRIA TOKEN E PRIMEIRA JOGADA##########
if(host):
    token = Game.message(True, False, 'all')
    has_token = True
    play = makePlay()
    sendPlay(play)
    printGame()
    sendToken(token)

###################

while(True):
    data, address = receive()
    if(data.dest == mID or data.dest == 'all'):
        #If message is token
        if(data.token):
            token = data
            has_token = True
            if(game.ship_count > 0):
                play = makePlay()
                sendPlay(play)
                printGame()

            sendToken(token)

        #If message is a kill broadcast
        elif(data.control and data.kill and data.player != mID and data.origin != my_name):
            orientation = data.orientation
            x = data.x
            y = data.y
            game.players[getPlayerByID(data.player)].ship_count -= 1

            if(game.players[getPlayerByID(data.player)].ship_count == 0):
                game.players_left -= 1
                print('O jogador ' + str(data.player) + ' foi eliminado.' )

            if(orientation == 'h'):
                for i in range(0, 3):
                    game.players[getPlayerByID(data.player)].field[x + i][y] = -1

            else:
                for i in range(0, 3):
                    game.players[getPlayerByID(data.player)].field[x][y + i] = -1

            printGame()
            send(data)

        #If message is an atack
        elif(data.attack == True):
            attacked(data)
            send(data)


    else: # Se a mensagem não for pra mim, manda pra frente
        send(data)
