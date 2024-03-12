import pandas as pd
import numpy as np

pd.options.mode.copy_on_write = True


def feature_engineering(df):
    feature_engineering_team_data(df)
    feature_engineering_player_data(df)
    return df


def feature_engineering_team_data(df):
    df['avg_game_mode_score_team_one'] = df.apply(
        lambda x: calculate_team_average_game_mode_score(x['team_one'], x['date'], df), axis=1)
    df['avg_game_mode_score_team_one_against'] = df.apply(
        lambda x: calculate_team_average_game_mode_score_against(x['team_one'], x['date'], df), axis=1)
    df['avg_map_game_mode_score_team_one'] = df.apply(
        lambda x: calculate_team_average_map_game_mode_score(x['team_one'], x['date'], x['map_id'], df), axis=1)
    df['avg_map_game_mode_score_team_one_against'] = df.apply(
        lambda x: calculate_team_average_map_game_mode_score_against(x['team_one'], x['date'], x['map_id'], df), axis=1)
    df['avg_game_mode_score_team_two'] = df.apply(
        lambda x: calculate_team_average_game_mode_score(x['team_two'], x['date'], df), axis=1)
    df['avg_game_mode_score_team_two_against'] = df.apply(
        lambda x: calculate_team_average_game_mode_score_against(x['team_two'], x['date'], df), axis=1)
    df['avg_map_game_mode_score_team_two'] = df.apply(
        lambda x: calculate_team_average_map_game_mode_score(x['team_two'], x['date'], x['map_id'], df), axis=1)
    df['avg_map_game_mode_score_team_two_against'] = df.apply(
        lambda x: calculate_team_average_map_game_mode_score_against(x['team_two'], x['date'], x['map_id'], df), axis=1)


def calculate_team_average_game_mode_score(team_id, match_date, df):
    team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['date'] < match_date)]

    if len(team_matches) < 5:
        team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id))]

    team_matches['relevant_scores'] = np.where(team_matches['team_one'] == team_id,
                                               team_matches['team_one_score'],
                                               team_matches['team_two_score'])
    average_game_mode_score = team_matches['relevant_scores'].mean()
    return average_game_mode_score


def calculate_team_average_game_mode_score_against(team_id, match_date, df):
    team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['date'] < match_date)]

    if len(team_matches) < 5:
        team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id))]

    team_matches['relevant_scores_against'] = np.where(team_matches['team_one'] == team_id,
                                                       team_matches['team_two_score'],
                                                       team_matches['team_one_score'])
    average_game_mode_score = team_matches['relevant_scores_against'].mean()
    return average_game_mode_score


def calculate_team_average_map_game_mode_score(team_id, match_date, map_id, df):
    team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['map_id'] == map_id) & (
            df['date'] < match_date)]

    if len(team_matches) < 5:
        team_matches = df[(df['team_one'] == team_id) | (df['team_two'] == team_id) & (df['map_id'] == map_id)]

    team_matches['relevant_scores'] = np.where(team_matches['team_one'] == team_id,
                                               team_matches['team_one_score'],
                                               team_matches['team_two_score'])
    average_map_game_mode_score = team_matches['relevant_scores'].mean()
    return average_map_game_mode_score


def calculate_team_average_map_game_mode_score_against(team_id, match_date, map_id, df):
    team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['map_id'] == map_id) & (
            df['date'] < match_date)]

    if len(team_matches) < 5:
        team_matches = df[(df['team_one'] == team_id) | (df['team_two'] == team_id) & (df['map_id'] == map_id)]

    team_matches['relevant_scores_against'] = np.where(team_matches['team_one'] == team_id,
                                                       team_matches['team_two_score'],
                                                       team_matches['team_one_score'])
    average_map_game_mode_score = team_matches['relevant_scores_against'].mean()
    return average_map_game_mode_score


def feature_engineering_player_data(df):
    player_performance_df = get_player_performance_df(df)

    player_columns = ['team_one_player_one', 'team_one_player_two', 'team_one_player_three', 'team_one_player_four',
                      'team_two_player_one', 'team_two_player_two', 'team_two_player_three', 'team_two_player_four']

    for player in player_columns:
        df[f'avg_game_mode_kills_{player}'] = df.apply(
            lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'], player_performance_df,
                                                                    'kills'),
            axis=1)
        df[f'avg_map_game_mode_kills_{player}'] = df.apply(
            lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'], player_performance_df,
                                                                    'kills'),
            axis=1)
        df[f'avg_game_mode_deaths_{player}'] = df.apply(
            lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'], player_performance_df,
                                                                    'deaths'),
            axis=1)
        df[f'avg_map_game_mode_deaths_{player}'] = df.apply(
            lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'],
                                                                        player_performance_df,
                                                                        'deaths'),
            axis=1)
        df[f'avg_game_mode_damage_{player}'] = df.apply(
            lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'], player_performance_df,
                                                                    'damage'),
            axis=1)
        df[f'avg_map_game_mode_damage_{player}'] = df.apply(
            lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'],
                                                                        player_performance_df,
                                                                        'damage'),
            axis=1)
        df[f'avg_game_mode_objectives_{player}'] = df.apply(
            lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'],
                                                                    player_performance_df, 'objectives'),
            axis=1)
        df[f'avg_map_game_mode_objectives_{player}'] = df.apply(
            lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'],
                                                                        player_performance_df,
                                                                        'objectives'),
            axis=1)


def get_player_performance_df(df):
    """
    Reformat player data so each entry in the player_performance data frame resembles a singular players
    results for a map ie (map_id, player_id, kills, deaths, damage, obj)
    """
    players_info = []
    for team in ['team_one', 'team_two']:
        for player in ['player_one', 'player_two', 'player_three', 'player_four']:
            player_info_arr = [f'{team}_{player}_id', f'{team}_{player}_kills', f'{team}_{player}_deaths',
                               f'{team}_{player}_damage', f'{team}_{player}_objectives']
            players_info.append(player_info_arr)

    performance_dfs_list = []

    for player_info in players_info:
        player_id_col, kills_col, deaths_col, damage_col, obj = player_info

        # Create a temp df for each player
        temp_df = df[['date', 'map_id', player_id_col, kills_col, deaths_col, damage_col, obj]]

        # Rename columns to have a uniform structure
        temp_df.rename(columns={
            player_id_col: 'player_id',
            kills_col: 'kills',
            deaths_col: 'deaths',
            damage_col: 'damage',
            obj: 'objectives',
        }, inplace=True)

        performance_dfs_list.append(temp_df)

    # Concatenate to single df
    player_performance_df = pd.concat(performance_dfs_list).reset_index(drop=True)

    return player_performance_df


def calculate_player_average_game_mode_kd(player_id, match_date, player_stats_df):
    player_data = player_stats_df[(player_stats_df['player_id'] == player_id) & (player_stats_df['date'] < match_date)]

    agg_kills = player_data['kills'].sum()
    agg_deaths = player_data['deaths'].sum()
    kd_ratio = agg_kills / max(agg_deaths, 1)

    return kd_ratio if kd_ratio else np.nan


def calculate_player_average_game_mode_statistics(player_id, match_date, player_stats_df, statistic):
    player_data = player_stats_df[(player_stats_df['player_id'] == player_id) & (player_stats_df['date'] < match_date)]
    if len(player_data) < 5:
        player_data = player_stats_df[(player_stats_df['player_id'] == player_id)]
    return player_data[statistic].mean()


def calculate_player_average_map_game_mode_statistics(player_id, match_date, map_id, player_stats_df, statistic):
    player_data = player_stats_df[
        (player_stats_df['player_id'] == player_id) &
        (player_stats_df['date'] < match_date) &
        (player_stats_df['map_id'] == map_id)
    ]
    if len(player_data) < 5:
        player_data = player_stats_df[(player_stats_df['player_id'] == player_id) & (player_stats_df['map_id'] == map_id)]
    return player_data[statistic].mean()
