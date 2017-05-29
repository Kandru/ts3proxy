import time


class Ts3Client:

    def __init__(self, socket, addr):
        self._socket = socket
        self.addr = addr
        self.last_seen = time.time()

    def fileno(self):
        return self._socket.fileno()

    @property
    def socket(self):
        self.last_seen = time.time()
        return self._socket
