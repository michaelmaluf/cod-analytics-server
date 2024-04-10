from decimal import Decimal

CDL_FIRST_MATCH_DATE = '2023-12-07'
CDL_YEAR = 2023
BREAKING_POINT_URL = 'https://www.breakingpoint.gg/matches/'

HARDPOINT_TARGET_SCORE = 250
SEARCH_AND_DESTROY_TARGET_SCORE = 6
CONTROL_TARGET_SCORE = 3

WEIGHTS_PER_GAME_MODE = {
    'Hardpoint': {
        'kills': Decimal('0.125'),
        'deaths': Decimal('0.1'),
        'damage': Decimal('0.2'),
        'objectives': Decimal('0.2'),
        'kd':  Decimal('0.2'),
        'engagements':  Decimal('0.175'),
    },
    'Search & Destroy': {
        'kills': Decimal('0.2'),
        'deaths': Decimal('0.2'),
        'damage': Decimal('0.1'),
        'objectives': Decimal('0.1'),
        'kd':  Decimal('0.3'),
        'engagements':  Decimal('0.1'),
    },
    'Control': {
        'kills': Decimal('0.2'),
        'deaths': Decimal('0.2'),
        'damage': Decimal('0.2'),
        'objectives': Decimal('0.1'),
        'kd':  Decimal('0.2'),
        'engagements':  Decimal('0.1'),
    }
}
