from copy import deepcopy

from game.state import State


class UnoEnv:
    """
    強化学習における環境。
    Stateクラスを保持する。
    エージェントとのやり取りを行う。
    プレイヤ番号は0で固定。
    """

    def __init__(self):
        """ゲームの初期化。
        """
        self.player_number = 0
        self.agent_state = State()

    def legal_actions(self) -> list:
        """現在の状態で合法な行動集合を返す。

        Returns:
            list: 合法な行動のリスト。
        """
        if self.player_number != self.agent_state.current_player:
            return []
        return self.agent_state.legal_actions()

    def next_state(self, state: State, action) -> State:
        """与えられた状態で与えられた行動を取った際の次状態を返す。

        Args:
            state (State): 現在状態。
            action (_type_): 現在状態で取る行動。

        Returns:
            State: 次状態。
        """
        return state.next(action)

    def reward(self, state: State, action, next_state: State) -> int:
        """報酬関数。

        Args:
            state (State): 現在状態。UNOでは不要だが、一般的な報酬関数の定義に合わせて用意。
            action (_type_): 取る行動。UNOでは不要だが、一般的な報酬関数の定義に合わせて用意。
            next_state (State): 次状態。

        Returns:
            int: 次状態に遷移したとき得られた報酬・
        """
        return next_state.player_scores()[self.player_number]

    def reset(self):
        """ゲームの状態を初期化。
        """
        self.agent_state = State()

    def step(self, action):
        """与えられた行動を適用して状態遷移を行い、エージェントに結果を与える。

        Args:
            action (_type_): 取る行動。

        Returns:
            _type_: [観測、報酬、ゲームが終了したか？]のリスト。UNOは不完全情報ゲームなので、エージェントは状態ではなく観測を与えられる。
        """
        state = deepcopy(self.agent_state)
        next_state = self.next_state(state, action)
        reward = self.reward(state, action, next_state)
        done = next_state.is_finished()

        self.agent_state = next_state
        return next_state.player_observation(self.player_number), reward, done
