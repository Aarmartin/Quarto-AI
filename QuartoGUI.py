from tkinter import *
from PIL import Image, ImageTk
from QuartoClasses import *
from Game import Game
from qutil import *
import sys
import os

class gameGUI:

	def __init__(self, model="models/comp.model", title="Quarto",geometry="1250x500"):

		self.firstPlayer = None
		self.piece = None
		self.model = model

		# Env
		self.root = Tk()
		self.root.title(title)
		self.root.geometry(geometry)
		self.root.protocol("WM_DELETE_WINDOW", exit)
		def handle(event):
			self.root.update()
			self.root.quit()
			self.root.destroy()
			sys.exit()
			os._exit(0)
		self.root.bind_all('<Control-c>',handle)
		self.root.pack_propagate(True)
		self.root.grid_propagate(True)

		# Canvas
		self.canvas = Canvas(self.root, width=500, height=500)
		self.canvas.place(x=0,y=0)

		# Mouse Control
		self.canvas.bind("<Button-1>", self.click)
		self.waiting = BooleanVar()
		self.waiting.set(1)
		self.buttonPressed = BooleanVar()
		self.buttonPressed.set(0)
		self.computerSelected = False
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
		self.pngs = []
		img = Image.open("Resources/TLSS.png").resize((100,100))
		self.TLSS = ImageTk.PhotoImage(img)
		self.pngs.append(self.TLSS)
		img = Image.open("Resources/TLSH.png").resize((100,100))
		self.TLSH = ImageTk.PhotoImage(img)
		self.pngs.append(self.TLSH)
		img = Image.open("Resources/TLCS.png").resize((100,100))
		self.TLCS = ImageTk.PhotoImage(img)
		self.pngs.append(self.TLCS)
		img = Image.open("Resources/TLCH.png").resize((100,100))
		self.TLCH = ImageTk.PhotoImage(img)
		self.pngs.append(self.TLCH)
		img = Image.open("Resources/TDSS.png").resize((100,100))
		self.TDSS = ImageTk.PhotoImage(img)
		self.pngs.append(self.TDSS)
		img = Image.open("Resources/TDSH.png").resize((100,100))
		self.TDSH = ImageTk.PhotoImage(img)
		self.pngs.append(self.TDSH)
		img = Image.open("Resources/TDCS.png").resize((100,100))
		self.TDCS = ImageTk.PhotoImage(img)
		self.pngs.append(self.TDCS)
		img = Image.open("Resources/TDCH.png").resize((100,100))
		self.TDCH = ImageTk.PhotoImage(img)
		self.pngs.append(self.TDCH)
		img = Image.open("Resources/SLSS.png").resize((100,100))
		self.SLSS = ImageTk.PhotoImage(img)
		self.pngs.append(self.SLSS)
		img = Image.open("Resources/SLSH.png").resize((100,100))
		self.SLSH = ImageTk.PhotoImage(img)
		self.pngs.append(self.SLSH)
		img = Image.open("Resources/SLCS.png").resize((100,100))
		self.SLCS = ImageTk.PhotoImage(img)
		self.pngs.append(self.SLCS)
		img = Image.open("Resources/SLCH.png").resize((100,100))
		self.SLCH = ImageTk.PhotoImage(img)
		self.pngs.append(self.SLCH)
		img = Image.open("Resources/SDSS.png").resize((100,100))
		self.SDSS = ImageTk.PhotoImage(img)
		self.pngs.append(self.SDSS)
		img = Image.open("Resources/SDSH.png").resize((100,100))
		self.SDSH = ImageTk.PhotoImage(img)
		self.pngs.append(self.SDSH)
		img = Image.open("Resources/SDCS.png").resize((100,100))
		self.SDCS = ImageTk.PhotoImage(img)
		self.pngs.append(self.SDCS)
		img = Image.open("Resources/SDCH.png").resize((100,100))
		self.SDCH = ImageTk.PhotoImage(img)
		self.pngs.append(self.SDCH)

		self.buttons: list[Button] = []

		self.buttons.append(Button(self.controlB, image=self.TLSS, command = lambda: self.setSelect(0)))
		self.buttons.append(Button(self.controlB, image=self.TLSH, command = lambda: self.setSelect(1)))
		self.buttons.append(Button(self.controlB, image=self.TLCS, command = lambda: self.setSelect(2)))
		self.buttons.append(Button(self.controlB, image=self.TLCH, command = lambda: self.setSelect(3)))
		self.buttons.append(Button(self.controlB, image=self.TDSS, command = lambda: self.setSelect(4)))
		self.buttons.append(Button(self.controlB, image=self.TDSH, command = lambda: self.setSelect(5)))
		self.buttons.append(Button(self.controlB, image=self.TDCS, command = lambda: self.setSelect(6)))
		self.buttons.append(Button(self.controlB, image=self.TDCH, command = lambda: self.setSelect(7)))
		self.buttons.append(Button(self.controlB, image=self.SLSS, command = lambda: self.setSelect(8)))
		self.buttons.append(Button(self.controlB, image=self.SLSH, command = lambda: self.setSelect(9)))
		self.buttons.append(Button(self.controlB, image=self.SLCS, command = lambda: self.setSelect(10)))
		self.buttons.append(Button(self.controlB, image=self.SLCH, command = lambda: self.setSelect(11)))
		self.buttons.append(Button(self.controlB, image=self.SDSS, command = lambda: self.setSelect(12)))
		self.buttons.append(Button(self.controlB, image=self.SDSH, command = lambda: self.setSelect(13)))
		self.buttons.append(Button(self.controlB, image=self.SDCS, command = lambda: self.setSelect(14)))
		self.buttons.append(Button(self.controlB, image=self.SDCH, command = lambda: self.setSelect(15)))

		for i, button in enumerate(self.buttons):
			x = i // 4
			y = i % 4
			button.grid(row=x,column=y,padx=5,pady=5)

		# Exit Button
		Button(self.controlM, text="Exit", command=self.exit).pack(fill=X, side="right")
		Button(self.controlM, text="Player", command= lambda: self.setPlayer("Player")).pack(fill=X, side="right")
		Button(self.controlM, text="Computer", command= lambda: self.setPlayer("Computer")).pack(fill=X, side="right")

		# Current Piece Label
		# self.p = StringVar()
		# self.p.set("Piece")
		self.selectedPiece = Label(self.controlM,image=None)
		self.selectedPiece.pack(side="right")

		# Draw Board
		self.draw(None)

		# Begin Game
		self.play()

	# Set selected piece for play
	def setSelect(self, piece):
		if piece is None:
			self.selectedPiece.config(image='')
			self.root.update()
		else:
			self.piece = piece
			self.buttonPressed.set(1)
			if not self.computerSelected:
				self.selectedPiece.config(image=self.pngs[self.piece])
			self.root.update()
			self.waiting.set(0)

	# Set current player
	def setPlayer(self, player):
		if player == "Player":
			self.firstPlayer = "Player"
		else:
			self.firstPlayer = "Computer"
		self.buttonPressed.set(1)
		print("Player Selected:", self.firstPlayer)

	# Draw board
	def draw(self, game: Game, content=False):
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(0,i,500,i)
		for i in range(0,500,int(500/4)):
			self.canvas.create_line(i,0,i,500)

		if content:
			for x in range(4):
				for y in range(4):
					p = game.getPiece((x,y))
					if p is not None:
						#self.canvas.create_text((y*(500/4)+(250/4), x*(500/4)+(250/4)), text = game.getPiece(x,y))
						self.canvas.create_image((x*(500/4)+(250/4), y*(500/4)+(250/4)), image=self.pngs[p])

		self.root.update_idletasks()
		self.root.update()

	# Exit function
	def exit(self):
		self.root.update()
		self.canvas.delete("all")
		self.root.quit()
		self.root.destroy()
		sys.exit()
		os._exit(0)

	# Map grid selection to location for action
	def click(self,event):
		if not self.waiting.get(): return
		self.move = (int(event.x/(500/4)), int(event.y/(500/4)))
		x,y = self.move
		self.waiting.set(0)

	def play(self):

		# End Status
		def end():
			if game.finished():
				if game.won():
					print("Winner:", player)
				else:
					print("No Winners")
				return True
			return False
		
		# Player's Turn: Selecting location to place piece
		def playerTurnPlace():
			self.move = None
			while game.badMove(self.move):
				self.waiting.set(1)
				self.canvas.wait_variable(self.waiting)
			game.playerPlace(self.move)
			self.computerSelected = False
			self.setSelect(None)
			self.draw(game,True)

		# Player's Turn: Choosing a piece to give opponent
		def playerTurnSelect():
			self.piece = None
			while game.badPiece(self.piece):
				self.waiting.set(1)
				self.canvas.wait_variable(self.waiting)
			# self.p.set(dpiece(self.piece))
			game.playerPick(self.piece)
			self.buttons[self.piece]["state"] = "disabled"
			self.draw(game,True)
		
		# Computer's Turn
		def computerTurn():
			game.computerTurn()
			self.piece = game.state.nextPiece
			self.setSelect(self.piece)
			self.buttons[self.piece]["state"] = "disabled"
			self.computerSelected = True
			self.draw(game,True)

		# Wait for first player selection
		while self.firstPlayer is None:
			self.control.wait_variable(self.buttonPressed)
			self.buttonPressed.set(0)

		game = Game(self.model)
		player = self.firstPlayer

		# First player chooses piece, and play begins
		if self.firstPlayer == "Computer":
			print("Computer Selecting a Piece...")
			self.piece = game.setFirstPiece(rand=True)
			self.setSelect(self.piece)
			self.buttons[self.piece]["state"] = "disabled"
			self.draw(game)
			player = "Player"
			playerTurnPlace()
			playerTurnSelect()
		else:
			self.piece = None
			print("Please Select a Piece")
			while self.piece is None:
				self.control.wait_variable(self.buttonPressed)
				self.buttonPressed.set(0)
			game.setFirstPiece(self.piece)
			self.buttons[self.piece]["state"] = "disabled"
			player = "Computer"

		# Gameplay loop
		while self.root.winfo_exists():
			
			print("Computer's Turn...")
			player = "Computer"
			computerTurn()
			self.root.update()
			if end():
				break

			print("Player Placing...")
			player = "Player"
			playerTurnPlace()
			self.root.update()
			if end():
				break

			print("Player Selecting")
			playerTurnSelect()
			self.root.update()
			if end():
				break

			try:
				self.root.winfo_exists()
			except:
				break

if __name__ == "__main__":
	if len(sys.argv) > 1:
		model = str(sys.argv[1])
	else:
		model = "comp.model"
	app = gameGUI(model)
	app.root.mainloop()