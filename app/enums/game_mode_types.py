from enum import Enum
from app.errors import GameModeNotFoundError

class GameModeType(Enum):
    HARDPOINT = 'Hardpoint'
    SEARCH_AND_DESTROY = 'Search & Destroy'
    CONTROL = 'Control'

    @classmethod
    def get_mode_by_value(cls, value):
        for mode in cls:
            if mode.value == value:
                return mode
        return None

    def to_objective_key(game_mode_type):
        if game_mode_type.name == GameModeType.HARDPOINT:
            return 'hill_time'
        elif game_mode_type.name == GameModeType.SEARCH_AND_DESTROY:
            return 'first_bloods'
        else:
            return 'captures'
