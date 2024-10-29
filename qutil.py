##########
# Pieces #
##########

def b(p):
	return f"{p:04b}"

def dpiece(p):
	if p is not None:
		s = b(p)
		t = ""
		if s[0] == '0':
			t = t + 'T'
		else:
			t = t + 'S'

		if s[1] == '0':
			t = t + 'L'
		else:
			t = t + 'D'
		
		if s[2] == '0':
			t = t + 'S'
		else:
			t = t + 'C'

		if s[3] == '0':
			t = t + 'S'
		else:
			t = t + 'H'

		return t
	return None

def dzone(z):
	return list(map(lambda x: dpiece(x) ,z))

def pieceList(ps):
	return list(filter(lambda x: x is not None, ps))

##########################
# Comparing Piece Traits #
##########################

def comp(b1:int ,b2:int):
	return ~(b1^b2) & 0b1111

def compZone(bs: list[int]):
	p = bs[0]
	s = 0b1111
	for b in bs[1:]:
		s &= comp(p,b)
		p = b
	return s

def sharedTraits(bs: list[int]):
	return bin(compZone(bs)&0b1111).count('1')

#########################
# Counting Piece Traits #
#########################

def bcount(ps):
	
	m = 0

	for i in range(4):
		z = sum(1 for bs in ps if not (bs & (1 << i)))
		o = sum(1 for bs in ps if (bs & (1 << i)))

		m = max(m,z,o)

	return m

__all__ = ['sharedTraits','pieceList','dpiece','dzone','bcount']