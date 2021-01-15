from tkinter import *
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

		self.leftover = self.pieces

	def make_move(self, piece, loc):
		if loc in self.open and piece not in self.occupied.values():
			self.occupied[loc] = piece
			self.open.remove(loc)
			self.leftover.remove(piece)
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
		self.tag = self.height[:1] + self.color[:1] + self.shape[:1] + self.fill[:1]

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
		self.move = None



		self.control = Frame(self.root)
		self.control.place(x=510, y=10)

		Button(self.control, text="TLSS", command = lambda: self.setSelect(board.pieces[0])).pack(anchor=W,fill=X)
		Button(self.control, text="TLSH", command = lambda: self.setSelect(board.pieces[1])).pack(anchor=W,fill=X)
		Button(self.control, text="TLCS", command = lambda: self.setSelect(board.pieces[2])).pack(anchor=W,fill=X)
		Button(self.control, text="TLCH", command = lambda: self.setSelect(board.pieces[3])).pack(anchor=W,fill=X)
		Button(self.control, text="TDSS", command = lambda: self.setSelect(board.pieces[4])).pack(anchor=W,fill=X)
		Button(self.control, text="TDSH", command = lambda: self.setSelect(board.pieces[5])).pack(anchor=W,fill=X)
		Button(self.control, text="TDCS", command = lambda: self.setSelect(board.pieces[6])).pack(anchor=W,fill=X)
		Button(self.control, text="TDCH", command = lambda: self.setSelect(board.pieces[7])).pack(anchor=W,fill=X)
		Button(self.control, text="SLSS", command = lambda: self.setSelect(board.pieces[8])).pack(anchor=W,fill=X)
		Button(self.control, text="SLSH", command = lambda: self.setSelect(board.pieces[9])).pack(anchor=W,fill=X)
		Button(self.control, text="SLCS", command = lambda: self.setSelect(board.pieces[10])).pack(anchor=W,fill=X)
		Button(self.control, text="SLCH", command = lambda: self.setSelect(board.pieces[11])).pack(anchor=W,fill=X)
		Button(self.control, text="SDSS", command = lambda: self.setSelect(board.pieces[12])).pack(anchor=W,fill=X)
		Button(self.control, text="SDSH", command = lambda: self.setSelect(board.pieces[13])).pack(anchor=W,fill=X)
		Button(self.control, text="SDCS", command = lambda: self.setSelect(board.pieces[14])).pack(anchor=W,fill=X)
		Button(self.control, text="SDCH", command = lambda: self.setSelect(board.pieces[15])).pack(anchor=W,fill=X)

		self.draw()

		self.play()

	def setSelect(self, piece):
		self.selected = piece
		print("Current Selection is now:", self.selected.tag)

	def draw(self, content=False):
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(0,i,500,i)
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(i,0,i,500)

		if content:
			for x, row in zip(range(4), ['1', '2', '3', '4']):
				for y, col in zip(range(4), ['a', 'b', 'c', 'd']):
					if (row+col) in self.currentState.board.occupied.keys():
						self.canvas.create_text((x*(500/4)+(250/4), y*(500/4)+(250/4)), text = self.currentState.board.occupied[row+col].tag)


		self.root.update_idletasks()
		self.root.update()

	def click(self, event):
		if not self.waiting.get(): return
		self.move = (int(event.x/(500/4))+1, int(event.y/(500/4))+1)
		if self.move == (1, 1):
			self.add = '1a'
		elif self.move == (1, 2):
			self.add = '1b'
		print(self.add)
		self.waiting.set(1)

	def play(self):

		while True:

			self.add = None
			while self.add not in self.currentState.board.occupied.keys():
				self.waiting.set(1)

			self.currentState.board.make_move(random.choice(self.currentState.board.leftover), random.choice(self.currentState.board.open))
			self.currentState.board.printBoard()

			self.draw(True)

			if(self.currentState.board.quarto()):
				print("Winner:", self.currentState.turn)
				break

			self.currentState.turn = "Computer"

			self.currentState.board.make_move(random.choice(self.currentState.board.leftover), random.choice(self.currentState.board.open))
			self.currentState.board.printBoard()

			self.draw(True)

			if(self.currentState.board.quarto()):
				print("Winner", self.currentState.turn)
				break

			self.currentState.turn = "Player"


if __name__ == "__main__":
	app = gameGUI()
	app.root.mainloop()
