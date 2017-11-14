import socket
class message (object):
    def __init__(self, token, control, dest, x = "", y = ""):
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
        self.field = [[0 for x in range(5)] for y in range(5)] # Inicializa uma matriz 5x5, preenchida com
        players = ''
        kills = 0
        ships = 2
