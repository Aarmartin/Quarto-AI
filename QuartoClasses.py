from qutil import *
import numpy as np
import torch

###########
# Classes #
###########

class QuartoState:

	# Initialize
	# Board: 2D array populated with None
	# Pieces: List 0 through 15
	def __init__(self,training=False,rewardVal=1):
		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

		# Board state
		self.board = [[None for _ in range(4)] for _ in range(4)]	# Empty 2D 4x4 grid
		self.pieces = list(range(16))								# List of available pieces
		self.nextPiece = None										# Next piece to play
		self.done = False											# Is Terminal
		if training:
			self.movePickPiece(np.random.choice(self.pieces))
		self.rewardVal = rewardVal									# Optional win reward value

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
		'''
		Reset Quarto State to initial empty board
		'''
		self.board = [[None for _ in range(4)] for _ in range(4)]
		self.pieces = list(range(16))
		self.nextPiece = None
		self.done = False
		self.movePickPiece(np.random.choice(self.pieces))
		return self

	def terminal(self):
		'''
		Returns:
		bool: True if state is terminal, False otherwise
		'''
		if self.quarto() or self.draw():
			return True	# Terminal state found
		return False
	
	def quarto(self):
		'''
		Returns:
		bool: True if state contains a Quarto, False otherwise
		'''

		l = len(self.board)

		# Check Rows for winning lines
		for row in self.board:
			frow = pieceList(row)
			if len(frow) == 4 and sharedTraits(frow) > 0:
				return True

		# Check columns for winning lines
		for col in [[row[i] for row in self.board] for i in range(l)]:
			fcol = pieceList(col)
			if len(fcol) == 4 and sharedTraits(fcol) > 0:
				return True
		
		# Check diagonals for winning lines
		for diag in [[self.board[i][i] for i in range(l)],[self.board[i][l-i-1] for i in range(l)]]:
			fdiag = pieceList(diag)
			if len(fdiag) == 4 and sharedTraits(fdiag) > 0:
				return True
			
		return False

	def draw(self):
		'''
		Returns:
		bool: True if the board is a draw, False otherwise
		'''
		if all(all((self.board[i][j] is not None) for j in range(len(self.board[i]))) for i in range(len(self.board))) and not self.quarto():
			return True
		return False
	
	def move(self,loc,piece):
		'''
		Performs an action on the board. Chooses a location to place the current piece, and selects the next piece to be played.

		Parameters:
		loc (int,int): A tuple of the form (x,y), representing the location on the board
		piece (int): An integer representing a piece

		Returns:
		bool: True if board is terminal after moving piece
		'''
		x,y = loc
		self.board[x][y] = self.nextPiece	# Place piece on board
		self.nextPiece = piece				# Set next piece to chosen piece
		if piece is not None:
			self.pieces[piece] = None		# Remove from available pieces
		if self.quarto() or self.draw():
			self.done = True				# Check if now in terminal state
		return self.done

	def moveSetPiece(self,loc):
		'''
		Performs half of an action on the board, placing a piece on it
		
		Parameters:
		loc (int,int): A tuple of the form (x,y), representing the location on the board
		'''
		x,y = loc
		self.board[x][y] = self.nextPiece
		self.nextPiece = None

	# Pick Piece
	def movePickPiece(self,piece):
		'''
		Performs half of an action in the state, choosing the next piece to be played
		
		Parameters:
		piece (int): An integer representing a piece
		'''
		self.nextPiece = piece
		self.pieces[piece] = None

	def getBoard(self):
		'''
		Returns:
		list[list[int]]: A copy of the board
		'''
		return self.board
	
	def getNextPiece(self):
		'''
		Returns:
		int: A copt of the next piece
		'''
		return self.nextPiece
	
	def getPieces(self):
		'''
		Returns:
		list[int]: A list of available pieces
		'''
		return self.pieces

	@staticmethod
	def encodePiece(p):
		'''
		Encode and normalize a piece

		Parameters:
		p (int): A piece

		Returns:
		list[float]: A list with a single element, the normalized representation of a piece
		'''
		return [(p+1)/16 if p is not None else 0]
		#return [int(bit) for bit in f"{p:04b}"]
	
	@staticmethod
	def encodePieceList(ps):
		'''
		Encode list of available pieces

		Parameters:
		ps (list[int]): A list of pieces

		Returns:
		list[bool]: A list of booleans, 1 if piece is present, 0 otherwise
		'''
		seq = [0 for _ in range(16)]
		for piece in ps:
			if piece is not None:
				seq[piece] = 1
		return seq

	@staticmethod
	def encodeBoard(b: list[list[int]]):
		'''
		Encode the board

		Parameters:
		b (list[list[int]]): A representation of a board

		Returns:
		list[float]: A flattened vector of normalized board placements
		'''
		seq = []
		for row in b:
			for sp in row:
				if sp is not None:
					seq.append((sp + 1)/16)
				else:
					seq.append(0)
		return seq

	def encode(self):
		'''
		Encodes the current state

		Returns:
		Tensor: An encoded board vector
		Tensor: An encoded vector containing the next piece and the available piece list
		'''
		encodedBoard = self.encodeBoard(self.board)
		encodedNextPiece = self.encodePiece(self.nextPiece)
		encodedPieceList = self.encodePieceList(self.pieces)
		return torch.tensor(encodedBoard,dtype=torch.float,device=self.device), torch.tensor((encodedNextPiece + encodedPieceList),dtype=torch.float,device=self.device)

	def actions(self):
		'''
		Returns:
		list[(int,int),int]: A list of possible actions
		'''
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
	
	def step(self, action):
		'''
		Performs an action and calculates the reward and terminal status

		Parameters:
		action ((int,int),int): The action to be taken

		Returns:
		QuartoState: A reference to itself
		int: The reward for the action
		bool: The terminal status
		'''
		reward = 0
		loc,piece = action
		if valid(loc,self.board,piece,self.pieces):
			res = self.move(loc,piece)
			if res:
				if self.quarto():
					reward = self.rewardVal

		return self, reward, self.done