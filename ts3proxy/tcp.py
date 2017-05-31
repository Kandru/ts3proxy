import select
import socket
import threading
import uuid

from .blacklist import Blacklist
from .ts3client import Ts3Client


class TcpRelay:
    """
    Relay for TCP communication of TeamSpeak 3
    """

    def __init__(self, logging,
                 relay_address="0.0.0.0", relay_port=9987,
                 remote_address="127.0.0.1", remote_port=9987,
                 blacklist_file="blacklist.txt", whitelist_file="whitelist.txt"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((relay_address, relay_port))
        self.socket.listen()
        self.relay_address = relay_address
        self.relay_port = relay_port
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.blacklist = Blacklist(blacklist_file, whitelist_file)
        self.logging = logging
        self.clients = {}

        self.thread = None
        self.run_loop = True

    def disconnect_client(self, addr, socket):
        self.logging.info('connection from {} not allowed'.format(addr[0]))
        socket.close()

    def start_thread(self):
        self.thread = threading.Thread(target=self.relay)
        self.thread.start()

    def stop_thread(self):
        self.run_loop = False
        # close one socket so that select returns
        self.socket.close()

    def relay(self):
        while True:
            readable, writable, exceptional = select.select(list(self.clients.values()) + [self.socket], [], [], 1)
            if not self.run_loop:
                # stop thread
                break
            for s in readable:
                # if ts3 server answers to a client or vice versa
                if isinstance(s, Ts3Client):
                    try:
                        data = s.socket.recv(4096)
                        if len(data) != 0:
                            self.clients[s.addr].socket.send(data)
                        else:
                            raise Exception
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
                            self.logging.debug('disconnected: {}'.format(addr))
                        else:
                            self.logging.debug('disconnected: {}'.format(s.addr))
                else:
                    conn, addr = s.accept()
                    data = conn.recv(4096)
                    if self.blacklist.check(addr[0]):
                        self.logging.debug('connected: {}'.format(addr))
                        tmpuid = str(uuid.uuid4())
                        self.clients[addr] = Ts3Client(conn, tmpuid)
                        self.clients[tmpuid] = Ts3Client(socket.socket(socket.AF_INET, socket.SOCK_STREAM), addr)
                        self.clients[tmpuid].socket.connect((self.remote_address, self.remote_port))
                        self.clients[tmpuid].socket.send(data)
                    else:
                        self.disconnect_client(addr, conn)

    @classmethod
    def create_from_config(cls, logging, relay_config):
        return cls(
            logging=logging,
            relay_address=relay_config['relayAddress'],
            relay_port=relay_config['relayPort'],
            remote_address=relay_config['remoteAddress'],
            remote_port=relay_config['remotePort'],
            blacklist_file=relay_config['blacklist'],
            whitelist_file=relay_config['whitelist'],
        )
