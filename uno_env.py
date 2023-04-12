from copy import deepcopy
from os import urandom

from game.state import State


class UnoEnv:
    """
    強化学習における環境。
    Stateクラスを保持する。
    エージェントとのやり取りを行う。
    """

    def __init__(self):
        """ゲームの初期化。
        """
        self.state = State(urandom(16)) # 128ビットの乱数を渡す。
        self.current_agent = self.state.current_player

    def legal_actions(self) -> list:
        """現在の状態で合法な行動集合を返す。

        Returns:
            list: 合法な行動のリスト。
        """
        return self.state.legal_actions()

    def next_state(self, state: State, action) -> State:
        """与えられた状態で与えられた行動を取った際の次状態を返す。

        Args:
            state (State): 現在状態。
            action (_type_): 現在状態で取る行動。

        Returns:
            State: 次状態。
        """
        return state.next(action)

    def reward(self, state: State, action, next_state: State) -> list[int]:
        """報酬関数。

        Args:
            state (State): 現在状態。UNOでは不要だが、一般的な報酬関数の定義に合わせて用意。
            action (_type_): 取る行動。UNOでは不要だが、一般的な報酬関数の定義に合わせて用意。
            next_state (State): 次状態。

        Returns:
            int: 次状態に遷移したとき得られた報酬のリスト。
        """
        return next_state.player_scores()

    def reset(self):
        """ゲームの状態を初期化して最初の観測を返す。

        Returns:
            int, dict: 最初のエージェントの添え字、最初のエージェントの観測。
        """
        self.state = State()
        self.current_agent = self.state.current_player
        return self.current_agent, self.state.player_observation(self.current_agent)

    def step(self, action):
        """与えられた行動を適用して状態遷移を行い、エージェントに結果を与える。

        Args:
            action (_type_): 取る行動。

        Returns:
            _type_: [現在のエージェントの添え字、観測、報酬、ゲームが終了したか？]のリスト。UNOは不完全情報ゲームなので、エージェントは状態ではなく観測を与えられる。
        """
        state = deepcopy(self.state)
        next_state = self.next_state(state, action)
        reward = self.reward(state, action, next_state)
        done = next_state.is_finished()

        self.state = next_state
        self.current_agent = self.state.current_player
        # print(next_state.player_observation(self.current_agent))
        print("====================")
        for i in range(4):
            print("----------------")
            for card in self.state.player_hands[i]:
                print(card)
        return self.current_agent, next_state.player_observation(self.current_agent), reward, done
