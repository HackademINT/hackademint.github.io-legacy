#! /usr/bin/env python3
def are_same(serial):
	if (serial[0] != serial[1] and
		serial[1] != serial[2] and
		serial[0] != serial[2]):
		return False
	return True

def check_serial(serial):
	try:
		serials = serial.split('-')
	except:
		return False

	if len(serials) != 3:
		return False
	try:
		X = [ord(a) for a in list(serials[0])]
		Y = [ord(a) for a in list(serials[1])]
		Z = int(serials[2])
	except ValueError:
		return False
	except:
		return False

	if not len(X) == 3 or not len(Y) == 3:
		return False
	for a in X+Y:
		if a < 65 or a > 90:
			return False
	if are_same(X) or are_same(Y):
		return False
	if X[1] + 10 > X[2]:
		return False
	if Y[1] - 10 < Y[2]:
		return False
	sum1 = X[0] + X[1] + X[2]
	sum2 = Y[0] + Y[1] + Y[2]
	if sum1 == sum2:
		return False
	if sum1+sum2 != Z:
		return False
	if Z % 3 != 0:
		return False
	return True
