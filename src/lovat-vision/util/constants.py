import enum


class GamePhase(enum.Enum):
    PRE_MATCH = 1
    AUTO = 2
    TRANSITION = 3
    TELEOP = 4
    ENDGAME = 5
    POST_MATCH = 6


SCOREBOARD_BOX = [60, 130, 900, 1020]