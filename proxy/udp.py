import time
import socket
import threading
import select

from .ts3client import Ts3Client

"""udp relay class

class for relaying the teamspeak3 udp communication stuff
"""


class Udp():

    def __init__(self, relayPort, remoteAddr, remotePort):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", relayPort))
        self.remoteAddr = remoteAddr
        self.remotePort = remotePort
        self.clients = []
        t = threading.Thread(target=self.proof_client_timeout)
        t.start()

    def proof_client_timeout(self):
        while True:
            # iterare through clients and find one with timeout
            item = next((x for x in self.clients if x.last_seen <= time.time() - 2), None)
            if item:
                try:
                    item.socket.close()
                except:
                    pass
                print('disconnected: ' + str(item.addr))
                del self.clients[self.clients.index(item)]
            time.sleep(1)

    def relay(self):
        while True:
            try:
                readable, writable, exceptional = select.select(
                    list(self.clients) + [self.socket], [], list(self.clients))
                for s in readable:
                    # if ts3 server answers to a client
                    if isinstance(s, Ts3Client):
                        data, addr = s.socket.recvfrom(1024)
                        self.socket.sendto(data, s.addr)
                    else:
                        # if a client sends something to a ts3 server
                        data, addr = s.recvfrom(1024)
                        tmpSocket = next((x for x in self.clients if x.addr == addr), None)
                        # if its a new and unkown client
                        if not tmpSocket:
                            print('connected: ' + str(addr))
                            tmpSocket = Ts3Client(socket.socket(socket.AF_INET, socket.SOCK_DGRAM), addr)
                            self.clients.append(tmpSocket)
                        # send data to ts3 server
                        tmpSocket.socket.sendto(data, (self.remoteAddr, self.remotePort))
            except:
                pass
