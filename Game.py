import socket
class message (object):
    def __init__(self, token, control, dest, x = "", y = "", orientation = 'v'):
        self.start = "start"
        self.token = token
        self.control = control
        self.origin = socket.gethostname
        self.dest = dest
        self.x = x
        self.y = y
        self.orientation = orientation
        self.seen = False
        self.hit = False
        self.miss = False
        self.kill = False

class create(object):
    def __init__(self):
        self.field = [[0 for x in range(5)] for y in range(5)] # Inicializa uma matriz 5x5, preenchida com 0s
        players = ''
        kills = 0
        ships = 2

    def printField(self):
        for x in range(5):
            for y in range(5):
                print('|' + str(self.field[x][y]) + '|'),
            print('')
            print('-------------------')



game = create()
game.printField()
