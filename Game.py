# -*- coding:utf-8 -*-
import socket
import os

class message (object):
    def __init__(self, token, control, dest, x = "", y = "", orientation = 'v'):
        self.start = "start"
        self.token = token
        self.control = control
        self.origin = socket.gethostname
        self.dest = dest
        self.x = x
        self.y = y
        self.seen = False
        self.hit = False
        self.miss = False
        self.kill = False

class create(object):
    def __init__(self):
        self.field = [[0 for x in range(5)] for y in range(5)] # Inicializa uma matriz 5x5, preenchida com 0s
        self.players = ''
        self.kills = 0
        self.ship_count = 0

    def createShip(self):
        #Primeiro navio
        x, y = 5, 5
        os.system("clear")
        self.ship_count += 1
        self.printField()

        print('Insira sua orientação(v = vertical, h = horizontal): '),
        orientation = raw_input()
        while(orientation != 'v' and orientation != 'h'):
            print('Insira uma orientação válida: '),
            orientation = raw_input()

        while(x > 2 or y > 2):
            print('Insira sua coordenada inicial no eixo X:')
            x = raw_input()
            print('Insira sua coordenada inicial no eixo Y:')
            y = raw_input()

            try:
                x = int(x)
                y = int(y)

            except:
                print('Insira coordenadas válidas.')

            #TODO Pode ser maior que 2. Ver orientação
            if(x > 2 or y > 2):
                print('São aceitos números inteiros de 0 a 2.')

            if(orientation == 'h'):
                for i in range(0, 3):
                    if(self.field[x + i][y] == 0):
                        self.field[x + i][y] = self.ship_count
                    else:
                        print('Já há um navio ocupando essa posição. Insira as coordenadas novamente.')
                        x, y = 5, 5
            else:
                for i in range(0, 3):
                    if(self.field[x][y + i] == 0):
                        self.field[x][y + i] = self.ship_count
                    else:
                        print('Já há um navio ocupando essa posição. Insira as coordenadas novamente.')
                        x, y = 5, 5




    def printField(self):
        for y in range(0, 5):
            for x in range(0, 5):
                if(self.field[x][y] == 0):
                    print('|' + ' ' + '|'),
                elif(self.field[x][y] > 0):
                    print('|' + str(self.field[x][y]) + '|'),
                else:
                    print('|' + 'X' + '|'),

            print('')
            print('-------------------')

game = create()
print('Posicione o primeiro navio.')
game.createShip()
print('Posicione o segundo navio.')
game.createShip()
game.printField()
