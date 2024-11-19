
# Quarto DQNAgent

Quarto is a two player zero-sum adversarial board game. The board is a 4x4 grid, in which the goal of the game is to place down four pieces in a row, column, or diangonal that all share at least one trait. Each piece contains 4 traits, Tall or short, Light or Dark, Square or Circle, and Solid or Hollow. This gives us 2<sup>4</sup> = 16 unique pieces. Gameplay works by handing the opponent the piece they are to play, and placing it onto the board before choosing their own piece to give to the player.

With 16 placements, and 16 pieces, there are ~16! possible board configurations. Though, there are many symmetries at play, and many invalid board states. Invalid board states include configurations with two separate distinct winning Quarto lines, as such a state in not achievable in a normal game. Regardless, the state space for possible board configurations is incredibly large.

The goal of this program is to develop an agent that can effectively play a game of Quarto.

[Instructions for running a game](#running-a-game)

## Challenges

- **Large State Space** - The large state space of the quarto board provides a difficult challenge in any state based evaluation on possible future states.
- **Shared State** - The board and all pieces are shared by both players, where the winner is determined by the first person to place the piece in a winning line. This makes the evaluation of intermediary states particularly difficult, as any given state is effecetively for both players only depending on whose turn it currently is.
- **Action Sequence** - A unique quirck of Quarto is the mechanic involving the piece selection for which your opponent is to place. Each action sequence then requires two separate actions to perform, choosing where you would like to place a piece, and choosing which piece will be next to play. This durastically increases the amount of possible action choices, especially in early game settings.

These challenges provide a unique setting with different considerations. There are a few different approaches that can be taken, each with their own complications.
## Approaches

- MinMax α-β Pruning
    * The first approach was to use MinMax alpha beta pruning to perform a search on the state tree. This way, the state space could be greatly reduced through it's pruning methods to find a path to victory.
    * The complication of a utility function arises. In order to properly perform pruning on your state tree, the value of a state must be evaluated to rank the states against each other. The primary rewards for winning, losing, and a draw are your terminal states with the highest impact on score, but without a proper utility function, the state search depth would have to be incredibly deep, effectively eliminating the benefits provided by this method in the first place. With too shallow a tree, decisions are effectively random.
- Q-Learning
    * The next consideration is Q-Learning, in response to the complication of the lack of intermediate utility. This method would perform a sequence of games and propogate Q-Values down to the intermediary states, so the can properly be ranked in decision making processess throughout the game.
    * The main complication of this approach is, once again, its incredibly vast state space. In order to mark a state with a Q-Value score, that state must be saved and tracked within a lookup table, which becomes impractical with so many possible states. Learning would also take an impractically long time to account for every possible state.
- Deep Q-Learning
    * This next method is an adaptation on Q-Learning that is an attempted response to the state space constraint. Instead of learning and tracking the Q-Values for every possible state, states and actions are tracked with their rewards and fed into a neural network to determine that state's Q-Value. This eleminates the storage constraint of the state space, as no individual states are saved, only the trained neural network model. This will also assist in pattern recognition of states, where the generalized state can better be tracked, and a state that has never been seen before can still be approached with some level of understanding.
    * The largest complication of Deep Q-Learning is the development of an effective state representation and an adequate training regime. The model needs to be able to take in the state representation and accurately identify patternistic behavior to generalize possible moves. It then needs to adequately back-propogate the results of its learning to the intermediary states in order for significant look ahead to the winning conditions, as we are still without intermediary reward. Sparse rewards in Deep Q-Learning mean more data is needed for learning to converge.
## DQNAgent Implementation

This implementaion is through the use of a Deep Q-Learning Agent (DQNAgent) that simulates gameplay in order to train a neural network, managed by a custom Q-Netowrk class, on how to play the game. Given the shared state aspect of the game, the approach will include two DQNAgents playing against each other, while training against the same neural network. The decision for the shared Q-Network is to reduce the training time and data required for convergence given its sparse rewards. After each simulated game completion, the agents are trained on the resulting values of the outcome. Outcomes are stored in a replay buffer of a set capacity for which the training data is sampled from. This capacity cap allows for the elimination of stale data to be trained on. A target Q-Network is developed along side the main neural net at a slower rate to allow for increased generalization. After training against the Q-Network, the loss is calculated against the target network and fed to an optimizer for determining the loss gradient and optimizing the learning rate.

### QuartoState
The QuartoState class is the representation of the game state. The primary data points in this class are a 2D array, representing the board, a list of available pieces, and the currently selected piece that is to be played next.

This class contains methods that allow for actions to be taken on the state, including the placement and selection of pieces.

It also contains encoding methods that allow the state to be encoded in preparation to be passed as input into the neural network. Choosing the write method of encoding was challenging, as it will effect the nature of understanding that the Q-Network gain about the games underlying mechanisms. I took a few different approaches to this.
- Flat binary representation
	- This method encodes the state by first representing each piece as a 4 digit binary sequence. Each digit represents a trait, with a 1 or a 0 to determine which classification if had. The board was then encoded as 16 5 digit binary codes, one for each location on the board. The first bit signified the presence of a piece, and the next four digits represented the occupying piece. This encoding was then conjoined with a 4 digit binary sequence that represented the next piece to be played. Then, 16 more binary digits were added, representing the 16 pieces, 1 if the piece was available, and 0 if it was already on the board, or set as the next piece.
	- This representation of the board state seems to encompass the exact state of the board, however, it creates a very 'piece-specific' view of the board state, complicating the generalizability across logically equivalent states. Each trait of each pieces corresponding to an input results in only learning against those exact specific states.
	- The next complication revolves around utilizing 0s as placeholders for an absent board space, only signified by the presense of a different input. This requires the network to associated these values to a much higher degree, given that 4 zeros also represents a piece.
- One-Hot Encoding
	- This approach seeks to alleviate the misrepresentation of input from absent pieces on the board by converting the encoding to a 256 input representation of the board, where each group of 16 represents a board space. Each input then corresponds to one of the 16 pieces, all of which are set to 0 except for whichever piece may be occupying the space.
	- This is a better representation at the cost of much more computational power needed for the increased network input size. It also still suffers from piece specificity, but to a smaller degree.
- Normalized encoding
	- The current implementation moves away from the binary input layer to a float inputs. The board representation is flat 16 element vector, where each element contains the normalized integer value of the piece occupying the board. This is performed by a calculation `(piece + 1)/16` to normalize the value between 0 and 1. An empty space is signified by a 0. This encoding then forms the input into a convolutional layer, were it is adapted into a 2D "image" for better spacial relationship procesing. A second input containing a normalized piece value for the next piece, and the same 16 digit binary sequence that reprents available pieces make up another encoded vector.
	- This encoding process greatly simplifies the processing required on the part of the neural network with a significantly smaller input size. While the normalized values are still piece specific, patternistic relationships can be better accounted for from the convolutional input board.

### QNetwork
The QNetwork class manages the construction and activation of a neural network. The layers for which involve two different layer types, and ReLU activation functions.
- Convolutional Layer
- ReLU Activation
- Convolutional Layer
- ReLU Activation
- Flatten
- Linear Layer
- ReLU Activation
- Linear Layer
- ReLU Activation
- Output Layer

The original approach involved only Linear Layers, but was adapted to contain early convolutional layers to better learn from the 2D spatial relationships of the board state. The board encoding is first fed into the convolutional layers and activated by ReLU functions, before the final output is flattened back into a 1 dimensional vector. This is then concatenated with the piece information vector to serve as the main input into the linear layers. ReLU activation functions were chosen over Sigmoid activiation functions due to the spare reward nature of the training which can lead to the vanishing gradient problem, when neuron values are much closer to 0 or 1. There is no final activation function for the output layer to leave it as Linear for an unconstrained representation of the output Q-Values.

### Buffer
The Buffer class is to represent our replay buffer, containing all of our training data. This contains a deque for storing experiences during training in the form of `(state, action, reward, nextState, done)`. Each step of a game creates an experience that is pushed onto the replay buffer. The capacity marks the number of historical experiences that are stored, so after a certain point, old and stale experiences are dropped off and no longer used for training.

The sample method is a method to retrieve a random sample of these experiences for the purpose of training, to promote generalizability. Given the sparse reward nature of the game, where nearly all of the intermediary steps come with no reward, the sample method is done using a weighted probability choice, that attributes incread priority to significant rewards, i.e. rewards away from 0. This allows the buffer to provide more useful training data to the batch.

### DQNAgent
This class is the primary DQNAgent class that handles decision making and training against it's associated Q-Network.

The choice method takes in the input of a state, and produces an action that the agent then wishes to take. The section of the method checks against the agent's epsilon value, which will determine whether or not a completely random valid action will be taken. If the random value lands above the epislon value, the decision moves to the neural network to provide Q-Values for the decision making process. The state is fed into the network, and a list of the resulting output Q-Values are returned. These outputs are then masked to eliminate invalid moves. The highest remaining Q-Value action is is then returned.

The train method is the foundational script for training the neural network. The only parameter is the batch size to be used for sampling against the replay buffer.
- The batch size is checked against the size of the buffer. If not enough training data exists in the buffer, we skip training and return.
- The replay buffer is sample from the batch size, pulling in a list of experiences that are zipped into individual lists of states, actions, rewards, nextStates, and dones.
- Each of these lists are stacked and converted into 1 dimensional Tensors.
- The Q-Values are gathered from our list of states against our list of actions.
- Our next predicted future Q-Values are then pulled against our list of nextStates.
- Predicted values for terminal states are negated to 0.
- Our target Q-Values are created from our predicted Q-Values against our discount (γ) and added to our reward values.
- Loss is calculated from the comparison of our Q-Values to our target Q-Values, and a loss gradient is created to optimize our learning rate.

The update epsilon method dynamically reduces our epsilon value to increase focus on neural network output

### Trainer
The Trainer class facilitates the creation of our agents and the simulation of games over a period of episodes.

Two agents are created, each with a reference to a Q-Network. This can either be the same network, or separate ones, but this implementation has them both share the same Q-Network.
- An episode begins and a new reset state is established
- A While loop begins as the gameplay loop for the simulated game, finishing when the state becomes a terminal state
	- Agent 1 analyzes the state and makes their choice of action
	- The action is performed on the state
	- Terminal status is checked
		- If the status is terminal, the experience (original state, action, reward, next state, terminal status) is pushed to Agent 1's buffer with a win reward
		- The staged experience is pushed to Agent 2's buffer with a reward of a loss, or -reward
		- Break
	- If not terminal, the staged experience is pushed to Agent 2's buffer with its original reward
	- The recent experience is pushed to the staged experience variable
	- Agent 2 analyzes the state and makes their choice of action
	- The action is performed on the state
	- Terminal status is checked
		- If the status is terminal, the experience is pushed to Agent 2's buffer with a win reward
		- The staged experience is pushed to Agent 1's buffer with a reward of a loss, or -reward
		- Break
	- If not terminal, the staged experience is pushed to Agent 1's buffer with its original reward
	- The recent experience is pushed to the staged experience variable
- Both agents run their training methods after the gameplay loop completes
- Every set amount of episodes, the target Q-Network and the epsilon values for the agents are updated
- Repeat for every episode

The purpose for staging the experience until after the next Agent's turn was to account for reverting the reward to a loss if the subsequent Agent's action led to a win

## Performance
After running the Trainer class's run method with two input agents, a model of the Q-Network is created and saved to a file. These models are then loaded into a Computer agent class to decide on an action given a state. The QuartoGUI class creates a graphical gameplay environment between the user and a computer opponent utilizing that model.

- First models
	- Flat binary vector encoding
	- Linear only hidden layers
	- Uniform buffer sampling
	- Single Agent
	- Immediate buffer push

	The original model creations suffered from improper state representation and a malformed training regimen on a single agent. Training was ineffective on unhelpful data points that were primarily composed of intermediary states with no reward. Q-Value outputs from the neural network were virtually identical, leading to an incredibly ineffective player. Most games would result in the computer picking the first space, and first piece it chose.

- Intermediate models
	- One-Hot binary vector encoding
	- Linear only hidden layers
	- Uniform buffer sampling
	- Double Agent
	- Immediate buffer push

	These intermediate models performed differently to the original models, in that actions began to diversify, and no longer chose the first options down the line. However, gameplay from the computer still struggled to display any form of intentional action decisions that truly benefitted its position. The immediate buffer push did not yet incorporate any values for a loss, only for a win. The pieces and positions it shows were seemingly random suggesting insufficient and ineffective training. This was evident when monitoring the loss over time, where there ended up being incredibly high divergence and skyrocketing loss

- Final models
	- Normalized board and piece encoding
	- Convolutional and Linear layers
	- Weighted buffer sampling
	- Double Agent
	- Delayed buffer push

	The final models training script took more time to process, as the data utilized weighted sampling and learning began to function as loss was stabilized. The delayed buffer push also allowed action rewards to account for losses, keeping the next agent's action into account. This appeared to be the case, as gameplay against the model was no longer seemingly random and its much less likely to immediately hand over a win. Gameplay decisions appear to be more intentional, almost appearing to have some level of understanding of the game. However, the model is still incapable of identifying specific winning moves. While the computer seems to postpone its loss, it will completely miss placing a winning piece handed to it. This postponement most often results in an unwinnable state where it is forced to hand over a winning piece to the player.

## Considerations for Improvement
The most significant improvement for Q-Network performance most likely relies in the state representation on input into the network. Despite significant training, the network is still seemingly incapable of identifying specific piece placements in there relationship with each other, as it most likely was not accounted for as one of the many states it had encountered.

The key significance of Quarto lies in the relationship between pieces more than any specific piece placements on the board. When viewing a winning line within a row, the important information lies in the number of pieces, the number of shared traits between those pieces, and their positional relationship to other locations on the board. The exact piece specification has less bearing, and only provides limitations in the networks ability to identify relationships.

Adjusting the encoding of the state to only bring in abstract representations of shared trait and positional relationships across the board would allow for a more abstracted and generalized neural network, and allow it to better analyze states it hasn't seen before. Specific piece placement is less important, and trait and positional alignment are emphasized.

Another improvement would be identifying intermediary rewards in moves that affect these trait and positional relationships. DQNAgents like this one benefit greatly from consistent state-to-state progress. Sparse rewards hinder training speeds and effectiveness, requiring larger batch sizes from the buffer, higher discount levels, and increased layer nodes.

Key moments in this game rely heavily on forward thinking, and analyzing the remaining pieces. Wins can be forced by limiting the leftover available pieces to only ones the create a win when your opponent hands it to you. However, determining the relationships that allow you to identify this and perform the right actions to result in it are incredibly complex. Abstracted relationship based state representations and intermediary rewards that identify patters that lead to these outcomes would greatly improve Q-Network effectiveness.

## Running a Game

Install dependencies
- torch torchvision torchaudio
- tensorboard

To run a graphical instance of a Quarto game against a computer, reference QuartoGUI.py and a specified model with:
```shell
python QuartoGUI.py ./models/<model.model>
```

If no model is specified, `./models/comp.model` containing the most recently trained model will be used.
`ConvulPriorityReducedBuffer.model` is the currently best performing model.

***Important!***
The process has a tendency to hang if the game is exited before gameplay is complete. Avoid exiting the window until after the game is finished. I don't know why this is happening.

Before gameplay begins, the player to go first must be selected. If 'Player' is chosen, the interface will wait for input on which piece will be given to the computer. If 'Computer' is selected, the player will be given a piece to place on the board.

## Training a Model
The training script used to train these models were run from Train2Agent1QNet.py. This creates two separate agents and a single Q-Network for both of them to use.

Modify the top hyperparameters to desired inputs. Specify the name of the model output (currently set to `models/comp.model`). With on Q-Network, one file name is specified. If the training code is modified to reference two different Q-Networks, a second model parameters can be added to save the second agent's model as well with: `trainer.saveModel("comp1.model","comp2.model")`.

## Other examples: Quarto and AI References
- [Alpha Beta Pruning](https://www.researchgate.net/publication/261848662_An_artificial_intelligence_for_the_board_game_%27Quarto%27_in_Java) - Jochen Mohrmann, Michael Neumann, David Duendermann
	- A Negamax α-β pruning attempt, using transposition tables and other techniques to reduce the state space.
	- Intermediary rewards prioritized lines containing more elements with traits in common to speed up game progression and eliminate extra state subtrees.
	- With significant performance impact but a robust approach and transposition table, successful in creating an agent capable of beating most human players.
- [Monte Carlo Tree Search](https://www.superperfundo.dev/articles/quarto-part-2.2) - Barrett Helms
	- A Monte Carlo Tree Search algorithm in response to the inability to define heuristics on intermediary states.
	- Eliminating heuristic requirement through the substitution of training games in a more quick and dirty form of learning
	- Successful to a degree after significant learning time, but not robust to all scenarios
- [Deep Q-Learning Agent](https://github.com/school-of-ai-angers/quarto/blob/master/Reinforcement%20Learning.ipynb) - Alexandre Blouin
	- A different approach to Deep Q-Learning Agents and Quarto.
	- Simplified and more straightforward than this implementation.
	- Robust match based setup and larger reward results provided more effective training.
	- Continuous training per action sequence rather than training across replay buffer sampling with much more forward movement in ability
- [An Exploration of Gameplay in Quarto](https://www.slideshare.net/slideshow/quarto-55043713/55043713) - Matthew Kerner
	- Paper disussing different approaches to creating an AI agent for quarto gameplay.
	- Analysis of mathematics behind state representation and state symmetries.

## Other References
- [Deep Q-Learning Description, Setup, and Training Algorithm](https://www.mathworks.com/help/reinforcement-learning/ug/dqn-agents.html) - MathWorks
- [Deep Q-Learning Example](https://nbviewer.org/github/nathanmargaglio/Deep-Q-Network/blob/master/DQN.ipynb) - Nathan Margaglio
- [Deep Q-Learning Agent Creation Walkthrough](https://www.youtube.com/watch?v=qfovbG84EBg) - Harrison Kinsley
- [Neural Network Description and Use Cases](https://machinelearningmastery.com/develop-your-first-neural-network-with-pytorch-step-by-step/) - Adrian Tam
- ChatGPT