from QuartoClasses import *
from qutil import *

board = Board(True)

board.makeMove(0b0000,(0,0))

#print(board)

board.makeMove(0b0001,(0,1))
board.makeMove(0b0101,(0,2))
board.makeMove(0b1011,(0,3))
board.makeMove(0b0010,(1,0))


print(board)
print(board.boardUtil())
print(board.quarto())

# 0101
# 1011
