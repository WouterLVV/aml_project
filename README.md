# Machines playing the Game of Hearts
Teaching a computer to play the game of hearts with reinforcement learning using deep Q learning.
## How to run
Run main.py for playing games with and training the neural network. 

The variable `load_previously_trained_network` decides whether a previously trained network should be used. This is helpful when additional training is required on the same network or work has been interrupted.

## Neural Network
The neural network is written in such a way that any number of hidden layers and activation functions, given that tensorflow has implemented the activation functions. The inputs and output sizes of the layers will be adapted such that they work with the given input, output, and hidden layer sizes.

## Simulator
Games are simulated using the `Simulator` class. Each `Simulator` instance needs to know how many games it needs to play for each cycle(epoch), how many cycles, and with which players. The `RandomSimulator` class is a `Simulator` with preset bots.

## Players
Each player is an instance of `Agent`. `Agent` has the basic functions/logic a player needs to be able play the game. There are 4 classes that inherit from `Agent`: 
 - `ml_agent`, agent using the trained neural network
 - `HumanPlayer`, agent a human player can control
 - `RandomAI`, agent that depending on its initialization playes either a random card from its hand or a random card from the deck.
 - `YoloAI`, agent that plays a random valid card
## The Game
The game logic has been encoded in the class `Hearts` and `Round`. Each `Hearts` instance will be assigned  

## Cards and decks
Each `Card` has a `Suit` and a `Rank`. We have used operator overloading to define a the relation between cards. A `Deck` consists of a list of `cards`. The variable `SMALLDECK` refers to a deck for the simplified version of the game of Hearts with 24 cards and 3 suits, whereas the variable `STANDARDDECK` refers to the usuals deck with 52 cards and 4 suits.