from QuartoClasses import *
from qutil import *

s = QuartoState()
s.setNext(0)

#s.setNext(0b0010)

print("First player")
res,rew,done = s.step(((0,0),1))
print(res,rew,done)



print("Second player")
res,rew,done = s.step(((0,1),2))
print(res,rew,done)

print("First player")
res,rew,done = s.step(((0,2),4))
print(res,rew,done)

print("Second player")
res,rew,done = s.step(((1,0),3))
print(res,rew,done)

print("First player")
res,rew,done = s.step(((0,3),5))
print(res,rew,done)

#print(board)

# s.move((0,1),0b0001)
# s.move((2,0),0b0101)
# s.move((3,3),0b1011)
# s.move((2,2),0b0010)
# s.move((0,2),0b0011)
#s.move((0,3),0b0101)

# print(s)
# print(s.actions())
# print(s.getBoardValue(),s.nextPiece,s.quarto(),s.terminal())

# s.reset()

# print(s)
# print(s.getBoardValue(),s.nextPiece)

# 0101
# 1011

# action = 256
# print(action)
# decAction = decodeAction(action)
# print(decAction)
# encAction = encodeAction(decAction)
# print(encAction)