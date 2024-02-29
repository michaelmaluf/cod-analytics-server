from enum import Enum
from app.errors import GameModeNotFoundError

class GameModeType(Enum):
    HARDPOINT = 'Hardpoint'
    SEARCH_AND_DESTROY = 'Search & Destroy'
    CONTROL = 'Control'

def string_to_game_mode_type(input_string):
    for game_mode in GameModeType:
        if game_mode.value == input_string:
            return game_mode
    raise GameModeNotFoundError(input_string)

def type_to_objective_key(game_mode_type):
    if game_mode_type.name == GameModeType.HARDPOINT:
        return 'hill_time'
    elif game_mode_type.name == GameModeType.SEARCH_AND_DESTROY:
        return 'first_bloods'
    else:
        return 'captures'
