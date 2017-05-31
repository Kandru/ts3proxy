import select
import socket
import threading
import time

from .blacklist import Blacklist
from .ts3client import Ts3Client


class UdpRelay:
    """
    Relay for UDP communication of TeamSpeak 3
    """

    def __init__(self, logging, statistics,
                 relay_address="0.0.0.0", relay_port=9987,
                 remote_address="127.0.0.1", remote_port=9987,
                 blacklist_file="blacklist.txt", whitelist_file="whitelist.txt"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((relay_address, relay_port))
        self.relay_address = relay_address
        self.relay_port = relay_port
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.blacklist = Blacklist(blacklist_file, whitelist_file)
        self.logging = logging
        self.statistics = statistics
        self.clients = {}

        self.thread = None
        self.run_loop = True

    def disconnect_client(self, addr, socket):
        if socket:
            try:
                socket.close()
            except OSError:
                pass
        if addr in self.clients:
            del self.clients[addr]
            self.statistics.remove_user(addr)

    def start_thread(self):
        self.thread = threading.Thread(target=self.relay)
        self.thread.start()
        self.run_loop = True

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
                # if ts3 server answers to a client
                if isinstance(s, Ts3Client):
                    data, addr = s.socket.recvfrom(1024)
                    self.socket.sendto(data, s.addr)
                else:
                    # if a client sends something to a ts3 server
                    data, addr = s.recvfrom(1024)
                    # check if the client is denied by our blacklist
                    if self.blacklist.check(addr[0]):
                        # if its a new and unkown client
                        if addr not in self.clients:
                            if not self.statistics.user_limit_reached():
                                self.logging.debug('connection from: {}'.format(addr))
                                self.clients[addr] = Ts3Client(socket.socket(socket.AF_INET, socket.SOCK_DGRAM), addr)
                                self.statistics.add_user(addr)
                            else:
                                self.logging.info('connection from {} not allowed. user limit ({}) reached.'.format(
                                    addr[0], self.statistics.max_users))
                                self.disconnect_client(addr, None)
                        # send data to ts3 server
                        if addr in self.clients:
                            self.clients[addr].socket.sendto(data, (self.remote_address, self.remote_port))
                    else:
                        self.logging.info('connection from {} not allowed. blacklisted.'.format(addr[0]))
                        if addr not in self.clients:
                            self.disconnect_client(addr, None)
                        else:
                            self.disconnect_client(addr, self.clients[addr].socket)
            # close sockets of disconnected clients
            for addr, client in list(self.clients.items()):
                if client.last_seen <= time.time() - 2:
                    self.logging.debug('disconnected: {}'.format(addr))
                    self.disconnect_client(addr, client.socket)

    @classmethod
    def create_from_config(cls, logging, statistics, relay_config):
        return cls(
            logging=logging,
            statistics=statistics,
            relay_address=relay_config['relayAddress'],
            relay_port=relay_config['relayPort'],
            remote_address=relay_config['remoteAddress'],
            remote_port=relay_config['remotePort'],
            blacklist_file=relay_config['blacklist'],
            whitelist_file=relay_config['whitelist'],
        )
