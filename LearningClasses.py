from QuartoClasses import QuartoState
from qutil import *

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

from torch.utils.tensorboard import SummaryWriter

class QuartoNetwork(nn.Module):
	def __init__(self,inputSize=101,outputSize=257):
		super(QuartoNetwork,self).__init__()
		self.h1 = nn.Linear(inputSize,256)
		self.act1 = nn.ReLU()
		self.h2 = nn.Linear(256,256)
		self.act2 = nn.ReLU()
		self.h3 = nn.Linear(256,256)
		self.dropout1 = nn.Dropout(p=0.2)
		self.out = nn.Linear(256,outputSize)

	def forward(self, x):
		x = self.act1(self.h1(x))
		x = self.act2(self.h2(x))
		x = self.dropout1(self.h3(x))
		x = self.out(x)
		return x
	
class Buffer:
	def __init__(self, size):
		self.buffer = deque(maxlen=size)

	def add(self, exp):
		self.buffer.append(exp)

	def sample(self, size):
		return random.sample(self.buffer,size)
	
	def size(self):
		return len(self.buffer)
	
class DQNAgent:
	def __init__(self, writer: SummaryWriter, learningRate=0.001, gamma=0.99, epsilon=1, epsilon_min=0.1, epsilon_decay=0.995):
		self.epsilon = epsilon
		self.epsilon_min = epsilon_min
		self.epsilon_decay = epsilon_decay
		self.gamma = gamma
		self.q_net = QuartoNetwork()
		self.target_net = QuartoNetwork()
		self.target_net.load_state_dict(self.q_net.state_dict())
		self.optimizer = optim.Adam(self.q_net.parameters(), lr=learningRate)

		self.buffer = Buffer(size=200000)

		self.writer = writer

	def choice(self, state: QuartoState,eps=None):
		s = state.encode()
		if eps is None: eps = self.epsilon
		if np.random.rand() <= eps:
			act = random.choice(state.actions())
			return act
		s = torch.FloatTensor(s).unsqueeze(0)

		q_vals = self.q_net(s)

		mask = torch.full((257,), float('-inf'))
		for action in range(257):
			loc, piece = decodeAction(action)
			if valid(loc,state.board,piece,state.pieces):
				mask[action] = 0

		m_q_vals = q_vals + mask
		return decodeAction(m_q_vals.argmax().item())
	
	def updateEpsilon(self):
		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay

	def train(self,size):
		if self.buffer.size() < size:
			return
		
		batch = self.buffer.sample(size)
		states, actions, rewards, nextStates, dones = zip(*batch)

		states = torch.stack(states)
		actions = torch.LongTensor(actions).unsqueeze(1)
		rewards = torch.FloatTensor(rewards).unsqueeze(1)
		nextStates = torch.stack(nextStates)
		dones = torch.FloatTensor(dones).unsqueeze(1)

		q_vals = self.q_net(states).gather(1, actions)

		next_q = self.target_net(nextStates).max(1, keepdim=True)[0]
		target_q = rewards + (1 - dones) * self.gamma * next_q

		loss = nn.MSELoss()(q_vals,target_q)
		self.optimizer.zero_grad()
		loss.backward()
		self.optimizer.step()

		self.writer.add_scalar('Loss/Training', loss.item())
		self.writer.add_scalar('Rewards/Average', rewards.mean().item())
	
	def updateTargetNet(self):
		self.target_net.load_state_dict(self.q_net.state_dict())

class Train:
	def __init__(self, env: QuartoState, agent: DQNAgent, writer: SummaryWriter, episodes=20000, targetUpdate=10, size=32):
		self.env = env
		self.agent = agent
		self.episodes = episodes
		self.targetUpdate = targetUpdate
		self.size = size

		self.writer = writer

	def run(self):
		for episode in range(self.episodes):
			state = self.env.reset()
			done = False
			totalReward = 0

			while not done:
				action = self.agent.choice(state)
				scode = state.encode()
				nextState, reward, done = self.env.step(action)
				ncode = nextState.encode()
				self.agent.buffer.add((scode,encodeAction(action),reward,ncode,done))
				self.agent.train(self.size)

				state = nextState
				totalReward += reward

			if episode % self.targetUpdate == 0:
				self.agent.updateTargetNet()
			self.agent.updateEpsilon()

			self.writer.add_scalar('Training/Total Reward', totalReward, episode)

			if episode % 10 == 0:
				print(f"Episode: {episode} - Total Reward: {totalReward} - Epsilon: {self.agent.epsilon}")

		self.writer.close()

	def saveModel(self,filename):
		torch.save(self.agent.q_net.state_dict(), filename)
		print(f"Model saved to: {filename}")