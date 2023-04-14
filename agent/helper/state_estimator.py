import os
import random
from game.card import Card
from game.consts import NUM_OF_PLAYERS
from game.state import State

def observation2state(observation):
    # わかっていない情報を推定。
    deck, player_hands = deal_randomly(observation["current_player"], observation["player_hand"], observation["discards"], observation["player_hand_qtys"])

    # 観測と推定結果から状態を生成。
    state = State()
    state.random_engine = random.Random(16)
    state.deck = deck
    state.discards = observation["discards"]
    state.player_hands = player_hands
    state.player_seats = observation["player_seats"]
    state.action_type = observation["action_type"]
    state.prev_player = observation["prev_player"]
    state.current_player = observation["current_player"]
    state.is_normal_order = observation["is_normal_order"]
    state.table_color = observation["table_card"].color
    state.table_number = observation["table_card"].number
    state.table_action = observation["table_card"].action

    return state


def deal_randomly(my_player_num: int, my_hand: list[Card], discards: list[Card], player_hand_qtys: list[int]):
    """カードをランダムに配る。
    Args:
        my_player_num (int): 自分(手札が分かっているプレイヤ)の番号。
        my_hand (list[Card]): 自分の手札。
        discards (list[Card]): 捨て札。
        player_hand_qtys (list[int]): 各プレイヤ(含自分)の手札枚数。

    Returns:
        (list[Card], list[list[Card]]): (山札, 自分を含む各プレイヤの手札)
    """
    # どこにあるかわからないカードの集合。
    rest_cards = State.all_cards()

    # rest_cardsから自分の手札を除く。
    for card in my_hand:
        del rest_cards[rest_cards.index(card)]

    # rest_cardsから捨て札にあるカードを除く。
    for card in discards:
        del rest_cards[rest_cards.index(card)]

    # 分配するためにシャッフルする。
    random.Random(os.urandom(16)).shuffle(rest_cards)

    # 各プレイヤに分配。
    player_hands: list[list[Card]] = [[] for _ in range(NUM_OF_PLAYERS)]
    player_hands[my_player_num] = my_hand
    for player in range(NUM_OF_PLAYERS):
        if player == my_player_num:
            continue
        hand_qty = player_hand_qtys[player]
        player_hands[player] = rest_cards[:hand_qty]
        rest_cards = rest_cards[hand_qty:]

    return rest_cards, player_hands
