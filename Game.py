from QuartoClasses import QuartoState
from ComputerAgent import Computer
from qutil import *
import random

class Game:
	def __init__(self,adv=False):
		self.state = QuartoState()
		self.computer = Computer("comp.model")
		self.player = "Computer"
	
	def setPlayer(self, player):
		self.player = player
		if player == "Computer":
			self.state.setPlayer(1)
		else:
			self.state.setPlayer(-1)

	def setFirstPiece(self,piece=None,rand=False):
		if rand:
			self.state.setNext(random.choice(self.state.pieces))
		else:
			self.state.setNext(piece)
		return self.state.nextPiece

	def playerPlace(self,loc):
		self.state.moveSetPiece(loc)

	def playerPick(self,piece):
		self.state.movePickPiece(piece)

	def computerTurn(self):
		loc, piece = self.computer.play(self.state)
		self.state.move(loc,piece)
		self.player = "Player"

	def badMove(self,loc):
		return not validPlace(loc,self.state.board)
	
	def badPiece(self,piece):
		return not validPiece(piece,self.state.pieces)
	
	def getPiece(self,loc):
		x,y = loc
		return self.state.board[x][y]

	def finished(self):
		if self.state.quarto() or self.state.isDraw(): return True
		return False
	
	def won(self):
		if self.state.quarto(): return True
		return False