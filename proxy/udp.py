import time
import socket
import threading

class udp():
	def __init__(self, relayPort, remoteAddr, remotePort):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(("0.0.0.0", relayPort))
		self.remoteAddr = remoteAddr
		self.remotePort = remotePort
		self.clientList = dict()
		t = threading.Thread(target = self.getFromServer)
		t.start()
		t2 = threading.Thread(target = self.proofClientTimeout)
		t2.start()

	def getFromServer(self):
		while True:
			# send data from remote server to specific client
			for key in list(self.clientList):
				try:
					data, addr = self.clientList[key]['socket'].recvfrom(1024)
					self.clientList[key]['lastseen'] = time.time()
					self.socket.sendto(data, key)
				except:
					pass
			time.sleep(.05)

	def proofClientTimeout(self):
		while True:
			# check for timeout
			for key in list(self.clientList):
				if self.clientList[key]['lastseen'] < time.time() -2:
					print('disconnected: ' + str(key))
					del self.clientList[key]
			time.sleep(1)

	def relay(self):
		while True:
			# get data from an connected client
			data, addr = self.socket.recvfrom(1024)
			# if we see the client the first time
			if not addr in self.clientList:
				print('connected: ' + str(addr))
				self.clientList[addr] = {
					'socket': socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
					'lastseen': time.time()
				}
				self.clientList[addr]['socket'].setblocking(0)
			self.clientList[addr]['socket'].sendto(data, (self.remoteAddr, self.remotePort))
