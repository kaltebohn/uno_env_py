import json

from game.consts import NUM_OF_PLAYERS
from agent.random_agent import RandomAgent
from agent.better_random_agent import BetterRandomAgent
from agent.mcts_agent import MCTSAgent
from uno_env import UnoEnv

env = UnoEnv()
agent = MCTSAgent()
opponents = [BetterRandomAgent() for _ in range(NUM_OF_PLAYERS - 1)]

current_agent_idx, observation = env.reset()

state_log = []

while True:
    if current_agent_idx == 0:
        action = agent.get_action(observation)
    else:
        action = opponents[current_agent_idx - 1].get_action(observation)
    current_agent_idx, next_observation, reward, done = env.step(action)

    if done:
        break

    observation = next_observation

    # 状態のログを取る。形式はuno_state_viewerに準拠。
    state_log.append(env.state.to_dict())

# 状態の履歴をJSON形式で出力。
# print(json.dumps(state_log, default=str))
print(env.state.player_scores())
