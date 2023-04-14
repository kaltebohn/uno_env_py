from .helper.limited_random_policy import limited_random_policy


class LimitedRandomAgent:
    """ランダムな行動を取るだけのエージェント。ゲームを進行するため一部行動を制限。
    """
    def __init__(self, random_engine):
        self.random_engine = random_engine

    def get_action(self, observation: dict):
        """行動を選ぶ。

        Args:
            observation (dict): 環境から与えられる観測。

        Returns:
            _type_: 選択した行動。
        """
        return limited_random_policy(observation["legal_actions"], observation["action_type"], self.random_engine)
