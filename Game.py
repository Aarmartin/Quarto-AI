from QuartoClasses import QuartoState
from ComputerAgent import Computer
from qutil import *
import random

class Game:
	def __init__(self, model=""):
		self.state = QuartoState()
		print("Loading model:",model)
		self.computer = Computer(model)

	def setFirstPiece(self,piece=None,rand=False):
		'''
		Selects the first piece of the game

		Parameters:
		piece (int): The chosen piece

		Returns:
		int: The piece
		'''
		if rand:
			self.state.movePickPiece(random.choice(self.state.pieces))
		else:
			self.state.movePickPiece(piece)
		return self.state.nextPiece

	def playerPlace(self,loc):
		'''
		Player method for placing a piece on the board

		Parameters:
		loc ((int,int)): A board location
		'''
		self.state.moveSetPiece(loc)

	def playerPick(self,piece):
		'''
		Player method for choosing a piece for opponent

		Parameters:
		piece (int): A chosen piece
		'''
		self.state.movePickPiece(piece)

	def computerTurn(self):
		'''
		Computer player method for performing action
		'''
		loc, piece = self.computer.play(self.state)
		self.state.move(loc,piece)

	def badMove(self,loc):
		'''
		Parameters:
		loc ((int,int)): Location on the board

		Returns:
		bool: True if the location is invalid, False otherwise
		'''
		if loc is None: return True
		return not validPlace(loc,self.state.board)
	
	def badPiece(self,piece):
		'''
		Parameters:
		piece (int): A chosen piece

		Returns:
		bool: True if the piece is invalid, False otherwise
		'''
		if piece is None: return True
		return not validPiece(piece,self.state.pieces)
	
	def getPiece(self,loc):
		'''
		Parameters:
		loc ((int,int)): A location on the board

		Returns:
		int: The piece at that location
		'''
		x,y = loc
		return self.state.board[x][y]

	def finished(self):
		'''
		Returns:
		bool: True if the game is finished, False otherwise
		'''
		if self.state.quarto() or self.state.draw(): return True
		return False
	
	def won(self):
		'''
		Returns:
		bool: True if the game is won, False otherwise
		'''
		if self.state.quarto(): return True
		return False