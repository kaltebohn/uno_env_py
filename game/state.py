from __future__ import annotations
from copy import deepcopy
import random

from . import action_type, card, consts


class State:
    """UNOのある時点を表す状態。
    """
    def __init__(self, seed=0) -> None:
        """ゲーム開始時の状態にする。

        Args:
            seed (int, optional): 乱数シード値。初期値0。
        """
        # ランダム性に影響されないメンバ変数を初期化。
        self.discards = []
        self.prev_player = None
        self.is_normal_order = True

        # 山札生成・席順シャッフルに必要な乱数生成器。
        self.random_engine = random.Random(seed)

        # 山札を生成。
        self.initialize_deck(True)

        # 山札から手札を各プレイヤに配る。
        self.player_hands: list[list[card.Card]] = []
        for _ in range(consts.NUM_OF_PLAYERS):
            self.player_hands.append(self.deck[:consts.NUM_OF_FIRST_HAND])
            self.deck = self.deck[consts.NUM_OF_FIRST_HAND:]

        # 席順をシャッフルし、席0のプレイヤを最初のプレイヤとする。
        self.player_seats = list(range(consts.NUM_OF_PLAYERS))
        self.random_engine.shuffle(self.player_seats)
        self.current_player = self.player_seats.index(0)

        # 場のカードを決める。
        while True:
            tmp_card: card.Card = self.deck[0]
            # ワイルドドロー4、シャッフルワイルド、白いワイルドなら仕切り直し。
            if tmp_card == card.Card.wild_draw_4() or tmp_card == card.Card.wild_shuffle_hands() or tmp_card == card.Card.wild_customizable():
                self.initialize_deck(True)
                continue
            else:
                self.update_table_card(tmp_card)
                self.discards.append(tmp_card)
                self.deck = self.deck[1:]
                break

        # 場のカードの効果を反映させる。
        self.action_type = action_type.ActionType.SUBMISSION
        if self.table_number != card.Number.NONE:
            # 数字カード: 何もしない。
            pass
        elif self.table_action == card.Action.DRAW_TWO:
            # ドロー2: 最初のプレイヤがカードを2枚引き、次のプレイヤに手番が移る。
            self.draw(self.current_player, 2)
            self.current_player = self.next_player_of(self.current_player)
        elif self.table_action == card.Action.REVERSE:
            # リバース: 手番が逆順になり、本来最後の手番だったプレイヤが最初のプレイヤになる。
            self.is_normal_order = False
            self.current_player = self.next_player_of(self.current_player)
        elif self.table_action == card.Action.SKIP:
            # スキップ: 最初のプレイヤが手番を飛ばされる。
            self.current_player = self.next_player_of(self.current_player)
        elif self.table_action == card.Action.WILD:
            # ワイルド: 最初のプレイヤが色を宣言する。
            self.action_type = action_type.ActionType.COLOR_CHOICE
        else:
            # ここに到達した場合はロジックが誤っている。
            assert False

    def next(self, action) -> State:
        # ラウンドが終わっていたら状態遷移しない。
        if self.is_finished():
            return deepcopy(self)

        # 次状態。この状態を順次書き換えて返す。
        next_state = deepcopy(self)

        # 次状態でのprev_playerは原則現在プレイヤにすればよいのでここで前もって更新。
        next_state.prev_player = self.current_player

        if self.action_type == action_type.ActionType.COLOR_CHOICE:
            # 不正な色を選択する利点がないので、不正な色ならプレイヤを修正するということで。
            assert action in [card.Color.BLUE, card.Color.GREEN, card.Color.RED, card.Color.YELLOW]

            next_state.table_color = action
            next_state.current_player = self.next_player_of(self.current_player)

            # ワイルドドロー4が出ていた場合、色選択後にチャレンジが発生する。
            next_state.action_type = action_type.ActionType.CHALLENGE if self.table_action == card.Action.WILD_DRAW_4 else action_type.ActionType.SUBMISSION

            return next_state

        if self.action_type == action_type.ActionType.CHALLENGE:
            # ここに引っかかったらロジックがおかしい。
            assert self.prev_player is not None

            # チャレンジ後は必ず提出。
            next_state.action_type = action_type.ActionType.SUBMISSION

            challenging_player = self.current_player
            challenged_player = self.prev_player

            # チャレンジしなかったら、チャレンジするプレイヤに4枚引かせて飛ばす。
            if not action:
                next_state.change_turn_forward()
                next_state.draw(challenging_player, 4)
                return next_state

            # チャレンジが成功したか判定する。
            prev_table_card = self.discards[-2]
            challenged_player_hand = self.player_hands[challenged_player]
            is_challenge_succeeded =\
                any([card.action != card.Action.WILD_DRAW_4 and card.is_legal(prev_table_card) for card in challenged_player_hand])

            if is_challenge_succeeded:
                # チャレンジが成功したら、チャレンジされたプレイヤのカードを場から戻し、4枚引かせ、手番を戻す。

                # 場のカードをチャレンジされたプレイヤに戻す。
                next_state.player_hands[challenged_player].append(self.discards[-1])
                next_state.update_table_card(prev_table_card)
                next_state.discards = next_state.discards[:-1]

                # チャレンジされたプレイヤに4枚引かせる。
                next_state.draw(challenged_player, 4)

                # 手番を戻す。
                next_state.current_player = challenged_player
                next_state.prev_player = challenging_player
            else:
                # チャレンジが失敗したら、今のプレイヤに6枚引かせて飛ばす。
                next_state.change_turn_forward()
                next_state.draw(challenging_player, 6)

            return next_state

        if self.action_type == action_type.ActionType.SUBMISSION_OF_DRAWN_CARD:
            if action.color == card.Color.NONE:
                # パスなら、次の手番に移す。
                next_state.action_type = action_type.ActionType.SUBMISSION
                next_state.change_turn_forward()
                return next_state
            else:
                # パスでなければ、引いたカードであることだけ確認して残りは提出の処理に任せる。
                # 違法な着手をする利点がないので、ここで止まったらプレイヤを修正するということで。
                assert action == self.player_hands[self.current_player][-1]

        # 以下提出の処理。

        # パスなら、カードを1枚引かせて、引いたカードの提出に移る。
        if action.is_empty():
            next_state.action_type = action_type.ActionType.SUBMISSION_OF_DRAWN_CARD
            next_state.draw(self.current_player, 1)
            return next_state

        # 合法性の確認。違法な着手をする利点がないので、ここで止まったらプレイヤを修正するということで。
        assert action in self.player_hands[self.current_player] and action.is_legal(self.table_card())

        # カードを場に出す。
        next_state.accept_submission(self.current_player, action)

        next_state.action_type = action_type.ActionType.SUBMISSION
        if action.number != card.Number.NONE:
            # 数字カードなら特別なことはしない。
            next_state.change_turn_forward()
        elif action.action == card.Action.DRAW_TWO:
            # ドロー2: 次の人に2枚引かせて飛ばす。
            next_state.draw(self.next_player_of(self.current_player), 2)
            next_state.change_turn_forward()
            next_state.change_turn_forward()
        elif action.action == card.Action.REVERSE:
            # リバース: 順番を変える。
            next_state.is_normal_order = not self.is_normal_order
            next_state.change_turn_forward()
        elif action.action == card.Action.SKIP:
            # スキップ: 次のプレイヤを飛ばす。
            next_state.change_turn_forward()
            next_state.change_turn_forward()
        elif action.action == card.Action.WILD:
            # ワイルド: 色選択に移る。
            next_state.action_type = action_type.ActionType.COLOR_CHOICE
        elif action.action == card.Action.WILD_CUSTOMIZABLE:
            # 白いワイルド: 特別ルール。未実装。
            assert False
        elif action.action == card.Action.WILD_DRAW_4:
            # ワイルドドロー4: 色選択に移る。チャレンジへの遷移は色選択時に行われる。
            next_state.action_type = action_type.ActionType.COLOR_CHOICE
        elif action.action == card.Action.WILD_SHUFFLE_HANDS:
            # シャッフルワイルド: 色選択に移る。手札をまとめて次プレイヤから順に再分配。

            # ゲームが終了していたら処理しない。
            if self.is_finished():
                return next_state

            next_state.action_type = action_type.ActionType.COLOR_CHOICE

            collected_cards = []
            for i in range(consts.NUM_OF_PLAYERS):
                collected_cards += self.player_hands[i]
                next_state.player_hands[i] = []
            self.random_engine.shuffle(collected_cards)

            player = self.next_player_of(self.current_player)
            for card in collected_cards:
                next_state.player_hands[player].append(card)
                player = self.next_player_of(player)

            next_state.change_turn_forward()

        return next_state

    def legal_actions(self) -> list:
        if self.is_finished():
            return []

        if self.action_type == action_type.ActionType.SUBMISSION:
            # 提出できるカードとパスを返す。
            hand = self.player_hands[self.current_player]
            return [card for card in hand if card.is_legal(self.table_card())] + [card.Card.empty()]
        elif self.action_type == action_type.ActionType.SUBMISSION_OF_DRAWN_CARD:
            # 引いたカードが合法なら選択肢に加える。パスは常に選べる。
            drawn_card = self.player_hands[self.current_player][-1]
            return [drawn_card, card.Card.empty()] if drawn_card.is_legal(self.table_card()) else [card.Card.empty()]
        elif self.action_type == action_type.ActionType.COLOR_CHOICE:
            return [card.Color.BLUE, card.Color.GREEN, card.Color.RED, card.Color.YELLOW]
        elif self.action_type == action_type.ActionType.CHALLENGE:
            return [True, False]
        else:
            # ここに到達した場合はロジックが誤っている。
            assert False

    def is_finished(self) -> bool:
        """ラウンドが終わったか？

        Returns:
            bool: ラウンドが終わっていたらTrue、終わっていなければFalse。
        """
        return any([len(player_hand) == 0 for player_hand in self.player_hands])

    def player_scores(self) -> list[int]:
        """各プレイヤの得点をリストで返す。

        Returns:
            list[int]: 各プレイヤの得点。プレイヤ番号をインデックスとしてアクセス。
        """
        scores = [0 for _ in range(consts.NUM_OF_PLAYERS)]
        sum_score = 0
        if not self.is_finished():
            return scores

        # 勝者以外のプレイヤの得点を決めつつ、勝者に渡す得点sum_scoreを計算。
        for i in range(consts.NUM_OF_PLAYERS):
            if len(self.player_hands[i]) == 0:
                winner = i
                continue
            score = sum(card.to_score() for card in self.player_hands[i])
            scores[i] = -score
            sum_score += score
        # 勝者は勝者以外のプレイヤに課された減点の総和を受け取る。
        scores[winner] = sum_score

        return scores

    def player_observation(self, player: int):
        """特定のプレイヤにUNOのルール上見せられる情報を返す。

        Args:
            player (int): 情報を見るプレイヤ。

        Returns:
            dict: プレイヤに見せる情報。
        """
        return {
            "discards": self.discards,
            "player_hand": self.player_hands[player],
            "player_hand_qtys": [len(hand) for hand in self.player_hands],
            "player_seats": self.player_seats,
            "player_scores": self.player_scores(),
            "action_type": self.action_type,
            "prev_player": self.prev_player,
            "current_player": self.current_player,
            "is_normal_order": self.is_normal_order,
            "table_card": self.table_card(),
            "legal_actions": self.legal_actions() if player == self.current_player else []
        }

    def draw(self, player, quantity) -> None:
        """プレイヤにカードを引かせる。

        Args:
            player (int): カードを引かせるプレイヤの番号。
            quantity (int): 引くカードの枚数。
        """
        # 山札から必要分配れるならそのまま処理を返す。
        if quantity <= len(self.deck):
            self.player_hands[player] += self.deck[:quantity]
            self.deck = self.deck[quantity:]
            return

        # まず、山札の残りをすべて配る。
        self.player_hands[player] += self.deck
        rest_quantity = quantity - len(self.deck)
        self.deck = []

        # 捨て札を山札に戻して、配る。
        self.reshuffle_deck_from_discard()
        if len(self.deck) < rest_quantity:
            # 山札も捨て札も使い切る場合は手札を持ちすぎているプレイヤがいるので、そちらを何とかするべき。
            assert False
        self.player_hands[player] += self.deck[:rest_quantity]
        self.deck = self.deck[rest_quantity:]

    def next_player_of(self, player: int) -> int:
        """次の手番のプレイヤの番号。現在の席、周り順を考慮する。

        Args:
            player (int): 基準となるプレイヤの番号。

        Returns:
            int: 基準となるプレイヤの次のプレイヤの番号。
        """
        if self.is_normal_order:
            next_seat = (self.player_seats[player] + 1) % consts.NUM_OF_PLAYERS
        else:
            next_seat = (self.player_seats[player] - 1 + consts.NUM_OF_PLAYERS) % consts.NUM_OF_PLAYERS
        return self.player_seats[next_seat]

    def reshuffle_deck_from_discard(self) -> None:
        """捨て札を山札に戻して山札を再構成する。
        """
        if len(self.deck) > 0 or len(self.discards) <= 0:
            # ここに到達した場合はロジックが誤っている。
            assert False

        self.deck = self.discards
        self.random_engine.shuffle(self.deck)
        self.discards = []

    def change_turn_forward(self) -> None:
        """次のプレイヤに手番を移す。現在の席・周り順を考慮。prev_playerは「前に行動をしたプレイヤ」なのでここで変えない。
        """
        self.current_player = self.next_player_of(self.current_player)

    def table_card(self) -> card.Card:
        """場の状態に対応するカードを返す。ワイルドカードなどの場合は色がWILDとは限らない。

        Returns:
            Card: 場の状態に対応するカード。
        """
        return card.Card(self.table_color, self.table_number, self.table_action)

    def update_table_card(self, new_table_card: card.Card) -> None:
        """受け取ったカードの情報で場札の情報を更新。

        Args:
            new_table_card (Card): 新しい場札。
        """
        self.table_color = new_table_card.color
        self.table_number = new_table_card.number
        self.table_action = new_table_card.action

    def accept_submission(self, player: int, card: card.Card) -> None:
        """プレイヤの提出を受理する。カード毎の特殊効果は反映させない。

        Args:
            player (int): カードを提出するプレイヤ。
            card (Card): 提出するカード。
        """
        # ここで引っかかったらロジックがおかしい。
        assert card in self.player_hands[player]

        self.update_table_card(card)
        self.discards.append(deepcopy(card))
        idx = self.player_hands[player].index(card)
        del self.player_hands[player][idx]

    def to_dict(self) -> dict:
        """uno_state_viewerに合わせた形式の辞書を返す。

        Returns:
            dict: 現在状態から生成した辞書。
        """
        return {
            "deck": [str(card) for card in self.deck],
            "discards": [str(card) for card in self.discards],
            "playerCards": [[str(card) for card in player_hand] for player_hand in self.player_hands],
            "playerSeats": self.player_seats,
            "playerScores": self.player_scores(),
            "currentMoveType": self.action_type.value,
            "prevPlayer": self.prev_player,
            "currentPlayer": self.current_player,
            "isNormalOrder": self.is_normal_order,
            "tableColor": self.table_color,
            "tablePattern": self.table_number if self.table_number != card.Number.NONE else self.table_action,
            "drawnCard": self.player_hands[self.current_player][-1]
        }

    def initialize_deck(self, is_shuffled: bool) -> None:
        """UNOのルールに従った構成の山札を生成。

        Args:
            is_shuffled (bool): 山札をシャッフルする？
        """
        self.deck = [
            card.Card.blue_zero(),
            card.Card.blue_one(),
            card.Card.blue_one(),
            card.Card.blue_two(),
            card.Card.blue_two(),
            card.Card.blue_three(),
            card.Card.blue_three(),
            card.Card.blue_four(),
            card.Card.blue_four(),
            card.Card.blue_five(),
            card.Card.blue_five(),
            card.Card.blue_six(),
            card.Card.blue_six(),
            card.Card.blue_seven(),
            card.Card.blue_seven(),
            card.Card.blue_eight(),
            card.Card.blue_eight(),
            card.Card.blue_nine(),
            card.Card.blue_nine(),
            card.Card.blue_draw_two(),
            card.Card.blue_draw_two(),
            card.Card.blue_reverse(),
            card.Card.blue_reverse(),
            card.Card.blue_skip(),
            card.Card.blue_skip(),

            card.Card.green_zero(),
            card.Card.green_one(),
            card.Card.green_one(),
            card.Card.green_two(),
            card.Card.green_two(),
            card.Card.green_three(),
            card.Card.green_three(),
            card.Card.green_four(),
            card.Card.green_four(),
            card.Card.green_five(),
            card.Card.green_five(),
            card.Card.green_six(),
            card.Card.green_six(),
            card.Card.green_seven(),
            card.Card.green_seven(),
            card.Card.green_eight(),
            card.Card.green_eight(),
            card.Card.green_nine(),
            card.Card.green_nine(),
            card.Card.green_draw_two(),
            card.Card.green_draw_two(),
            card.Card.green_reverse(),
            card.Card.green_reverse(),
            card.Card.green_skip(),
            card.Card.green_skip(),

            card.Card.red_zero(),
            card.Card.red_one(),
            card.Card.red_one(),
            card.Card.red_two(),
            card.Card.red_two(),
            card.Card.red_three(),
            card.Card.red_three(),
            card.Card.red_four(),
            card.Card.red_four(),
            card.Card.red_five(),
            card.Card.red_five(),
            card.Card.red_six(),
            card.Card.red_six(),
            card.Card.red_seven(),
            card.Card.red_seven(),
            card.Card.red_eight(),
            card.Card.red_eight(),
            card.Card.red_nine(),
            card.Card.red_nine(),
            card.Card.red_draw_two(),
            card.Card.red_draw_two(),
            card.Card.red_reverse(),
            card.Card.red_reverse(),
            card.Card.red_skip(),
            card.Card.red_skip(),

            card.Card.yellow_zero(),
            card.Card.yellow_one(),
            card.Card.yellow_one(),
            card.Card.yellow_two(),
            card.Card.yellow_two(),
            card.Card.yellow_three(),
            card.Card.yellow_three(),
            card.Card.yellow_four(),
            card.Card.yellow_four(),
            card.Card.yellow_five(),
            card.Card.yellow_five(),
            card.Card.yellow_six(),
            card.Card.yellow_six(),
            card.Card.yellow_seven(),
            card.Card.yellow_seven(),
            card.Card.yellow_eight(),
            card.Card.yellow_eight(),
            card.Card.yellow_nine(),
            card.Card.yellow_nine(),
            card.Card.yellow_draw_two(),
            card.Card.yellow_draw_two(),
            card.Card.yellow_reverse(),
            card.Card.yellow_reverse(),
            card.Card.yellow_skip(),
            card.Card.yellow_skip(),

            card.Card.wild(),
            card.Card.wild(),
            card.Card.wild(),
            card.Card.wild(),
            card.Card.wild_draw_4(),
            card.Card.wild_draw_4(),
            card.Card.wild_draw_4(),
            card.Card.wild_draw_4(),
            card.Card.wild_shuffle_hands(),
            # card.Card.wild_customizable(),
            # card.Card.wild_customizable(),
            # card.Card.wild_customizable()
        ]

        if is_shuffled:
            self.random_engine.shuffle(self.deck)
