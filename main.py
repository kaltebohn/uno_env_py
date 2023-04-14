import json
import os
import random

from game.consts import NUM_OF_PLAYERS
from agent.random_agent import RandomAgent
from agent.limited_random_agent import LimitedRandomAgent
from agent.mcts_agent import MCTSAgent
from uno_env import UnoEnv

state_log = []

while 1000:
    env = UnoEnv()
    agent = MCTSAgent()
    # agent = LimitedRandomAgent(random.Random(os.urandom(16)))
    opponents = [LimitedRandomAgent(random.Random(os.urandom(16))) for _ in range(NUM_OF_PLAYERS - 1)]

    current_agent_idx, observation = env.reset()

    while True:
        if current_agent_idx == 0:
            # print('--------------------')
            action = agent.get_action(observation)
        else:
            action = opponents[current_agent_idx - 1].get_action(observation)
        current_agent_idx, next_observation, reward, done = env.step(action)

        if done:
            break

        observation = next_observation

        # 状態のログを取る。形式はuno_state_viewerに準拠。
        # state_log.append(env.state.to_dict())

    # 状態の履歴をJSON形式で出力。
    # print(json.dumps(state_log, default=str))
    print(env.state.player_scores())
