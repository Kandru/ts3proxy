import socket
import select


class weblist:

    def __init__(self, logging):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.remote_address = ('194.97.114.3', 2010)
        self.logging = logging
        self.server_name = "Inofficial Test Server Europe"
        self.server_port = 9987
        self.max_users = 100
        self.num_users = 50
        self.initial_packet()
        self.loop()

    def initial_packet(self):
        self.socket.sendto(b'\0x01\0x03\0x00\0x01', self.remote_address)
        print('sent packet')

    def loop(self):
        while True:
            readable, writable, exceptional = select.select([self.socket], [], [])
            for s in readable:
                data, addr = s.recvfrom(1024)
                packet = b'\0x01\0x04\0x00\0x02'
                print('data: ', data)
                authkey = data[4] + data[5] + data[6] + data[7]
                packet = packet + authkey
                print('authkey: ', authkey)
