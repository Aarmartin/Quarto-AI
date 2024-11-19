from QuartoClasses import QuartoState
from LearningClasses import DQNAgent, Buffer, Train, QNetwork
import torch
import torch.optim as optim

from torch.utils.tensorboard import SummaryWriter

EPSILON = 1
EPSILON_MINIMUM = 0.1
EPSILON_DECAY = 0.995
GAMMA = 0.997
LEARNING_RATE = 0.001
EPISODES = 30000
BUFFER_SIZE = 300000
BATCH_SIZE = 128
WIN_REWARD = 10

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Quarto State
env = QuartoState(training=True,rewardVal=WIN_REWARD)

# Replay Buffer
buffer = Buffer(BUFFER_SIZE)

# Q Network and Target Network
q_net = QNetwork().to(device)
t_net = QNetwork().to(device)

# Optimizer
optimizer = optim.Adam(q_net.parameters(),lr=LEARNING_RATE)

# Agents
agent1 = DQNAgent(epsilon=EPSILON,epsilon_min=EPSILON_MINIMUM,epsilon_decay=EPSILON_DECAY,gamma=GAMMA,q_net=q_net,t_net=t_net,buffer=buffer,optimizer=optimizer)
agent2 = DQNAgent(epsilon=EPSILON,epsilon_min=EPSILON_MINIMUM,epsilon_decay=EPSILON_DECAY,gamma=GAMMA,q_net=q_net,t_net=t_net,buffer=buffer,optimizer=optimizer)

writer = SummaryWriter()

# Trainer
trainer = Train(env,agent1=agent1,agent2=agent2,episodes=EPISODES,size=BATCH_SIZE, writer=writer)

# Run training, and save model
trainer.run()
trainer.saveModel("models/comp.model")