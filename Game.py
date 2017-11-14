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
        players = ''
        kills = 0
        ship_count = 2

    def createShip(self):
        #Primeiro navio
        x, y = 5, 5
        os.system("clear")
        self.printField()

        print('Posicione o primeiro navio.')
        print('Insira sua orientação(v = vertical, h = horizontal): '),
        orientation = raw_input()
        while(orientation != 'v' and orientation != 'h'):
            print('Insira uma orientação válida: '),
            orientation = raw_input()

        while(x > 4 or y > 4):
            print('Insira sua coordenada inicial no eixo X:')
            x = raw_input()
            print('Insira sua coordenada inicial no eixo Y:')
            y = raw_input()

            try:
                x = int(x)
                y = int(y)

            except:
                print('Insira coordenadas válidas.')
            if(x > 4 or y > 4):
                print('São aceitos números inteiros de 0 a 4.')



    def printField(self):
        for x in range(5):
            for y in range(5):
                print('|' + ' ' + '|'),
            print('')
            print('-------------------')

game = create()
game.createShips()
