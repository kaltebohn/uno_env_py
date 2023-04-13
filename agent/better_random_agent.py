import numpy as np
from game.action_type import ActionType


class BetterRandomAgent:
    """ランダムな行動を取るだけのエージェント。ゲームを進行するため一部行動を制限。
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

        actions: list = observation["legal_actions"]

        if len(actions) == 1:
            return actions[0]

        # 本当にランダムに選ぶとゲームが終わらないので、パス出しとチャレンジは制限する。
        if observation["action_type"] in [ActionType.SUBMISSION, ActionType.SUBMISSION_OF_DRAWN_CARD]:
            idx = [i for i, card in enumerate(actions) if card.is_empty()][0]
            del actions[idx]
        elif observation["action_type"] == ActionType.CHALLENGE:
            return False  # チャレンジはしない。

        return np.random.choice(actions)
