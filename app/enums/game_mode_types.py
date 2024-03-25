from enum import Enum


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

    def to_objective_key(self):
        if self == GameModeType.HARDPOINT:
            return 'hill_time'
        elif self == GameModeType.SEARCH_AND_DESTROY:
            return 'first_bloods'
        else:
            return 'captures'
