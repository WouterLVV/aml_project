from Network.Network import DQNetwork
from logic.simulator import Simulator
from ai.ml_agent import ml_agent
from logic.agent import RandomAI
import time


start_time = time.time()

neural_network = DQNetwork(161, 52, [100, 100, 100], ['sigmoid', 'sigmoid', 'sigmoid', 'sigmoid'], 0.1)
players = [ml_agent(neural_network), ml_agent(neural_network), ml_agent(neural_network), ml_agent(neural_network)]
simulator = Simulator(players=players, number_of_games_per_cycle=20, number_of_update_cycles=100, neural_network=neural_network, update_rate=1)
simulator.run_cycles()

end_time = time.time()
print(end_time-start_time)
