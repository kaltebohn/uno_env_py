class UnoEnv:
    """
    強化学習における環境。
    Gameクラスを保持する。
    エージェントとのやり取りを行う。
    """

    def __init__(self):
        pass
    
    def legal_actions(self):
        pass

    def next_state(self, state, action):
        pass

    def reward(self, state, action, next_state):
        pass

    def reset(self):
        pass
    
    def step(self, action):
        pass
