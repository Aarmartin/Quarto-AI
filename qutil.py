import torch

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

def compare(b1:int ,b2:int):
	return ~(b1^b2) & 0b1111

def comparePieces(bs: list[int]):
	if len(bs) == 0: return 0b0000
	p = bs[0]
	s = 0b1111
	for b in bs[1:]:
		s &= compare(p,b)
		p = b
	return s

def sharedTraits(bs: list[int]):
	return bin(comparePieces(bs)&0b1111).count('1')

#########################
# Counting Piece Traits #
#########################

# Maximum number of pieces with a shared trait
def maxShareCount(ps):
	
	m = 0

	for i in range(4):
		z = sum(1 for bs in ps if not (bs & (1 << i)))
		o = sum(1 for bs in ps if (bs & (1 << i)))

		m = max(m,z,o)

	return m

########################
# GUI Helper Functions #
########################



########################
# Board Util Functions #
########################

def boardValue(b, adv=False):
	l = len(b)
	s = 0

	for row in b:
		pl = pieceList(row)
		if sharedTraits(pl) > 0:
			if len(pl) == 4:
				return 1000
			elif len(pl) == 3:
				s += 10
			elif len(pl) == 2:
				s += 5

	for col in [[row[i] for row in b] for i in range(l)]:
		pl = pieceList(col)
		if sharedTraits(pl) > 0:
			if len(pl) == 4:
				return 1000
			elif len(pl) == 3:
				s += 10
			elif len(pl) == 2:
				s += 5

	for diag in [[b[i][i] for i in range(l)],[b[i][i-1] for i in range(l)]]:
		pl = pieceList(diag)
		if sharedTraits(pl) > 0:
			if len(pl) == 4:
				return 1000
			elif len(pl) == 3:
				s += 10
			elif len(pl) == 2:
				s += 5

	if adv:
		for i in range(l-1):
			for j in range(l-1):
				pl = pieceList(b[i][j],b[i][j+1],b[i+1][j],b[i+1][j+1])
				if sharedTraits(pl) > 0:
					if len(pl) == 4:
						return -1000
					elif len(pl) == 3:
						s += 10
					elif len(pl) == 2:
						s += 5

	return s

def finalPlace(b):
	loc = None
	for x, row in enumerate(b):
		for y, val in enumerate(row):
			if val is None and loc is None:
				loc = (x,y)
			elif val is None and loc is not None:
				return
	return loc

def getPieceEncode(p):
	return [int(bit) for bit in f"{p:04b}"]

def getEncode(b,p,ps,player) -> torch.FloatTensor:
	boardEncode = []

	if player > 0:
		boardEncode.extend([1])
	else:
		boardEncode.extend([0])

	for row in b:
		for piece in row:
			if piece is None:
				boardEncode.extend([0,0,0,0,0])
			else:
				boardEncode.extend([1] + getPieceEncode(piece))

	if p is not None:
		boardEncode.extend(getPieceEncode(p))
	else:
		boardEncode.extend([0,0,0,0])

	for piece in ps:
		if piece is None:
			boardEncode.extend([0])
		else:
			boardEncode.extend([1])

	return torch.FloatTensor(boardEncode)

def encodeAction(action):
	(loc, piece) = action
	if loc is None or piece is None:
		return 256
	x,y = loc
	return x * 4 * 16 + y * 16 + piece

def decodeAction(action):
	if action == 256:
		return (None,None)
	loc = action // 16
	piece = action % 16
	x,y = divmod(loc,4)
	return ((x,y),piece)

def valid(loc,b,p,ps):
	if loc is None:
		loc = finalPlace(b)
	if loc is None:
		return False
	x,y = loc

	if p is None and pieceList(ps):
		return False

	if (b[x][y] is None and p is None and not pieceList(ps)) or (b[x][y] is None and ps[p] is not None):
		return True

	return False

def validPlace(loc,b):
	if loc is None:
		return False
	x,y = loc
	if b[x][y] is None:
		return True
	return False

def validPiece(p, ps):
	if p is None:
		return False
	if ps[p] is not None:
		return True
	return False

__all__ = ['getEncode','encodeAction','decodeAction','boardValue','sharedTraits','pieceList','dpiece','dzone','maxShareCount','valid','validPlace','validPiece','finalPlace']