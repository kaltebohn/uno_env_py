import numpy as np


class RandomAgent:
    """ランダムな行動を取るだけのエージェント。パスやチャレンジもランダムに行うのでゲームが終わらない可能性がある。
    """
    def get_action(self, observation: dict):
        """行動を選ぶ。

        Args:
            observation (dict): 環境から与えられる観測。

        Returns:
            _type_: 選択した行動。
        """
        # ここで引っかかったらロジックがおかしい。
        assert len(observation["legal_actions"]) > 0

        return np.random.choice(observation["legal_actions"])
