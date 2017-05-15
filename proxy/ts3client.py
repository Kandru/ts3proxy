import time


class ts3client():

    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr
        self.lastseen = time.time()

    def getAddr(self):
        return self.addr

    def getSocket(self):
        self.lastseen = time.time()
        return self.socket

    def fileno(self):
        return self.socket.fileno()
