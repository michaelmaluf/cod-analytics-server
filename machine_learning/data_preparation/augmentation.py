from random import shuffle

import pandas as pd



def data_augmentation(df):
    """
    :param data: DataFrame for game mode
    Method creates duplicate entries for each entry in the data argument.

    The order of the teams and players does not matter (Team One vs Team One, player_one vs player_two), therefore
    duplication and swaps ensures the model treats player and team order neutrally.
    For instance, for every entry, we will create 4 entries where a team is designated as team one with their players in randomized order.
    We will repeat this process for 4 entries but now designate this team as team two.
    The result is 1 entry turning into 8 entries, facilitates the model training later.
    """

    df_copy = df.copy()  # df for game_mode just copied
    randomized_entries = generate_randomized_entries(
        df_copy)  # df for game_mode with 4 randomized rows based on the teams original team designation
    swapped_teams_df = swap_teams(df_copy)  # takes df_copy and swaps teams and their respective players
    randomized_entries_swapped = generate_randomized_entries(
        swapped_teams_df)  # df for game_mode with 4 randomized rows based on the teams swapped team designation

    augmented_df = pd.concat([df_copy, randomized_entries, swapped_teams_df, randomized_entries_swapped]).reset_index(
        drop=True)

    return augmented_df


def swap_teams(df):
    df_swapped = df.copy()

    team_one_cols = [col for col in df.columns if 'team_one' in col]
    team_two_cols = [col for col in df.columns if 'team_two' in col]

    for t1_col, t2_col in zip(team_one_cols, team_two_cols):
        df_swapped[t1_col], df_swapped[t2_col] = df_swapped[t2_col], df_swapped[t1_col]

    return df_swapped


def generate_randomized_entries(df, num_entries=3):
    """
    For each row in the DataFrame, generate additional rows with players in randomized positions.

    Returns:
    - df_augmented: DataFrame with original and randomized entries.
    """
    augmented_rows = []

    for _, row in df.iterrows():
        # Collect all player-related info for each team
        team_player_stats = {}

        for team in ['team_one', 'team_two']:
            team_player_stats[team] = []
            for player in ['player_one', 'player_two', 'player_three', 'player_four']:
                player_info = {
                    'avg_game_mode_kills': row[f'avg_game_mode_kills_{team}_{player}'],
                    'avg_map_game_mode_kills': row[f'avg_map_game_mode_kills_{team}_{player}'],
                    'avg_game_mode_deaths': row[f'avg_game_mode_deaths_{team}_{player}'],
                    'avg_map_game_mode_deaths': row[f'avg_map_game_mode_deaths_{team}_{player}'],
                    'avg_game_mode_damage': row[f'avg_game_mode_damage_{team}_{player}'],
                    'avg_map_game_mode_damage': row[f'avg_map_game_mode_damage_{team}_{player}'],
                    'avg_game_mode_objectives': row[f'avg_game_mode_objectives_{team}_{player}'],
                    'avg_map_game_mode_objectives': row[f'avg_map_game_mode_objectives_{team}_{player}'],
                }
                team_player_stats[team].append(player_info)

        # Create permutations
        for _ in range(num_entries):
            for team in ['team_one', 'team_two']:
                shuffle(team_player_stats[team])

            new_row = row.copy()
            for team in ['team_one', 'team_two']:
                for player, info in zip(['player_one', 'player_two', 'player_three', 'player_four'],
                                        team_player_stats[team]):
                    new_row[f'avg_game_mode_kills_{team}_{player}'] = info['avg_game_mode_kills']
                    new_row[f'avg_map_game_mode_kills_{team}_{player}'] = info['avg_map_game_mode_kills']
                    new_row[f'avg_game_mode_deaths_{team}_{player}'] = info['avg_game_mode_deaths']
                    new_row[f'avg_map_game_mode_deaths_{team}_{player}'] = info['avg_map_game_mode_deaths']
                    new_row[f'avg_game_mode_damage_{team}_{player}'] = info['avg_game_mode_damage']
                    new_row[f'avg_map_game_mode_damage_{team}_{player}'] = info['avg_map_game_mode_damage']
                    new_row[f'avg_game_mode_objectives_{team}_{player}'] = info['avg_game_mode_objectives']
                    new_row[f'avg_map_game_mode_objectives_{team}_{player}'] = info['avg_map_game_mode_objectives']

            augmented_rows.append(new_row)

    return pd.DataFrame(augmented_rows)