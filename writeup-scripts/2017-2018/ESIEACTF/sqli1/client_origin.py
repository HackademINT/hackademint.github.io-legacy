
#encoding: utf-8

import socket
import sys

# change this if needed
HOST = '192.168.1.73'
# change this if needed
IP   = 8095


def create_socket():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		s.connect((HOST,IP))
	except Exception as e:
		print("Can't open socket !")
		print(e)
		sys.exit(1)
	return s


def test_level1():
	print("[+] Test level1 ...")
	s = create_socket()

	login = "toto"
	password = "toto"
	cmd = "\x01%s\x00%s" % (login,password)
	s.send(cmd.encode('utf-8'))
	msg = s.recv(1024)
	if msg and msg.decode('utf-8').startswith("Welcome"):
		print(msg.decode('utf-8'))
		res = s.recv(1024)
		print(res.decode('utf-8'))
	else:
		print("If you called a valid level, notice an admin")
	s.close()

def test_level2():
	print("[+] Test level2 ...")
	s = create_socket()

	citation = 1
	s.send(b"\x02%d" % citation)
	msg = s.recv(1024)
	if msg and msg.decode('utf-8').startswith("Welcome"):
		print(msg.decode('utf-8'))
		res = s.recv(1024)
		print(res.decode('utf-8'))
	else:
		print("If you called a valid level, notice an admin")
	s.close()


if __name__ == '__main__':
	test_level1()
	print("")
	test_level2()
