from game.consts import NUM_OF_PLAYERS
from random_agent import RandomAgent
from uno_env import UnoEnv

env = UnoEnv()
agents = [RandomAgent() for _ in range(NUM_OF_PLAYERS)]

current_agent_idx, observation = env.reset()

while True:
    action = agents[current_agent_idx].get_action(observation)
    current_agent_idx, next_observation, reward, done = env.step(action)

    if done:
        break

    observation = next_observation

print(env.state.player_scores())
