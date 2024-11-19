###########################
# Piece and Piece Display #
###########################

# Format piece string representation
def b(p):
	return f"{p:04b}"

# Convert bit string to characters
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

# Display all characters within a zone
def dzone(z):
	return list(map(lambda x: dpiece(x) ,z))

# Filter None from a list of pieces
def pieceList(ps):
	return list(filter(lambda x: x is not None, ps))

##########################
# Comparing Piece Traits #
##########################

def comparePieces(b1:int ,b2:int):
	'''
	Compare to piece traits by their associated binary values

	Parameters:
	b1 (int): First piece
	b2 (int): Second piece

	Returns:
	int: A binary string representing which traits are shared, 1 for shared, 0 otherwise
	'''
	return ~(b1^b2) & 0b1111

def comparePieceList(bs: list[int]):
	'''
	Compare piece traits across list of pieces

	Parameters:
	bs (list[int]): A list of pieces

	Returns:
	int: A binary string representing which traits are shared, 1 for shared, 0 otherwise
	'''
	if len(bs) == 0: return 0b0000
	p = bs[0]
	s = 0b1111
	for b in bs[1:]:
		s &= comparePieces(p,b)
		p = b
	return s

def sharedTraits(bs: list[int]):
	'''
	Counts the number of shared traits for pieces in a list

	Parameters:
	bs (list[int]): A list of pieces

	Returns:
	int: A count of the number of shared traits across all pieces
	'''
	return bin(comparePieceList(bs)&0b1111).count('1')

###########################
# Convert Action Encoding #
###########################

def encodeAction(action):
	'''
	Encode an action, converting to an int

	Parameters:
	action ((int,int),int): An action

	Returns:
	int: The integer value of the encoded action
	'''
	loc, piece = action
	x,y = loc
	if piece is None:
		return x * 4 + y + 256
	return x * 4 * 16 + y * 16 + piece

def decodeAction(action):
	'''
	Decode an action, converting to a tuple

	Parameters:
	action (int): An integer representing an action

	Returns:
	((int,int),int): The associated action
	'''
	if action < 256:
		loc = action // 16
		piece = action % 16
		x,y = divmod(loc,4)
		return ((x,y),piece)
	else:
		action = action - 256
		x,y = divmod(action,4)
		return ((x,y),None)

#################
# Move Validity #
#################

def valid(loc,b: list[list[int]],p,ps):
	'''
	Returns the validity of an action

	Parameters:
	loc (int,int): The proposed location
	b (list[list[int]]): The board
	p (int): The proposed piece
	ps (list[int]): The list of available pieces

	Returns:
	bool: True if the action is valid, False otherwise
	'''
	x,y = loc

	if p is None:
		c = 0
		for row in b:
			c += row.count(None)
		if b[x][y] is None and c == 1:
			return True
		return False

	if (b[x][y] is None and ps[p] is not None):
		return True

	return False

def validPlace(loc,b):
	'''
	Returns the validity of a location

	Paremeters:
	loc (int,int): The proposed location
	b (list[list[int]]): The board

	Returns:
	bool: True if the action is valid, False otherwise
	'''
	x,y = loc
	if b[x][y] is None:
		return True
	return False

def validPiece(p, ps):
	'''
	Returns the validity of a piece

	Paremeters:
	p (int): The proposed piece
	ps (list[int]): The list of available pieces

	Returns:
	bool: True if the action is valid, False otherwise
	'''
	if p is None:
		return False
	if ps[p] is not None:
		return True
	return False