import time
import socket
import threading
import select

from proxy.ts3client import ts3client

"""udp relay class

class for relaying the teamspeak3 udp communication stuff
"""


class udp():

    def __init__(self, relayPort, remoteAddr, remotePort):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", relayPort))
        self.remoteAddr = remoteAddr
        self.remotePort = remotePort
        self.clients = []
        t = threading.Thread(target=self.proofClientTimeout)
        t.start()

    def proofClientTimeout(self):
        while True:
            # iterare through clients and find one with timeout
            item = next(
                (x for x in self.clients if x.lastseen <= time.time() - 2), None)
            if item:
                try:
                    item.getSocket().close()
                except:
                    pass
                print('disconnected: ' + str(item.getAddr()))
                del self.clients[self.clients.index(item)]
                pass
            time.sleep(1)

    def relay(self):
        while True:
            try:
                readable, writable, exceptional = select.select(
                    list(self.clients) + [self.socket], [], list(self.clients))
                for s in readable:
                    # if ts3 server answers to a client
                    if isinstance(s, ts3client):
                        data, addr = s.getSocket().recvfrom(1024)
                        self.socket.sendto(data, s.getAddr())
                    else:
                        # if a client sends something to a ts3 server
                        data, addr = s.recvfrom(1024)
                        tmpSocket = next(
                            (x for x in self.clients if x.addr == addr), None)
                        # if its a new and unkown client
                        if not tmpSocket:
                            print('connected: ' + str(addr))
                            tmpSocket = ts3client(socket.socket(
                                socket.AF_INET, socket.SOCK_DGRAM), addr)
                            self.clients.append(tmpSocket)
                        # send data to ts3 server
                        tmpSocket.getSocket().sendto(
                            data, (self.remoteAddr, self.remotePort))
            except:
                pass
