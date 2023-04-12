from enum import Enum


class ActionType(Enum):
    CHALLENGE = "Challenge"
    COLOR_CHOICE = "ColorChoice"
    SUBMISSION = "Submission"
    SUBMISSION_OF_DRAWN_CARD = "SubmissionOfDrawCard"

    def __str__(self) -> str:
        return f"{self.value}"
