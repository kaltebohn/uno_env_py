import json

from game.consts import NUM_OF_PLAYERS
from random_agent import RandomAgent
from uno_env import UnoEnv

env = UnoEnv()
agents = [RandomAgent() for _ in range(NUM_OF_PLAYERS)]

current_agent_idx, observation = env.reset()

state_log = []

while True:
    action = agents[current_agent_idx].get_action(observation)
    current_agent_idx, next_observation, reward, done = env.step(action)

    if done:
        break

    observation = next_observation

    # 状態のログを取る。形式はuno_state_viewerに準拠。
    state_log.append(env.state.to_dict())

# 状態の履歴をJSON形式で出力。
print(json.dumps(state_log, default=str))
# print(env.state.player_scores())
