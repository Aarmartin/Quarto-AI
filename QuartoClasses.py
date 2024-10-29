from copy import deepcopy
from qutil import *
import random

###########
# Classes #
###########
	
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

		# Establish all board spaces
		self.spaces = [[None for _ in range(4)] for _ in range(4)]
		
		self.pieces = [i for i in range(16)]

		self.used = []

	def __str__(self):
		s = ""
		for r in self.spaces:
			s += f"{dpiece(r[0])} | {dpiece(r[1])} | {dpiece(r[2])} | {dpiece(r[3])}\n"
		return s
	
	def __repr__(self):
		s = ""
		for r in self.spaces:
			s += f"{dpiece(r[0])} | {dpiece(r[1])} | {dpiece(r[2])} | {dpiece(r[3])}\n"
		return s

	# Performs a single move on the board and updates availability accordingly
	def makeMove(self, piece: int, loc: tuple[int,int]):
		if self.spaces[loc[0]][loc[1]] is None and piece is not None and piece not in self.used:
			self.spaces[loc[0]][loc[1]] = piece
			self.pieces.remove(piece)
			self.used.append(piece)
		else:
			print("Illegal move attempted")

	# True if a zone on the current board contains a quarto
	def quarto(self):
		for zone in self.zones():
				if bcount(pieceList(zone)) == 4:
					return True	
		return False

	def boardUtil(self):
		
		total = 0

		for zone in self.zones():
			val = bcount(pieceList(zone))
			if val == 4:
				return 1000
			#elif val == 3:
			#	total += 10
			#elif val == 2:
			#	total += 5
		
		return 0
		
	def zones(self):
		l = len(self.spaces)

		# Rows
		z = self.spaces.copy()
		
		# Columns
		for i in range(l):
			z.append([row[i] for row in self.spaces])

		# Diagonals
		z.append([self.spaces[i][i] for i in range(l)])
		z.append([self.spaces[i][l-1-i] for i in range(l)])

		# Sub-squares
		if self.adv:
			for i in range(l-1):
				for j in range(l-1):
					z.append([self.spaces[i][j],self.spaces[i][j+1],self.spaces[i+1][j],self.spaces[i+1][j+1]])

		return z

	def isFull(self):
		if all(all((self.spaces[i][j] is not None) for j in range(len(self.spaces[i]))) for i in range(len(self.spaces))):
			return True
		return False
	
	def openSpaces(self):
		open = []
		for x in range(4):
			for y in range(4):
				if self.spaces[x,y] is None:
					open.append((x,y))
		return open

	def copy(self):

		bc = Board(self.adv)
		
		bc.pieces = self.pieces
		bc.used = self.used
		bc.spaces = self.spaces

		return bc
	
class State:

	def __init__(self, board: Board, player, nextPiece: int):
		
		self.board = board
		self.player = player
		self.nextPiece = nextPiece
		self.previousPiece = None
		self.previousLoc = None
	
	def quarto(self):
		return self.board.quarto()
	
	def dead(self):
		return self.board.isFull()
	
	def terminal(self):
		if self.dead() or self.quarto():
			return True
		return False
	
	def copy(self):
		return State(self.board, self.player, self.nextPiece)
	
	def move(self,loc,piece):
		self.board.makeMove(self.nextPiece,loc)
		self.previousPiece = self.nextPiece
		self.previousLoc = loc
		self.nextPiece = piece

	def placePiece(self,loc):
		print("Placing at:",loc)
		self.board.makeMove(self.nextPiece, loc)
		print(self.board)
		self.previousPiece = self.nextPiece
		self.previousLoc = loc
		self.nextPiece = None

	def choosePiece(self,piece):
		self.nextpiece = piece

	def lastMove(self):
		return self.previousPiece, self.previousLoc
	
	def successors(self) -> list['State']:

		successors = []

		for loc in self.board.openSpaces():
			for piece in self.board.pieces:
				if piece != self.nextPiece:
					s = self.copy()
					s.move(self.nextPiece, loc, piece)
					successors.append(s)

		return successors
	
	def utility(self):

		return self.board.boardUtil()
	

class Game:

	def __init__(self, adv, player):
		self.state = State(Board(adv),player,None)

	def randomPiece(self):
		self.state.nextPiece = random.randint(0,15)
		return dpiece(self.state.nextPiece)
	
	def badMove(self,move):
		if move is None or self.state.board.spaces[move[0]][move[1]] is not None:
			return True
		return False
	
	def badPiece(self,piece):
		if piece is None or piece in self.state.board.used:
			return True
		return False
	
	def getPiece(self,x,y):
		return dpiece(self.state.board.spaces[x][y])
	
	def place(self, loc):
		self.state.placePiece(loc)

	def choose(self, piece):
		self.state.choosePiece(piece)

	def won(self):
		return self.state.quarto()
	def finished(self):
		return self.state.dead()