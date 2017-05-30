import socket
import sys
import select
import struct


class weblist:

    def __init__(self, logging):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.remote_address = ('194.97.114.3', 2010)
        self.logging = logging
        self.server_name = "dies ist ein test123"
        self.server_port = 9988
        self.max_users = 100
        self.num_users = 50
        self.initial_packet()
        self.loop()

    def initial_packet(self):
        self.socket.sendto(bytes.fromhex('01 03 00 01'), self.remote_address)
        print('sent packet')

    def loop(self):
        while True:
            readable, writable, exceptional = select.select([self.socket], [], [])
            for s in readable:
                data, addr = s.recvfrom(1024)
                print('data: ', data)
                if data[0:4] == bytes.fromhex('01 03 00 01'):
                    packet = bytes.fromhex('01 04 00 02')
                    auth_key = bytes(data[4:5] + data[5:6] + data[6:7] + data[7:8])
                    packet = packet + struct.pack(
                        "!4shhhbh",
                        auth_key,
                        self.server_port,
                        self.max_users,
                        self.num_users,
                        int('00000010', 2),
                        sys.getsizeof(self.server_name)
                    )
                    packet = packet + self.server_name.encode('utf-8')
                    print('send: ', packet)
                    self.socket.sendto(packet, self.remote_address)
                elif data[4:5] == bytes.fromhex('00'):
                    print('successfull')
                elif data[4:5] == bytes.fromhex('01'):
                    print('wrong data')
                elif data[4:5] == bytes.fromhex('05'):
                    print('spam protection')
                elif data[4:5] == bytes.fromhex('07'):
                    print('serverlist forgot me')
                else:
                    print('unknown answer')
