from QuartoClasses import QuartoState
from qutil import *

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

from torch.utils.tensorboard import SummaryWriter

class QNetwork(nn.Module):
	def __init__(self):

		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

		super(QNetwork,self).__init__()

		# Layers and Activation
		# Convolutional layers for board space
		self.conv1 = nn.Conv2d(1,16, kernel_size=2, stride=1).to(self.device)
		self.convact1 = nn.ReLU().to(self.device)
		self.conv2 = nn.Conv2d(16,32, kernel_size=2, stride=1)
		self.convact2 = nn.ReLU().to(self.device)
		self.flatten = nn.Flatten().to(self.device)
		self.h1 = nn.Linear(145,512).to(self.device)
		self.act1 = nn.ReLU().to(self.device)
		self.h2 = nn.Linear(512,512).to(self.device)
		self.act2 = nn.ReLU().to(self.device)
		self.out = nn.Linear(512,272).to(self.device)

	def forward(self, boardv, piecev):
		board = boardv.view(-1,1,4,4)							# Convert board vector for convoultional input
		x = self.convact1(self.conv1(board))
		x = self.convact2(self.conv2(x))
		x = self.flatten(x)										# Flatten convolutional output
		concat = torch.cat((x,piecev),dim=1).to(self.device)	# Combine with piece information
		x = self.act1(self.h1(concat))
		x = self.act2(self.h2(x))
		x = self.out(x)
		return x
	
class Buffer:
	def __init__(self, size):
		self.buffer = deque(maxlen=size)

	def add(self, exp):
		'''
		Append experience to replay buffer

		Parameters:
		exp (Tensor,int,int,Tensor,bool): A state, action, reward, nextState, and done experience tuple
		'''
		self.buffer.append(exp)

	def sample(self,size):
		'''
		Calculate trainind data priority for weighted sample selection of experiences

		Parameters:
		size (int): The batch size of experiences to return

		Returns:
		list(Tensor,int,int,Tensor,bool): A list of experiences
		'''
		# Calculate Priority based on reward
		rewards = [exp[2] for exp in self.buffer]
		probabilities = [abs(reward) + 1e-5 for reward in rewards]
		total = sum(probabilities)
		probabilities = [p/total for p in probabilities]
		samples = random.choices(self.buffer,weights=probabilities,k=size)
		return samples
	
	def size(self):
		return len(self.buffer)

class DQNAgent:
	def __init__(self, epsilon=1, epsilon_min=0.1, epsilon_decay=0.995, gamma=0.99, learningRate=0.001, q_net=None, t_net=None, optimizer=None, buffer=None):
		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

		self.epsilon = epsilon
		self.epsilon_min = epsilon_min
		self.epsilon_decay = epsilon_decay
		self.gamma = gamma
		if q_net is None:
			self.q_net = QNetwork().to(self.device)
		else:
			self.q_net = q_net
		if t_net is None:
			self.t_net = QNetwork().to(self.device)
		else:
			self.t_net = t_net
		self.t_net.load_state_dict(self.q_net.state_dict())
		if optimizer is None:
			self.optimizer = optim.Adam(self.q_net.parameters(), lr=learningRate)
		else:
			self.optimizer = optimizer

		if buffer is None:
			self.buffer = Buffer(size=200000)
		else:
			self.buffer = buffer

	def choice(self, state: QuartoState, eps=None):
		'''
		Decision making process based on state

		Parameters:
		state (QuartoState): A Quarto state
		eps (float): Optional custom epsilon value

		Returns:
		((int,int),int): A location and piece pair reprsenting an action
		'''
		# Random choice at rate of epsilon, for exploration
		if eps is None: eps = self.epsilon
		if np.random.rand() <= eps:
			act = random.choice(state.actions())
			return act
		
		# Encode board state and piece information
		b,p = state.encode()
		p = torch.tensor(p,dtype=torch.float,device=self.device).unsqueeze(0)

		# Retrieve Q values
		q_vals = self.q_net(b,p)

		# Mask invalid actions
		mask = torch.full((272,), float('-inf')).to(self.device)
		for action in range(272):
			loc, piece = decodeAction(action)
			if valid(loc,state.board,piece,state.pieces):
				mask[action] = 0
		m_q_vals = q_vals + mask

		# Return action
		return decodeAction(m_q_vals.argmax().item())
	
	def updateEpsilon(self):
		'''
		Update Epsilon value
		'''
		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay

	def train(self,size):
		'''
		Training algorithm for training agent's Q-Network

		Parameters:
		size (int): Batch size passed to replay buffer sample

		Returns:
		float: The loss after Q Training
		'''
		# Return if batch size too small
		if self.buffer.size() < size:
			return
		
		# Sample from replay buffer
		batch = self.buffer.sample(size)
		states, actions, rewards, nextStates, dones = zip(*batch)
		stateboards, statepieces = zip(*states)
		nextstateboards, nextstatepieces = zip(*nextStates)

		# Convert training data to Tensors
		stateboards = torch.stack(stateboards).to(self.device)
		statepieces = torch.stack(statepieces).to(self.device)
		actions = torch.tensor(actions,dtype=torch.long,device=self.device).unsqueeze(1)
		rewards = torch.tensor(rewards,dtype=torch.float,device=self.device).unsqueeze(1)
		nextstateboards = torch.stack(nextstateboards).to(self.device)
		nextstatepieces = torch.stack(nextstatepieces).to(self.device)
		dones = torch.tensor(dones,dtype=torch.bool,device=self.device).unsqueeze(1)

		# Update Q values, cut off terminal states
		q_vals = self.q_net(stateboards,statepieces).gather(1, actions)
		next_q = self.t_net(nextstateboards,nextstatepieces).max(1, keepdim=True)[0]
		next_q[dones] = 0.0
		t_q = rewards + (self.gamma * next_q)

		# Calculate loss gradient
		criterion = nn.MSELoss()
		loss = criterion(q_vals,t_q)
		self.optimizer.zero_grad()
		loss.backward()
		self.optimizer.step()

		return loss.item()
	
	def updateTargetNet(self):
		'''
		Update Target Network
		'''
		self.t_net.load_state_dict(self.q_net.state_dict())

class Train:
	def __init__(self, env: QuartoState, agent1: DQNAgent, agent2: DQNAgent, episodes=10000, targetUpdate=10, size=128, writer: SummaryWriter = None):
		self.env = env
		self.agent1 = agent1
		self.agent2 = agent2
		self.episodes = episodes
		self.targetUpdate = targetUpdate
		self.size = size
		self.writer = writer

	def run(self):
		'''
		Training method for simulating two agent gameplay
		'''
		for episode in range(self.episodes):
			state = self.env.reset()
			done = False
			deck = None

			while not done:

				# Agent 1 Sequence
				action1 = self.agent1.choice(state)					# Choose action
				scodeboard1, scodepiece1 = state.encode()			# Encode original state
				acode1 = encodeAction(action1)						# Encode action
				nextState1, reward1, done = self.env.step(action1)	# Step function, with nextState, reward, and done
				ncodeboard1,ncodepiece1 = nextState1.encode()		# Encode next state
				
				# If done, retieve values from staged agent 2 step results and push them with negative reward
				if done:
					(b,p),a,_,(nb,np),d = deck
					self.agent2.buffer.add(((b,p),a,-reward1,(nb,np),d))
					self.agent1.buffer.add(((scodeboard1,scodepiece1),acode1,reward1,(ncodeboard1,ncodepiece1),done))
					break
				else:
					if deck is not None:
						# Push staged agent 2 step results
						self.agent2.buffer.add(deck)
				# Stage new results
				deck = ((scodeboard1,scodepiece1),acode1,reward1,(ncodeboard1,ncodepiece1),done)

				state = nextState1

				# Agent 2 Sequence
				action2 = self.agent2.choice(state)					# Choose action
				scodeboard2,scodepiece2 = state.encode()			# Encode original state
				acode2 = encodeAction(action2)						# Encode action
				nextState2, reward2, done = self.env.step(action2)	# Step function, with nextState, reward, and done
				ncodeboard2,ncodepiece2 = nextState2.encode()		# Encode next state

				# If done, retrieve values from staged agent 1 step results and push them with negative reward
				if done:
					(b,p),a,_,(nb,np),d = deck
					self.agent1.buffer.add(((b,p),a,-reward2,(nb,np),d))
					self.agent2.buffer.add(((scodeboard2,scodepiece2),acode2,reward2,(ncodeboard2,ncodepiece2),done))
					break
				else:
					self.agent1.buffer.add(deck)
				deck = ((scodeboard2,scodepiece2),acode2,reward2,(ncodeboard2,ncodepiece2),done)

				state = nextState2

			# Train agents
			rl1 = self.agent1.train(self.size)
			rl2 = self.agent2.train(self.size)

			if rl1 is not None and rl2 is not None and self.writer is not None:
				self.writer.add_scalar("loss/episode Agent 1",rl1,episode)
				self.writer.add_scalar("loss/episode Agent 2",rl2,episode)

			# Periodically update target net
			if episode % self.targetUpdate == 0:
				self.agent1.updateTargetNet()
				self.agent1.updateEpsilon()
				self.agent2.updateTargetNet()
				self.agent2.updateEpsilon()

			if episode % 1000 == 0:
				print(f"Episode: {episode}")
		
		self.writer.close()

	def saveModel(self,filename1,filename2=None):
		'''
		Method for saving model to file output

		Parameters:
		filename1 (str): The filename to save the first agent's network model
		filename2 (str): Optional filename to save second agent's network model
		'''
		torch.save(self.agent1.q_net.state_dict(), filename1)
		print(f"Model saved to: {filename1}")
		if filename2 is not None:
			torch.save(self.agent2.q_net.state_dict(), filename2)
			print(f"Model saved to: {filename2}")