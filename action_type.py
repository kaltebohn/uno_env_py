from enum import auto, Enum


class ActionType(Enum):
    CHALLENGE = auto()
    COLOR_CHOICE = auto()
    SUBMISSION = auto()
    SUBMISSION_OF_DRAWN_CARD = auto()
