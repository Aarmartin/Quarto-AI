from tkinter import *
from QuartoClasses import *
from qutil import *
import sys
import os

class gameGUI:

	def __init__(self, title="Quarto",geometry="800x500"):

		self.firstPlayer = None
		self.piece = None

		# Env
		self.root = Tk()
		self.root.title(title)
		self.root.geometry(geometry)
		self.root.protocol("WM_DELETE_WINDOW", exit)
		def handle(event):
			self.root.quit()
			self.root.destroy()
			sys.exit()
			os._exit(0)
		self.root.bind_all('<Control-c>',handle)

		# Canvas
		self.canvas = Canvas(self.root, width=500, height=500)
		self.canvas.place(x=0,y=0)

		# Mouse Control
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

		self.buttons.append(Button(self.controlB, text="TLSS", command = lambda: self.setSelect(0)))
		self.buttons.append(Button(self.controlB, text="TLSH", command = lambda: self.setSelect(1)))
		self.buttons.append(Button(self.controlB, text="TLCS", command = lambda: self.setSelect(2)))
		self.buttons.append(Button(self.controlB, text="TLCH", command = lambda: self.setSelect(3)))
		self.buttons.append(Button(self.controlB, text="TDSS", command = lambda: self.setSelect(4)))
		self.buttons.append(Button(self.controlB, text="TDSH", command = lambda: self.setSelect(5)))
		self.buttons.append(Button(self.controlB, text="TDCS", command = lambda: self.setSelect(6)))
		self.buttons.append(Button(self.controlB, text="TDCH", command = lambda: self.setSelect(7)))
		self.buttons.append(Button(self.controlB, text="SLSS", command = lambda: self.setSelect(8)))
		self.buttons.append(Button(self.controlB, text="SLSH", command = lambda: self.setSelect(9)))
		self.buttons.append(Button(self.controlB, text="SLCS", command = lambda: self.setSelect(10)))
		self.buttons.append(Button(self.controlB, text="SLCH", command = lambda: self.setSelect(11)))
		self.buttons.append(Button(self.controlB, text="SDSS", command = lambda: self.setSelect(12)))
		self.buttons.append(Button(self.controlB, text="SDSH", command = lambda: self.setSelect(13)))
		self.buttons.append(Button(self.controlB, text="SDCS", command = lambda: self.setSelect(14)))
		self.buttons.append(Button(self.controlB, text="SDCH", command = lambda: self.setSelect(15)))

		for button in self.buttons:
			button.pack(anchor=W, fill=X)

		# Exit Button
		Button(self.controlM, text="Exit", command=self.exit).pack(fill=X, side="right")
		Button(self.controlM, text="Player", command= lambda: self.setPlayer("Player")).pack(fill=X, side="right")
		Button(self.controlM, text="Computer", command= lambda: self.setPlayer("Computer")).pack(fill=X, side="right")

		# Current Piece Label
		self.p = StringVar()
		self.p.set("Piece")
		Label(self.controlM, width=13, textvariable=self.p).pack(side="right")

		# Draw Board
		self.draw(None)

		# Begin Game
		self.play()

	def setSelect(self, piece):
		self.piece = piece
		self.buttonPressed.set(1)
		print("Current Selection:", self.piece)

	def setPlayer(self, player):
		if player == "Player":
			self.firstPlayer = "Player"
		else:
			self.firstPlayer = "Computer"
		self.buttonPressed.set(1)
		print("Player Selected:", self.firstPlayer)

	def draw(self, game: Game, content=False):
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(0,i,500,i)
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(i,0,i,500)

		if content:
			for x in range(4):
				for y in range(4):
					if game.getPiece(x,y) is not None:
						self.canvas.create_text((y*(500/4)+(250/4), x*(500/4)+(250/4)), text = game.getPiece(x,y))


		self.root.update_idletasks()
		self.root.update()

	def exit(self):
		self.canvas.delete("all")
		self.root.quit()
		self.root.destroy()
		sys.exit()
		os._exit(0)

	def click(self,event):
		if not self.waiting.get(): return
		self.move = (int(event.x/(500/4))+1, int(event.y/(500/4))+1)

		print(self.move)
		self.waiting.set(0)

	def play(self):

		def end():
			if game.won():
				print("Winner:", player)
				return True
			if game.finished():
				print("No Winners")
				return True
			return False
		
		def playerTurn():
			self.move = None
			while game.badMove(self.move):
				print("Bad move?",game.badMove(self.move))
				print("Waiting...")
				self.waiting.set(1)
				self.canvas.wait_variable(self.waiting)
			game.place(self.move)
			self.draw(game,True)
			self.piece = None
			while game.badPiece(self.piece):
				self.waiting.set(1)
				self.canvas.wait_variable(self.waiting)
			self.p.set(dpiece(self.piece))
			game.choose(self.piece)
			self.draw(game,True)
		
		def computerTurn():
			return

		while self.firstPlayer is None:
			self.control.wait_variable(self.buttonPressed)
			self.buttonPressed.set(0)

		game = Game(True,self.firstPlayer)
		player = self.firstPlayer

		if self.firstPlayer == "Computer":
			self.p.set(game.randomPiece())
			self.draw(game)

		if self.firstPlayer == "Computer":
			playerTurn()

		while True:
			
			computerTurn()

			if end():
				break

			playerTurn()

			if end():
				break

		self.draw(game)

if __name__ == "__main__":
	app = gameGUI()
	app.root.mainloop()