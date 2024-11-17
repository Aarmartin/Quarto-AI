from qutil import *
import numpy as np
import torch

###########
# Classes #
###########
'''
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
				if maxShareCount(pieceList(zone)) == 4:
					return True	
		return False

	def boardUtil(self):
		
		total = 0

		for zone in self.zones():
			val = maxShareCount(pieceList(zone))
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
'''

class QuartoState:

	# Initialize
	# Board: 2D array populated with None
	# Pieces: List 0 through 15
	def __init__(self, adv=False, setFirst=False):
		self.board = [[None for _ in range(4)] for _ in range(4)]
		self.pieces = list(range(16))
		self.nextPiece = None
		self.player = 1
		self.adv = adv
		self.boardVal = None
		if setFirst:
			self.setNext(np.random.choice(self.pieces))

	def __str__(self):
		s = ""
		for r in self.board:
			s += f"{dpiece(r[0])} | {dpiece(r[1])} | {dpiece(r[2])} | {dpiece(r[3])}\n"
		return s
	
	def __repr__(self):
		s = ""
		for r in self.board:
			s += f"{dpiece(r[0])} | {dpiece(r[1])} | {dpiece(r[2])} | {dpiece(r[3])}\n"
		return s

	def reset(self):
		self.board = [[None for _ in range(4)] for _ in range(4)]
		self.pieces = list(range(16))
		self.setNext(np.random.choice(self.pieces))
		self.player = 1
		self.boardVal = None
		return self

	# Is State Terminal
	def terminal(self):
		if self.quarto() or self.isDraw():
			return True
		return False
	
	# Make a move on the board
	def move(self,loc,piece):
		x,y = loc
		self.board[x][y] = self.nextPiece
		self.nextPiece = piece
		if piece is not None:
			self.pieces[piece] = None
		self.player = self.player * -1
		self.updateStateValue()

	def moveSetPiece(self,loc):
		x,y = loc
		self.board[x][y] = self.nextPiece
		self.nextPiece = None
		self.updateStateValue()

	def movePickPiece(self,piece):
		self.nextPiece = piece
		self.pieces[piece] = None
		self.player = self.player * -1
		self.updateStateValue()

	# Manually select next piece
	def setNext(self,piece):
		self.nextPiece = piece
		self.pieces[piece] = None

	def setPlayer(self,player):
		self.player = player

	def getBoard(self):
		return self.board
	
	def getNextPiece(self):
		return self.nextPiece
	
	def getPieces(self):
		return self.pieces

	def encode(self):
		return getEncode(self.board,self.nextPiece,self.pieces,self.player)

	# Set of all possible actions
	def actions(self):
		l = len(self.board)
		a = []
		for x in range(l):
			for y in range(l):
				for p in pieceList(self.pieces):
					if self.board[x][y] is None:
						a.append(((x,y),p))
		if not a:
			for x, row in enumerate(self.board):
				for y, val in enumerate(row):
					if val is None:
						a.append(((x,y),None))
		return a
	
	# Reward value for state
	# Quarto results in -1000 (if quarto and you're turn, you didn't place the winning piece)
	# Draw results in 0
	# Board value favors pieces on the board
	def reward(self):
		if self.quarto(): return -1000 * self.player
		if self.isDraw(): return 0
		return self.getBoardValue()
	
	# Get Board Value
	def getBoardValue(self):
		if self.boardVal is None:
			self.boardVal = boardValue(self.board,self.adv) * self.player
		return self.boardVal
	
	def updateStateValue(self):
		value = boardValue(self.board)
		if value == 1000:
			value *= self.player * -1
		self.boardVal = value
	
	def step(self, action):
		loc,piece = action
		if valid(loc,self.board,piece,self.pieces):
			if loc is None:
				loc = finalPlace(self.board)
			self.move(loc,piece)
			return self, self.getBoardValue(),self.terminal()
	
	# Get Quarto Status
	def quarto(self):
		if abs(self.getBoardValue()) == 1000:
			return True
		return False
	
	# Get Draw Status
	def isDraw(self):
		if all(all((self.board[i][j] is not None) for j in range(len(self.board[i]))) for i in range(len(self.board))) and not self.quarto():
			return True
		return False
'''
class OldState:

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
'''