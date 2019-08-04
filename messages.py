#!/usr/bin/env python

import socket
import argparse
import time
import json
import random

receiveSocket = None

# Message Types:
#	0 - Done with setup
#	1 - Shooting at location
#	2 - You hit location
#	3 - You missed location
#	4 - You win
#	5 - I give up
class message:
	def __init__(self, type=-1, x=-1, y=-1):
		self.type = type
		self.x = x
		self.y = y 

	def __str__(self):
		r = ''
		r += 'Type: %d, x: %d, y: %d' % (self.type, self.x, self.y)
		return(r)

class receiver:
	def __init__(self, addr, port):
		self.receiveAddr = addr
		self.receivePort = int(port)
		self.receiveSocket = socket.socket(socket.AF_INET,
						socket.SOCK_DGRAM)
		self.receiveSocket.bind((self.receiveAddr,
					 self.receivePort))
		self.receiveSocket.setblocking(0)
		return

	def receivePoll(self):
		try:
			data,addr = self.receiveSocket.recvfrom(2048)
			print('received message: ', data)
			m = message()
			m.__dict__ = json.loads(data)
			return m
		except:
			print('no message received')
			return None

class sender:
	def __init__(self, addr, port):
		self.sendAddr = addr
		self.sendPort = int(port)
		self.sendSocket = socket.socket(socket.AF_INET,
						socket.SOCK_DGRAM)
	
	def sendMessage(self, mtype, x=-1, y=-1):
		print("IN SEND MTPYE = {} X = {} y = {}".format(mtype, x,y))
		m = message(mtype, x, y)
		tmp = json.dumps(m.__dict__)
		print("TMP IS {}".format(tmp))
		self.sendSocket.sendto(tmp, (self.sendAddr, self.sendPort))

def test1():
	a = message(1, 3,4)
	print(a)
	b = json.dumps(a.__dict__)
	print(b)

def main():
	ADDR='0.0.0.0'
	PORT=9965

	parser = argparse.ArgumentParser('BPBattleship')
	parser.add_argument('-a', '--receiveAddr',  default='0.0.0.0')
	parser.add_argument('-p', '--receivePort',  default='9968')
	parser.add_argument('-A', '--sendToAddr', default='127.0.0.1')
	parser.add_argument('-P', '--sendToPort', default='9968')

	args = parser.parse_args()

	r = receiver(args.receiveAddr, args.receivePort)
	s = sender(args.sendToAddr, args.sendToPort)

	print('starting loop.')
	while True:
		r.receivePoll()
		time.sleep(1)

	return

if __name__=='__main__':
	main()

