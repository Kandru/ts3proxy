import time
import socket
import select
import uuid

from .ts3client import Ts3Client

"""tcp relay class

class for relaying the teamspeak3 tcp communication stuff
"""


class Tcp():

    def __init__(self, relayAddr="0.0.0.0", relayPort=9987, remoteAddr="127.0.0.1", remotePort=9987):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((relayAddr, relayPort))
        self.socket.listen()
        self.remoteAddr = remoteAddr
        self.remotePort = remotePort
        self.clients = {}

    def relay(self):
        while True:
            readable, writable, exceptional = select.select(list(self.clients.values()) + [self.socket], [], [], 1)
            for s in readable:
                # if ts3 server answers to a client or vice versa
                if isinstance(s, Ts3Client):
                    try:
                        data = s.socket.recv(4096)
                        if len(data) != 0:
                            self.clients[s.addr].socket.send(data)
                        else:
                            raise
                    except:
                        # get second socket from list
                        addr = self.clients[s.addr].addr
                        try:
                            # close other socket
                            self.clients[s.addr].socket.close()
                        except:
                            pass
                        try:
                            # close own socket, too
                            self.clients[addr].socket.close()
                        except:
                            pass
                        del self.clients[s.addr]
                        del self.clients[addr]
                        if isinstance(addr, tuple):
                            print('disconnected', addr)
                        else:
                            print('disconnected', s.addr)
                else:
                    conn, addr = s.accept()
                    data = conn.recv(4096)
                    print('connected', addr)
                    tmpuid = str(uuid.uuid4())
                    self.clients[addr] = Ts3Client(conn, tmpuid)
                    self.clients[tmpuid] = Ts3Client(socket.socket(socket.AF_INET, socket.SOCK_STREAM), addr)
                    self.clients[tmpuid].socket.connect((self.remoteAddr, self.remotePort))
                    self.clients[tmpuid].socket.send(data)
