class create (object):
    start = "start"
    token = ""
    control = ""
    origin = ""
    dest = ""
    x = ""
    y = ""
    seen = False
    hit = False
    miss = False
    kill = False

    def __init__(self, token, control, dest, x = "", y = ""):
        self.token = token
        self.control = control
        self.origin = socket.gethostname
        self.dest = dest
        self.x = x
        self.y = y
