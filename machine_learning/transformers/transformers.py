from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


def get_columns_to_encode():
    columns_to_encode = ['map_id', 'stage', 'team_one', 'team_two']
    return columns_to_encode


# def get_columns_to_impute():
#     columns_to_impute = []
#
#     for team in ['team_one', 'team_two']:
#         columns_to_impute.append(f'avg_game_mode_score_{team}')
#         columns_to_impute.append(f'avg_game_mode_score_{team}_against')
#         columns_to_impute.append(f'avg_map_game_mode_score_{team}')
#         columns_to_impute.append(f'avg_map_game_mode_score_{team}_against')
#         for player in ['player_one', 'player_two', 'player_three', 'player_four']:
#             columns_to_impute.append(f'avg_game_mode_kills_{team}_{player}')
#             columns_to_impute.append(f'avg_map_game_mode_kills_{team}_{player}')
#             columns_to_impute.append(f'avg_game_mode_deaths_{team}_{player}')
#             columns_to_impute.append(f'avg_map_game_mode_deaths_{team}_{player}')
#             columns_to_impute.append(f'avg_game_mode_damage_{team}_{player}')
#             columns_to_impute.append(f'avg_map_game_mode_damage_{team}_{player}')
#             columns_to_impute.append(f'avg_game_mode_objectives_{team}_{player}')
#             columns_to_impute.append(f'avg_map_game_mode_objectives_{team}_{player}')
#
#
#     return columns_to_impute

preprocessor = ColumnTransformer(
    transformers=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'), get_columns_to_encode())
    ],
    remainder='passthrough'
)
