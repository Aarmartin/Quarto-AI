from QuartoClasses import QuartoState
from LearningClasses import DQNAgent, Train

from torch.utils.tensorboard import SummaryWriter

env = QuartoState(setFirst=True)

writer = SummaryWriter('runs/DQNAgent_Training')

agent = DQNAgent(writer=writer)

trainer = Train(env,agent,writer=writer)

trainer.run()
trainer.saveModel("comp.model")

writer.close()