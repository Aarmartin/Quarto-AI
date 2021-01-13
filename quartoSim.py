

################
# Base Classes #
################

class Board:

	# Create board
	# Game mode Normal or Advanced
	# Initial win state is false
	# List of all of the possible board spaces
	# Initial open spaces is all spaces
	# Initial occupied spaces is none
	# Establish win zones (Rows, Columns, and Diags if Normal, include 2x2 squares if advaced)
	# Create 16 pieces associated with the board
	def __init__(self, adv):

		# Board specification if it is advanced or not
		self.adv = adv

		# Winning status of board
		self.win = False

		# Establish all board spaces
		self.spaces = []

		for i, row in enumerate(list('1234')):
			for j, col in enumerate(list('abcd')):
				self.spaces.append(row+col)

		# Initial open spaces are all spaces
		self.open = self.spaces

		# Dictionary of occupied spaces
		self.occupied = {}

		# Different win zones to check
		self.zones = []

		self.zones.append([ '1a', '1b', '1c', '1d' ])
		self.zones.append([ '2a', '2b', '2c', '2d' ])
		self.zones.append([ '3a', '3b', '3c', '3d' ])
		self.zones.append([ '4a', '4b', '4c', '4d' ])
		self.zones.append([ '1a', '2a', '3a', '4a' ])
		self.zones.append([ '1b', '2b', '3b', '4b' ])
		self.zones.append([ '1b', '2c', '3c', '4c' ])
		self.zones.append([ '1d', '2d', '3d', '4d' ])
		self.zones.append([ '1a', '2b', '3c', '4d' ])
		self.zones.append([ '4a', '3b', '2c', '1d' ])

		if adv:
			self.zones.append([ '1a', '1b', '2a', '2b' ])
			self.zones.append([ '1b', '1c', '2b', '2c' ])
			self.zones.append([ '1c', '1d', '2c', '2d' ])
			self.zones.append([ '2a', '2b', '3a', '3b' ])
			self.zones.append([ '2b', '2c', '3b', '3c' ])
			self.zones.append([ '2c', '2d', '3c', '3d' ])
			self.zones.append([ '3a', '3b', '4a', '4b' ])
			self.zones.append([ '3b', '3c', '4b', '4c' ])
			self.zones.append([ '3c', '3d', '4c', '4d' ])

		self.pieces = [
			Piece("Tall", "Light", "Square", "Solid"),
			Piece("Tall", "Light", "Square", "Hollow"),
			Piece("Tall", "Light", "Circle", "Solid"),
			Piece("Tall", "Light", "Circle", "Hollow"),
			Piece("Tall", "Dark", "Square", "Solid"),
			Piece("Tall", "Dark", "Square", "Hollow"),
			Piece("Tall", "Dark", "Circle", "Solid"),
			Piece("Tall", "Dark", "Circle", "Hollow"),
			Piece("Short", "Light", "Square", "Solid"),
			Piece("Short", "Light", "Square", "Hollow"),
			Piece("Short", "Light", "Circle", "Solid"),
			Piece("Short", "Light", "Circle", "Hollow"),
			Piece("Short", "Dark", "Square", "Solid"),
			Piece("Short", "Dark", "Square", "Hollow"),
			Piece("Short", "Dark", "Circle", "Solid"),
			Piece("Short", "Dark", "Circle", "Hollow")
		]

	def make_move(self, piece, loc):
		if loc in self.open and piece not in self.occupied.values():
			self.occupied[loc] = piece
			self.open.remove(loc)
			print("Successful move")
		else:
			print("Illegal move attempted")

	def quarto(self):

		print("Checking Zones")
		for zone in self.zones:
			if set(zone).issubset(set(self.occupied.keys())):
				if bool(set(self.occupied[zone[0]].properties()) & set(self.occupied[zone[1]].properties()) & set(self.occupied[zone[2]].properties()) & set(self.occupied[zone[3]].properties())):
					self.win = True
		print("Zones Checked")
		return self.win

	def currentUtil(self, turn):
		if self.quarto and turn == 'Player':
			return 1
		elif self.quarto and turn == 'Computer':
			return -1
		else:
			return 0

	def printBoard(self):
		print(self.win)
		print(self.open)

class Piece:

	def __init__(self, height, color, shape, fill):

		self.height = height
		self.color = color
		self.shape = shape
		self.fill = fill
		self.winning = False

	def properties(self):
		return [ self.height, self.color, self.shape, self.fill ]

class State:
	def __init__(self, turn, util, board, moves, winning_move=None):
		self.turn = turn
		self.util = util
		self.board = board
		self.moves = moves
		self.winning_move = winning_move

	def printState(self):
		print("Current turn is:", self.turn)
		print("Current available moves are:", self.moves)

################
# Game Testing #
################

board = Board(True)
board.make_move(board.pieces[0], '1a')
board.make_move(board.pieces[1], '1b')
board.make_move(board.pieces[2], '1c')
board.make_move(board.pieces[15], '1d')
board.quarto()
print(board.win)
#board.printBoard()

begin = State('Player', board.currentUtil('Player'), board, board.open)

begin.printState()
