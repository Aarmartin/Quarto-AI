from QuartoClasses import *
import random

INFI = 1.0e400

def firstChoice(state: State):
	return state.successors()[0].lastMove()

def randomChoice(state: State):
	return random.choice(state.successors()).lastMove()

def negamax(state: State, alpha, beta, depth, player, eval_fn=None):
	eval_fn = eval_fn or (lambda s: s.utility())

	if depth == 0 or state.terminal():
		return eval_fn(state)
	
	v = -INFI
	for s in state.successors():
		v = max(v, -negamax(s, -beta, -alpha, depth - 1, -player))
		alpha = max(alpha, v)
		if alpha >= beta:
			break
	return v

def alphabetaChoice(state: State, depth=1):

	bestScore = -INFI

	for s in state.successors():
		score = negamax(s, -INFI, INFI, depth, 1)
		if score > bestScore:
			best = s
			bestScore = score
	
	return best.lastMove()