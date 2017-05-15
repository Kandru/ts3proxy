import time
import socket
import threading


class Tcp():

    def __init__(self, relayPort, remoteAddr, remotePort):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", relayPort))
        self.socket.listen()
        self.remoteAddr = remoteAddr
        self.remotePort = remotePort
        self.clientList = dict()
        t = threading.Thread(target=self.get_from_server)
        t.start()

    def get_from_server(self):
        while True:
            # send data from remote server to specific client
            for key in list(self.clientList):
                try:
                    data = self.clientList[key]['rsocket'].recv(1024)
                    self.clientList[key]['lastseen'] = time.time()
                    self.clientList[key]['csocket'].send(data)
                except socket.error as msg:
                    pass
            time.sleep(.025)

    def get_from_client(self, conn, addr):
        while True:
            try:
                # if we see the client the first time
                if not addr in self.clientList:
                    print('connected: ' + str(addr))
                    rsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    rsocket.connect((self.remoteAddr, self.remotePort))
                    rsocket.setblocking(False)
                    self.clientList[addr] = {
                        'rsocket': rsocket,
                        'csocket': conn,
                        'lastseen': time.time()
                    }
                data = conn.recv(1024)
                if len(data) != 0:
                    self.clientList[addr]['rsocket'].send(data)
                else:
                    self.clientList[addr]['rsocket'].close()
                    del self.clientList[addr]
                    print('disconnected: ' + str(addr))
                    break
            except:
                try:
                    self.clientList[addr]['rsocket'].close()
                except:
                    pass
                try:
                    self.clientList[addr]['csocket'].close()
                except:
                    pass
                del self.clientList[addr]
                print('disconnected: ' + str(addr))
                break
            time.sleep(.025)

    def relay(self):
        while True:
            # get data from an connected client
            conn, addr = self.socket.accept()
            try:
                t = threading.Thread(
                    target=self.get_from_client, args=(conn, addr))
                t.start()
            except:
                pass
