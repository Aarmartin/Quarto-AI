from LearningClasses import DQNAgent
from qutil import *

import torch

class Computer:

	def __init__(self,model):
		self.agent = DQNAgent()
		self.agent.q_net.load_state_dict(torch.load(model,weights_only=False))
		self.agent.q_net.eval()

	def play(self,state):
		action = self.agent.choice(state,0)
		return action