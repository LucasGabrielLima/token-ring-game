# -*- coding:utf-8 -*-
import socket
import os

class message (object):
    def __init__(self, token, control, dest, x = "", y = ""):
        self.start = "start"
        self.token = token
        self.control = control
        self.attack = False
        self.origin = socket.gethostname()
        self.dest = dest
        self.x = x
        self.y = y
        self.seen = False
        self.hit = False
        self.kill = False

class create(object):
    def __init__(self):
        self.field = [[0 for x in range(5)] for y in range(5)] # Inicializa uma matriz 5x5, preenchida com 0s
        self.players = []
        self.kills = 0
        self.ship1_lives = 3
        self.ship2_lives = 3
        self.ship_count = 0

    def createShip(self):
        #Primeiro navio
        x, y = 5, 5
        os.system("clear")
        self.ship_count += 1
        self.printField()

        print('Posicione o ' + str(self.ship_count) + 'o navio.')
        print('Insira sua orientação(v = vertical, h = horizontal): '),
        orientation = raw_input()
        while(orientation != 'v' and orientation != 'h'):
            print('Insira uma orientação válida: '),
            orientation = raw_input()

        while(not validxy(x, y, orientation)):
            print('Insira sua coordenada inicial no eixo X:')
            x = raw_input()
            print('Insira sua coordenada inicial no eixo Y:')
            y = raw_input()

            try:
                x = int(x)
                y = int(y)

            except:
                print('Insira coordenadas válidas.')


            if(self.ship_count == 1):
                self.ship1_orientation = orientation
            else:
                self.ship2_orientation = orientation
            if(orientation == 'h'):
                inbounds = True
                try:
                    for i in range (0, 3):
                        if(self.field[x + i][y] != 0):
                            print('Já há um navio ocupando essa posição. Insira as coordenadas novamente.')
                            inbounds = False
                            x, y = 5, 5
                except:
                    print('Coordenadas inválidas. Tente novamente.')
                    inbounds = False
                    x, y = 5, 5

                if(inbounds):
                    for i in range(0, 3):
                        self.field[x + i][y] = self.ship_count

            else:
                inbounds = True
                try:
                    for i in range (0, 3):
                        if(self.field[x][y + i] != 0):
                            print('Já há um navio ocupando essa posição. Insira as coordenadas novamente.')
                            inbounds = False
                            x, y = 5, 5
                except:
                    print('Coordenadas inválidas. Tente novamente.')
                    inbounds = False
                    x, y = 5, 5

                if(inbounds):
                    for i in range(0, 3):
                        self.field[x][y + i] = self.ship_count
            self.ship1x = x
            self.ship1y = y
            self.ship2x = x
            self.ship2y = y


    def printField(self, f = 'default'):
        if(f == 'default'):
            f = self.field
        for y in range(0, 5):
            for x in range(0, 5):
                if(f[x][y] == 0):
                    print('|' + ' ' + '|'),
                elif(f[x][y] > 0):
                    print('|' + str(f[x][y]) + '|'),
                else:
                    print('|' + 'X' + '|'),

            print('')
            print('-------------------')
        print('')

class player(object):
    def __init__(self, field, mID):
        self.field = field
        self.mID = mID
        self.ships = 2

def validxy(x, y, orientation):
    return not((x > 2 and orientation == 'h') or (y > 2 and orientation == 'v'))
