import time


class Ts3Client:

    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr
        self.lastseen = time.time()

    def get_addr(self):
        return self.addr

    def get_socket(self):
        self.lastseen = time.time()
        return self.socket

    def fileno(self):
        return self.socket.fileno()
