import os
from .helper.mcts_node import MCTSNode
from .helper.state_estimator import observation2state


class MCTSAgent:
    """モンテカルロ木探索を用いるエージェント。
    """
    def __init__(self):
        pass

    def get_action(self, observation):
        return MCTSNode(observation2state(observation), os.urandom(16)).search()

    def update(self, state, action, reward, done):
        pass
