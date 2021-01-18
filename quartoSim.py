from tkinter import *
from copy import deepcopy
import random

from pip._vendor.distlib.compat import raw_input

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
		self.open = self.spaces.copy()

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
			Piece("Tall", "Light", "Square", "Solid", 0),
			Piece("Tall", "Light", "Square", "Hollow", 1),
			Piece("Tall", "Light", "Circle", "Solid", 2),
			Piece("Tall", "Light", "Circle", "Hollow", 3),
			Piece("Tall", "Dark", "Square", "Solid", 4),
			Piece("Tall", "Dark", "Square", "Hollow", 5),
			Piece("Tall", "Dark", "Circle", "Solid", 6),
			Piece("Tall", "Dark", "Circle", "Hollow", 7),
			Piece("Short", "Light", "Square", "Solid", 8),
			Piece("Short", "Light", "Square", "Hollow", 9),
			Piece("Short", "Light", "Circle", "Solid", 10),
			Piece("Short", "Light", "Circle", "Hollow", 11),
			Piece("Short", "Dark", "Square", "Solid", 12),
			Piece("Short", "Dark", "Square", "Hollow", 13),
			Piece("Short", "Dark", "Circle", "Solid", 14),
			Piece("Short", "Dark", "Circle", "Hollow", 15)
		]

		self.leftover = self.pieces.copy()

		self.lastPiece = None
		self.lastLoc = None

	# Performs a single move on the board and updates availability accordingly
	def make_move(self, piece, loc):
		if loc in self.open and piece not in self.occupied.values():
			self.occupied[loc] = piece
			self.open.remove(loc)
			self.leftover.remove(piece)
			print("Successful move")
			self.last = piece
		else:
			print("Illegal move attempted")

	# True if a zone on the current board contains a quarto, False if not,  updates wind status
	def quarto(self):

		print("Checking Zones")
		for zone in self.zones:
			if set(zone).issubset(set(self.occupied.keys())):
				if bool(set(self.occupied[zone[0]].properties()) & set(self.occupied[zone[1]].properties()) & set(self.occupied[zone[2]].properties()) & set(self.occupied[zone[3]].properties())):
					self.win = True
		print("Zones Checked")
		return self.win

	# Provides utility of current board
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

	# Created piece and each of its traits, as well as a reference id
	def __init__(self, height, color, shape, fill, pid):

		self.height = height
		self.color = color
		self.shape = shape
		self.fill = fill
		self.winning = False
		self.id = pid

		# Tag for text referencing
		self.tag = self.height[:1] + self.color[:1] + self.shape[:1] + self.fill[:1]

	def properties(self):
		return [ self.height, self.color, self.shape, self.fill ]

class State:

	# Current state of the game
	# Whos turn it is
	# Current utility of the state
	# The board object as a whole
	# A list of all of the open locations on the current board
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

#board = Board(True)
#board.make_move(board.pieces[0], '1a')
#board.make_move(board.pieces[1], '1b')
#board.make_move(board.pieces[2], '1c')
#board.make_move(board.pieces[4], '1d')
#board.quarto()
#print(board.win)
#board.printBoard()

#begin = State('Player', board.currentUtil('Player'), board, board.open)

#begin.printState()


###################
# DECISION MAKING #
###################

def randomPlacement(state):

	return random.choice(state.board.open)

def randomPiece(state):

	return random.choice(state.board.leftover)


def firstPlacement(state):

	return state.board.open[0]

def firstPiece(state):

	return state.board.leftover[0]


def alphabeta_cutoff(state, d=4, eval_fn=None):

	player = state.turn

	eval_fn = eval_fn or (lambda state: state.board.currentUtility(player))

	successors = []

	for move in state.moves:
		s = deepcopy(state)
		for piece in s.board.leftover:
			sp =  deepcopy(s)
			sp.board.make_move(move, piece)
			successors.append(sp)

	return random.choice(successors).board.lastLoc

#######
# GUI #
#######

class gameGUI:

	def __init__(self, title="Quarto", geometry="800x500"):

		board = Board(True)
		self.currentState = State('Player', 0, board, board.open)

		# Env
		self.root  = Tk()
		self.root.title(title)
		self.root.geometry( geometry )

		# Canvas
		self.canvas = Canvas( self.root, width=500, height=500)
		self.canvas.place(x=0,y=0)

		# Mouse control
		self.canvas.bind("<Button-1>", self.click)
		self.waiting = BooleanVar()
		self.waiting.set(1)
		self.buttonPressed = BooleanVar()
		self.buttonPressed.set(0)
		self.move = None


		# Initial Frame
		self.control = Frame(self.root)
		self.control.place(x=510, y=10)

		# Button Frame
		self.controlB = Frame(self.control, height=2, bd=1, relief=SUNKEN)
		self.controlB.pack(side = LEFT, fill=X, padx=5, pady=5)

		# Misc Frame
		self.controlM = Frame(self.control, height=2, bd=1, relief=SUNKEN)
		self.controlM.pack(side= RIGHT, fill=X, padx=5, pady=5)

		# Piece Buttons
		self.buttons = []

		print("Creating Buttons...")

		self.buttons.append(Button(self.controlB, text="TLSS", command = lambda: self.setSelect(board.pieces[0])))
		self.buttons.append(Button(self.controlB, text="TLSH", command = lambda: self.setSelect(board.pieces[1])))
		self.buttons.append(Button(self.controlB, text="TLCS", command = lambda: self.setSelect(board.pieces[2])))
		self.buttons.append(Button(self.controlB, text="TLCH", command = lambda: self.setSelect(board.pieces[3])))
		self.buttons.append(Button(self.controlB, text="TDSS", command = lambda: self.setSelect(board.pieces[4])))
		self.buttons.append(Button(self.controlB, text="TDSH", command = lambda: self.setSelect(board.pieces[5])))
		self.buttons.append(Button(self.controlB, text="TDCS", command = lambda: self.setSelect(board.pieces[6])))
		self.buttons.append(Button(self.controlB, text="TDCH", command = lambda: self.setSelect(board.pieces[7])))
		self.buttons.append(Button(self.controlB, text="SLSS", command = lambda: self.setSelect(board.pieces[8])))
		self.buttons.append(Button(self.controlB, text="SLSH", command = lambda: self.setSelect(board.pieces[9])))
		self.buttons.append(Button(self.controlB, text="SLCS", command = lambda: self.setSelect(board.pieces[10])))
		self.buttons.append(Button(self.controlB, text="SLCH", command = lambda: self.setSelect(board.pieces[11])))
		self.buttons.append(Button(self.controlB, text="SDSS", command = lambda: self.setSelect(board.pieces[12])))
		self.buttons.append(Button(self.controlB, text="SDSH", command = lambda: self.setSelect(board.pieces[13])))
		self.buttons.append(Button(self.controlB, text="SDCS", command = lambda: self.setSelect(board.pieces[14])))
		self.buttons.append(Button(self.controlB, text="SDCH", command = lambda: self.setSelect(board.pieces[15])))
	
		for button in self.buttons:
			button.pack(anchor=W, fill=X)

		# Exit Button
		Button(self.controlM, text="Exit", command=self.exit).pack(fill=X, side="right")

		# Current piece to play Label
		self.p = StringVar()
		self.p.set("Piece")
		Label(self.controlM, width=13, textvariable=self.p).pack(side="right")

		# Draw Board
		self.draw()

		# Begin the game
		self.play()

	# Player selected piece for computer to play
	def setSelect(self, piece):
		self.selected = piece
		self.buttonPressed.set(1)
		print("Current Selection is now:", self.selected.tag)

	# Draws entire contents of current board
	def draw(self, content=False):
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(0,i,500,i)
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(i,0,i,500)

		if content:
			for x, row in zip(range(4), ['1', '2', '3', '4']):
				for y, col in zip(range(4), ['a', 'b', 'c', 'd']):
					if (row+col) in self.currentState.board.occupied.keys():
						self.canvas.create_text((y*(500/4)+(250/4), x*(500/4)+(250/4)), text = self.currentState.board.occupied[row+col].tag)


		self.root.update_idletasks()
		self.root.update()

	# Destroy method to exit gui
	def exit(self):
		self.canvas.delete("all")
		self.root.destroy()

	# Click event function, records location of click and links it to a location on the board
	def click(self, event):
		if not self.waiting.get(): return
		self.move = (int(event.x/(500/4))+1, int(event.y/(500/4))+1)
		if self.move == (1, 1):
			self.add = '1a'
		elif self.move == (2, 1):
			self.add = '1b'
		elif self.move == (3, 1):
			self.add = '1c'
		elif self.move == (4, 1):
			self.add = '1d'
		elif self.move == (1, 2):
			self.add = '2a'
		elif self.move == (2, 2):
			self.add = '2b'
		elif self.move == (3, 2):
			self.add = '2c'
		elif self.move == (4, 2):
			self.add = '2d'
		elif self.move == (1, 3):
			self.add = '3a'
		elif self.move == (2, 3):
			self.add = '3b'
		elif self.move == (3, 3):
			self.add = '3c'
		elif self.move == (4, 3):
			self.add = '3d'
		elif self.move == (1, 4):
			self.add = '4a'
		elif self.move == (2, 4):
			self.add = '4b'
		elif self.move == (3, 4):
			self.add = '4c'
		elif self.move == (4, 4):
			self.add = '4d'

		print(self.add)
		self.waiting.set(0)

	# Turn based gameplay
	def play(self):

		self.pieceToPlay = None

		# Begin turns
		while True:

			#### PLAYER CHOOSES A PIECE ####
			self.control.wait_variable(self.buttonPressed)
			self.buttonPressed.set(0)
			self.pieceToPlay = self.selected
			self.buttons[self.pieceToPlay.id].config(state="disabled")
			self.p.set(self.pieceToPlay.tag)
			self.draw(True)
			print("Giving to computer:", self.pieceToPlay.tag)


			#### COMPUTER MAKES A MOVE ####
			self.currentState.turn = "Computer"
			####################
			#place = firstPlacement(self.currentState)
			#place = randomPlacement(self.currentState)
			place = alphabeta_cutoff(self.currentState)
			####################
			self.currentState.board.make_move(self.pieceToPlay, place)
			self.draw(True)

			# Win Check
			if(self.currentState.board.quarto()):
				print("Winner:", self.currentState.turn)
				break


			#### COMPUTER CHOOSES A PIECE ####
			####################
			self.pieceToPlay = firstPiece(self.currentState)
			#self.pieceToPlay = randomPiece(self.currentState)
			####################
			self.buttons[self.pieceToPlay.id].config(state="disabled")
			self.p.set(self.pieceToPlay.tag)
			self.draw(True)
			print("Gave to player:", self.pieceToPlay.tag)


			#### PLAYER MAKES A MOVE ####
			self.currentState.turn = "Player"
			self.add = None
			while self.add not in self.currentState.board.occupied.keys():
				self.waiting.set(1)
				self.canvas.wait_variable(self.waiting)
				self.currentState.board.make_move(self.pieceToPlay, self.add)

			self.add = None
			self.draw(True)

			# Win Check
			if(self.currentState.board.quarto()):
				print("Winner:", self.currentState.turn)
				break


if __name__ == "__main__":
	app = gameGUI()
	app.root.mainloop()
