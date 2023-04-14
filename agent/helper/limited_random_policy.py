import random
from game.action_type import ActionType


def limited_random_policy(legal_actions: list, action_type: ActionType, random_engine: random.Random):
    """行動を選ぶ。

    Args:
        observation (dict): 環境から与えられる観測。
        random_engine (random.Random): 乱数生成器。

    Returns:
        _type_: 選択した行動。
    """
    # ここで引っかかったらロジックがおかしい。
    assert len(legal_actions) > 0

    actions: list = legal_actions

    if len(actions) == 1:
        return actions[0]

    # 本当にランダムに選ぶとゲームが終わらないので、パス出しとチャレンジは制限する。
    if action_type in [ActionType.SUBMISSION, ActionType.SUBMISSION_OF_DRAWN_CARD]:
        idx = [i for i, card in enumerate(actions) if card.is_empty()][0]
        del actions[idx]
    elif action_type == ActionType.CHALLENGE:
        return False  # チャレンジはしない。

    return random_engine.choice(actions)
