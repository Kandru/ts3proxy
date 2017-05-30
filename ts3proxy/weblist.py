import select
import socket
import struct
import threading
import time


class Weblist:

    def __init__(self, logging, statistics, server_name, server_port, max_users):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.remote_address = ('194.97.114.3', 2010)
        self.logging = logging
        self.statistics = statistics
        self.server_name = server_name
        self.server_port = server_port
        self.max_users = max_users
        self.timestamp = 0

        self.thread = None
        self.run_loop = True

    def initial_packet(self):
        self.socket.sendto(bytes.fromhex('01 03 00 01'), self.remote_address)
        self.timestamp = time.time()
        self.logging.debug('weblist packet successfully sent')

    def start_thread(self):
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop_thread(self):
        self.run_loop = False
        # close the socket so that select returns
        self.socket.close()

    def loop(self):
        self.initial_packet()
        while True:
            readable, writable, exceptional = select.select([self.socket], [], [], 2)
            if not self.run_loop:
                # stop thread
                break
            for s in readable:
                data, addr = s.recvfrom(1024)
                if data[0:4] == bytes.fromhex('01 03 00 01'):
                    packet = bytes.fromhex('01 04 00 02')
                    auth_key = bytes(data[4:5] + data[5:6] + data[6:7] + data[7:8])
                    packet = packet + struct.pack(
                        "<4shhhbb",
                        auth_key,
                        self.server_port,
                        self.max_users,
                        int(self.statistics.num_users),
                        int('00000010', 2),
                        len(self.server_name)
                    )
                    packet = packet + self.server_name.encode('utf-8')
                    self.socket.sendto(packet, self.remote_address)
                elif data[4:5] == bytes.fromhex('00'):
                    self.logging.debug('weblist entry updated successfull')
                elif data[4:5] == bytes.fromhex('01'):
                    self.logging.debug('weblist entry reported wrong data')
                elif data[4:5] == bytes.fromhex('05'):
                    self.logging.debug('weblist entry spam protection')
                elif data[4:5] == bytes.fromhex('07'):
                    self.logging.debug('weblist server forgot me')
                else:
                    self.logging.debug('weblist got an unknown answer')
            if self.timestamp < time.time() - 600:
                self.initial_packet()
