from __future__ import annotations
from enum import Enum


class Color(Enum):
    """カードの色。NONEはパス。
    """
    BLUE = 'Blue'
    GREEN = 'Green'
    RED = 'Red'
    YELLOW = 'Yellow'
    WILD = 'Wild'
    NONE = 'None'


class Number(Enum):
    """カードの数字。NONEは記号カード・パス。
    """
    NONE = 'None'
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


class Action(Enum):
    """カードの記号。NONEは数字カード・パス。
    """
    NONE = 'None'
    DRAW_TWO = 'Draw Two'
    REVERSE = 'Reverse'
    SKIP = 'Skip'
    WILD = 'Wild'
    WILD_DRAW_4 = 'Wild Draw 4'
    WILD_SHUFFLE_HANDS = 'Wild Shuffle Hands'
    WILD_CUSTOMIZABLE = 'Wild Customizable'


class Card:
    def __init__(self, color: Color, number: Number, action: Action) -> None:
        self.color = color
        self.number = number
        self.action = action

    def __eq__(self, value: Card) -> bool:
        return self.color == value.color and\
          self.number == value.number and\
          self.action == value.action

    def __ne__(self, value: Card) -> bool:
        return not self == value

    def is_legal(self, table_card: Card) -> bool:
        if self.color == Color.WILD:
            return True
        elif self.color == table_card.color:
            return True
        elif self.action == Action.NONE and self.number == table_card.number:
            return True
        elif self.number == Number.NONE and self.action == table_card.action:
            return True
        else:
            return False

    def is_empty(self) -> bool:
        return self.color == Color.NONE

    @classmethod
    def empty(cls):
        return Card(Color.NONE, Number.NONE, Action.NONE)

    @classmethod
    def blue_zero(cls):
        return Card(Color.BLUE, Number.ZERO, Action.NONE)

    @classmethod
    def blue_one(cls):
        return Card(Color.BLUE, Number.ONE, Action.NONE)

    @classmethod
    def blue_two(cls):
        return Card(Color.BLUE, Number.TWO, Action.NONE)

    @classmethod
    def blue_three(cls):
        return Card(Color.BLUE, Number.THREE, Action.NONE)

    @classmethod
    def blue_four(cls):
        return Card(Color.BLUE, Number.FOUR, Action.NONE)

    @classmethod
    def blue_five(cls):
        return Card(Color.BLUE, Number.FIVE, Action.NONE)

    @classmethod
    def blue_six(cls):
        return Card(Color.BLUE, Number.SIX, Action.NONE)

    @classmethod
    def blue_seven(cls):
        return Card(Color.BLUE, Number.SEVEN, Action.NONE)

    @classmethod
    def blue_eight(cls):
        return Card(Color.BLUE, Number.EIGHT, Action.NONE)

    @classmethod
    def blue_nine(cls):
        return Card(Color.BLUE, Number.NINE, Action.NONE)

    @classmethod
    def blue_draw_two(cls):
        return Card(Color.BLUE, Number.NONE, Action.DRAW_TWO)

    @classmethod
    def blue_reverse(cls):
        return Card(Color.BLUE, Number.NONE, Action.REVERSE)

    @classmethod
    def blue_skip(cls):
        return Card(Color.BLUE, Number.NONE, Action.SKIP)

    @classmethod
    def green_zero(cls):
        return Card(Color.GREEN, Number.ZERO, Action.NONE)

    @classmethod
    def green_one(cls):
        return Card(Color.GREEN, Number.ONE, Action.NONE)

    @classmethod
    def green_two(cls):
        return Card(Color.GREEN, Number.TWO, Action.NONE)

    @classmethod
    def green_three(cls):
        return Card(Color.GREEN, Number.THREE, Action.NONE)

    @classmethod
    def green_four(cls):
        return Card(Color.GREEN, Number.FOUR, Action.NONE)

    @classmethod
    def green_five(cls):
        return Card(Color.GREEN, Number.FIVE, Action.NONE)

    @classmethod
    def green_six(cls):
        return Card(Color.GREEN, Number.SIX, Action.NONE)

    @classmethod
    def green_seven(cls):
        return Card(Color.GREEN, Number.SEVEN, Action.NONE)

    @classmethod
    def green_eight(cls):
        return Card(Color.GREEN, Number.EIGHT, Action.NONE)

    @classmethod
    def green_nine(cls):
        return Card(Color.GREEN, Number.NINE, Action.NONE)

    @classmethod
    def green_draw_two(cls):
        return Card(Color.GREEN, Number.NONE, Action.DRAW_TWO)

    @classmethod
    def green_reverse(cls):
        return Card(Color.GREEN, Number.NONE, Action.REVERSE)

    @classmethod
    def green_skip(cls):
        return Card(Color.GREEN, Number.NONE, Action.SKIP)

    @classmethod
    def red_zero(cls):
        return Card(Color.RED, Number.ZERO, Action.NONE)

    @classmethod
    def red_one(cls):
        return Card(Color.RED, Number.ONE, Action.NONE)

    @classmethod
    def red_two(cls):
        return Card(Color.RED, Number.TWO, Action.NONE)

    @classmethod
    def red_three(cls):
        return Card(Color.RED, Number.THREE, Action.NONE)

    @classmethod
    def red_four(cls):
        return Card(Color.RED, Number.FOUR, Action.NONE)

    @classmethod
    def red_five(cls):
        return Card(Color.RED, Number.FIVE, Action.NONE)

    @classmethod
    def red_six(cls):
        return Card(Color.RED, Number.SIX, Action.NONE)

    @classmethod
    def red_seven(cls):
        return Card(Color.RED, Number.SEVEN, Action.NONE)

    @classmethod
    def red_eight(cls):
        return Card(Color.RED, Number.EIGHT, Action.NONE)

    @classmethod
    def red_nine(cls):
        return Card(Color.RED, Number.NINE, Action.NONE)

    @classmethod
    def red_draw_two(cls):
        return Card(Color.RED, Number.NONE, Action.DRAW_TWO)

    @classmethod
    def red_reverse(cls):
        return Card(Color.RED, Number.NONE, Action.REVERSE)

    @classmethod
    def red_skip(cls):
        return Card(Color.RED, Number.NONE, Action.SKIP)

    @classmethod
    def yellow_zero(cls):
        return Card(Color.YELLOW, Number.ZERO, Action.NONE)

    @classmethod
    def yellow_one(cls):
        return Card(Color.YELLOW, Number.ONE, Action.NONE)

    @classmethod
    def yellow_two(cls):
        return Card(Color.YELLOW, Number.TWO, Action.NONE)

    @classmethod
    def yellow_three(cls):
        return Card(Color.YELLOW, Number.THREE, Action.NONE)

    @classmethod
    def yellow_four(cls):
        return Card(Color.YELLOW, Number.FOUR, Action.NONE)

    @classmethod
    def yellow_five(cls):
        return Card(Color.YELLOW, Number.FIVE, Action.NONE)

    @classmethod
    def yellow_six(cls):
        return Card(Color.YELLOW, Number.SIX, Action.NONE)

    @classmethod
    def yellow_seven(cls):
        return Card(Color.YELLOW, Number.SEVEN, Action.NONE)

    @classmethod
    def yellow_eight(cls):
        return Card(Color.YELLOW, Number.EIGHT, Action.NONE)

    @classmethod
    def yellow_nine(cls):
        return Card(Color.YELLOW, Number.NINE, Action.NONE)

    @classmethod
    def yellow_draw_two(cls):
        return Card(Color.YELLOW, Number.NONE, Action.DRAW_TWO)

    @classmethod
    def yellow_reverse(cls):
        return Card(Color.YELLOW, Number.NONE, Action.REVERSE)

    @classmethod
    def yellow_skip(cls):
        return Card(Color.YELLOW, Number.NONE, Action.SKIP)

    @classmethod
    def wild(cls):
        return Card(Color.WILD, Number.NONE, Action.WILD)

    @classmethod
    def wild_draw_4(cls):
        return Card(Color.WILD, Number.NONE, Action.WILD_DRAW_4)

    @classmethod
    def wild_shuffle_hands(cls):
        return Card(Color.WILD, Number.NONE, Action.WILD_SHUFFLE_HANDS)

    @classmethod
    def wild_customizable(cls):
        return Card(Color.WILD, Number.NONE, Action.WILD_CUSTOMIZABLE)
