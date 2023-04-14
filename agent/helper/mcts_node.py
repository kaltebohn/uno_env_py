from os import urandom
import numpy as np
import random
from game.state import State
from game.consts import NUM_OF_PLAYERS


class MCTSNode:
    EXPAND_THRESHOLD = 1  # この値以上探索した場合は子節点を展開。
    SEARCH_LIMIT = 100  # この値以上は探索しない。
    EVALUATION_MAX = 10000

    def __init__(self, state: State, seed: int, last_action=None) -> None:
        self.state = state
        self.random_engine = random.Random(seed)
        self.last_action = last_action
        self.children: list[MCTSNode] = []

        # 探索を通じて保持する、節点の評価値にかかわる値。
        self.visit_cnt = 0
        self.sum_scores = np.zeros(NUM_OF_PLAYERS)
        self.sum_squared_scores = np.zeros(NUM_OF_PLAYERS)

    def search(self):
        whole_search_cnt = 0

        # 子ノードを生成。
        self._expand()

        # ここで引っかかったらロジックがおかしい。
        assert len(self.children) > 0

        # 手がひとつしかないなら、それを出す。
        if len(self.children) == 1:
            return self.children[0].last_action

        # 回数に制限をかけて探索。
        while whole_search_cnt < MCTSNode.SEARCH_LIMIT:
            whole_search_cnt += 1
            self._search_child(whole_search_cnt)

        # 累計得点が最大の手を貪欲に選んで返す。
        # TODO: 探索を重ねるごとにより有効なパスを選ぶようになるので、定数重みをかけて、直近のものの値ほど大きくするのもいいかも。
        return max(self.children, key=lambda node: node.sum_scores)

    def _search_child(self, whole_search_cnt: int):
        self.visit_cnt += 1

        # 既にゲームが終了していたら、その結果を返す。
        result = np.array(self.state.player_scores(), dtype=float)
        if self.state.is_finished():
            self._reflect_search_result(result)
            return result

        # 子節点がなく、十分この節点を探索した場合は、展開する。
        if len(self.children) <= 0 and self.visit_cnt > MCTSNode.EXPAND_THRESHOLD:
            self._expand()

        if len(self.children) > 0:
            # 子節点があれば、選択して探索し、結果を返す。evaluate()が最大のものを選ぶ。
            child_node = max(self.children, key=lambda node: node._evaluate(whole_search_cnt))
            result = np.array(child_node._search_child(whole_search_cnt), dtype=float)
            self._reflect_search_result(result)
            return result
        else:
            # 子節点がなければ、プレイアウトを行い結果を返す。
            result = np.array(self._playout(), dtype=float)
            self._reflect_search_result(result)
            return result

    def _expand(self):
        actions_and_next_states = [[action, self.state.next(action)] for action in self.state.legal_actions()]
        self.children = [MCTSNode(next_state, urandom(16), action) for action, next_state in actions_and_next_states]

    def _playout(self):
        state = self.state

        while not state.is_finished():
            state = state.next(random.choice(state.legal_actions()))

        return state.player_scores()

    def _evaluate(self, whole_search_cnt: int):
        if self.visit_cnt <= 0:
            return [0 for _ in range(NUM_OF_PLAYERS)]
        else:
            # UCB1
            # return self.sum_scores / self.visit_cnt + np.sqrt(2 * np.log2(whole_search_cnt) / self.visit_cnt)

            # UCB1-Tuned
            mean = self.sum_scores / self.visit_cnt
            variance = self.sum_squared_scores - mean ** 2
            v = variance + np.sqrt(2.0 * np.log2(whole_search_cnt) / self.visit_cnt)
            return self.sum_scores / self.visit_cnt + np.sqrt(np.log2(whole_search_cnt) / self.visit_cnt * min(0.25, v))

    def _reflect_search_result(self, result: np.ndarray):
        self.sum_scores += result
        self.sum_squared_scores += result**2
