import pandas as pd
import numpy as np

pd.options.mode.copy_on_write = True


def feature_engineering(df):
    df_1 = feature_engineering_team_data(df)
    df_2 = feature_engineering_player_data(df_1)
    return df_2


def calculate_adjusted_cumulative_avg(series):
    # Calculate the backward-looking expanding mean and shift
    cum_avg = series.expanding().mean().shift(1)

    for i in range(len(series)):
        if i < 3:
            cum_avg.iloc[i] = series.iloc[0:min(3, len(series))].mean()
    return cum_avg


def feature_engineering_team_data(df):
    team_performance_df = get_team_performance_df(df)

    team_performance_df['avg_game_mode_score'] = team_performance_df.groupby('team')['team_score'].transform(
        calculate_adjusted_cumulative_avg)
    team_performance_df['avg_game_mode_score_against'] = team_performance_df.groupby('team')[
        'opponent_score'].transform(
        calculate_adjusted_cumulative_avg)
    team_performance_df['avg_map_game_mode_score'] = team_performance_df.groupby(['team', 'map_id'])[
        'team_score'].transform(
        calculate_adjusted_cumulative_avg)
    team_performance_df['avg_map_game_mode_score_against'] = team_performance_df.groupby(['team', 'map_id'])[
        'opponent_score'].transform(
        calculate_adjusted_cumulative_avg)

    df = df.merge(team_performance_df, left_on=['team_one', 'date', 'map_id', 'map_number'],
                  right_on=['team', 'date', 'map_id', 'map_number'], how='left')

    df.rename(columns={
        'avg_game_mode_score': 'avg_game_mode_score_team_one',
        'avg_game_mode_score_against': 'avg_game_mode_score_team_one_against',
        'avg_map_game_mode_score': 'avg_map_game_mode_score_team_one',
        'avg_map_game_mode_score_against': 'avg_map_game_mode_score_team_one_against',

    }, inplace=True)

    df.drop(['team', 'team_score', 'opponent', 'opponent_score'], axis=1, inplace=True)

    df = df.merge(team_performance_df, left_on=['team_two', 'date', 'map_id', 'map_number'],
                  right_on=['team', 'date', 'map_id', 'map_number'], how='left')
    df.rename(columns={
        'avg_game_mode_score': 'avg_game_mode_score_team_two',
        'avg_game_mode_score_against': 'avg_game_mode_score_team_two_against',
        'avg_map_game_mode_score': 'avg_map_game_mode_score_team_two',
        'avg_map_game_mode_score_against': 'avg_map_game_mode_score_team_two_against',

    }, inplace=True)
    df.drop(['team', 'team_score', 'opponent', 'opponent_score'], axis=1, inplace=True)

    return df

    # df['avg_game_mode_score_team_one'] = df.apply(
    #     lambda x: calculate_team_average_game_mode_score(x['team_one'], x['date'], df), axis=1)
    # df['avg_game_mode_score_team_one_against'] = df.apply(
    #     lambda x: calculate_team_average_game_mode_score_against(x['team_one'], x['date'], df), axis=1)
    # df['avg_map_game_mode_score_team_one'] = df.apply(
    #     lambda x: calculate_team_average_map_game_mode_score(x['team_one'], x['date'], x['map_id'], df), axis=1)
    # df['avg_map_game_mode_score_team_one_against'] = df.apply(
    #     lambda x: calculate_team_average_map_game_mode_score_against(x['team_one'], x['date'], x['map_id'], df), axis=1)
    # df['avg_game_mode_score_team_two'] = df.apply(
    #     lambda x: calculate_team_average_game_mode_score(x['team_two'], x['date'], df), axis=1)
    # df['avg_game_mode_score_team_two_against'] = df.apply(
    #     lambda x: calculate_team_average_game_mode_score_against(x['team_two'], x['date'], df), axis=1)
    # df['avg_map_game_mode_score_team_two'] = df.apply(
    #     lambda x: calculate_team_average_map_game_mode_score(x['team_two'], x['date'], x['map_id'], df), axis=1)
    # df['avg_map_game_mode_score_team_two_against'] = df.apply(
    #     lambda x: calculate_team_average_map_game_mode_score_against(x['team_two'], x['date'], x['map_id'], df), axis=1)


def get_team_performance_df(df):
    # Split the DataFrame into two based on team one and team two
    team_one_df = df[
        ['date', 'map_id', 'map_number', 'team_one', 'team_one_score', 'team_two', 'team_two_score']].copy()
    team_two_df = df[
        ['date', 'map_id', 'map_number', 'team_two', 'team_two_score', 'team_one', 'team_one_score']].copy()

    # Rename columns so they match
    team_one_df.rename(columns={'team_one': 'team', 'team_two': 'opponent', 'team_one_score': 'team_score',
                                'team_two_score': 'opponent_score'}, inplace=True)
    team_two_df.rename(columns={'team_two': 'team', 'team_one': 'opponent', 'team_two_score': 'team_score',
                                'team_one_score': 'opponent_score'}, inplace=True)

    # Concatenate the two DataFrames into a single DataFrame
    performance_df = pd.concat([team_one_df, team_two_df], ignore_index=True)

    performance_df.sort_values(by=['team', 'date', 'map_number'], inplace=True)

    # performance_df['cumulative_avg_score'] = performance_df.groupby('team')['team_score'].transform(lambda x: x.expanding().mean().shift(1))

    return performance_df


# THE FOUR METHODS BELOW ARE DEPRECATED - WERE USED PREVIOUSLY WITH DF.APPLY, FE IS NOW ENHANCED WITH GROUPBY
# def calculate_team_average_game_mode_score(team_id, match_date, df):
#     team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['date'] < match_date)]
#
#     if len(team_matches) < 5:
#         team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id))]
#
#     team_matches['relevant_scores'] = np.where(team_matches['team_one'] == team_id,
#                                                team_matches['team_one_score'],
#                                                team_matches['team_two_score'])
#     average_game_mode_score = team_matches['relevant_scores'].mean()
#     return average_game_mode_score
#
#
# def calculate_team_average_game_mode_score_against(team_id, match_date, df):
#     team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['date'] < match_date)]
#
#     if len(team_matches) < 5:
#         team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id))]
#
#     team_matches['relevant_scores_against'] = np.where(team_matches['team_one'] == team_id,
#                                                        team_matches['team_two_score'],
#                                                        team_matches['team_one_score'])
#     average_game_mode_score = team_matches['relevant_scores_against'].mean()
#     return average_game_mode_score
#
#
# def calculate_team_average_map_game_mode_score(team_id, match_date, map_id, df):
#     team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['map_id'] == map_id) & (
#             df['date'] < match_date)]
#
#     if len(team_matches) < 5:
#         team_matches = df[(df['team_one'] == team_id) | (df['team_two'] == team_id) & (df['map_id'] == map_id)]
#
#     team_matches['relevant_scores'] = np.where(team_matches['team_one'] == team_id,
#                                                team_matches['team_one_score'],
#                                                team_matches['team_two_score'])
#     average_map_game_mode_score = team_matches['relevant_scores'].mean()
#     return average_map_game_mode_score
#
#
# def calculate_team_average_map_game_mode_score_against(team_id, match_date, map_id, df):
#     team_matches = df[((df['team_one'] == team_id) | (df['team_two'] == team_id)) & (df['map_id'] == map_id) & (
#             df['date'] < match_date)]
#
#     if len(team_matches) < 5:
#         team_matches = df[(df['team_one'] == team_id) | (df['team_two'] == team_id) & (df['map_id'] == map_id)]
#
#     team_matches['relevant_scores_against'] = np.where(team_matches['team_one'] == team_id,
#                                                        team_matches['team_two_score'],
#                                                        team_matches['team_one_score'])
#     average_map_game_mode_score = team_matches['relevant_scores_against'].mean()
#     return average_map_game_mode_score


def feature_engineering_player_data(df):
    player_performance_df = get_player_performance_df(df)

    player_performance_df['avg_game_mode_kills'] = player_performance_df.groupby('player_id')['kills'].transform(
        calculate_adjusted_cumulative_avg)
    player_performance_df['avg_game_mode_deaths'] = player_performance_df.groupby('player_id')['deaths'].transform(
        calculate_adjusted_cumulative_avg)
    player_performance_df['avg_game_mode_damage'] = player_performance_df.groupby('player_id')['damage'].transform(
        calculate_adjusted_cumulative_avg)
    player_performance_df['avg_game_mode_objectives'] = player_performance_df.groupby('player_id')[
        'objectives'].transform(
        calculate_adjusted_cumulative_avg)
    player_performance_df['avg_map_game_mode_kills'] = player_performance_df.groupby(['player_id', 'map_id'])[
        'kills'].transform(
        calculate_adjusted_cumulative_avg)
    player_performance_df['avg_map_game_mode_deaths'] = player_performance_df.groupby(['player_id', 'map_id'])[
        'deaths'].transform(
        calculate_adjusted_cumulative_avg)
    player_performance_df['avg_map_game_mode_damage'] = player_performance_df.groupby(['player_id', 'map_id'])[
        'damage'].transform(
        calculate_adjusted_cumulative_avg)
    player_performance_df['avg_map_game_mode_objectives'] = player_performance_df.groupby(['player_id', 'map_id'])[
        'objectives'].transform(
        calculate_adjusted_cumulative_avg)

    player_columns = ['team_one_player_one', 'team_one_player_two', 'team_one_player_three', 'team_one_player_four',
                      'team_two_player_one', 'team_two_player_two', 'team_two_player_three', 'team_two_player_four']

    for player in player_columns:
        df = df.merge(player_performance_df, left_on=[f'{player}_id', 'date', 'map_id'],
                      right_on=['player_id', 'date', 'map_id'], how='left')

        df.rename(columns={
            'avg_game_mode_kills': f'avg_game_mode_kills_{player}',
            'avg_game_mode_deaths': f'avg_game_mode_deaths_{player}',
            'avg_game_mode_damage': f'avg_game_mode_damage_{player}',
            'avg_game_mode_objectives': f'avg_game_mode_objectives_{player}',
            'avg_map_game_mode_kills': f'avg_map_game_mode_kills_{player}',
            'avg_map_game_mode_deaths': f'avg_map_game_mode_deaths_{player}',
            'avg_map_game_mode_damage': f'avg_map_game_mode_damage_{player}',
            'avg_map_game_mode_objectives': f'avg_map_game_mode_objectives_{player}',

        }, inplace=True)

        df.drop(['player_id', 'kills', 'deaths', 'damage', 'objectives'], axis=1, inplace=True)

    return df

    # df[f'avg_game_mode_kills_{player}'] = df.apply(
    #     lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'], player_performance_df,
    #                                                             'kills'),
    #     axis=1)
    # df[f'avg_map_game_mode_kills_{player}'] = df.apply(
    #     lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'], player_performance_df,
    #                                                             'kills'),
    #     axis=1)
    # df[f'avg_game_mode_deaths_{player}'] = df.apply(
    #     lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'], player_performance_df,
    #                                                             'deaths'),
    #     axis=1)
    # df[f'avg_map_game_mode_deaths_{player}'] = df.apply(
    #     lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'],
    #                                                                 player_performance_df,
    #                                                                 'deaths'),
    #     axis=1)
    # df[f'avg_game_mode_damage_{player}'] = df.apply(
    #     lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'], player_performance_df,
    #                                                             'damage'),
    #     axis=1)
    # df[f'avg_map_game_mode_damage_{player}'] = df.apply(
    #     lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'],
    #                                                                 player_performance_df,
    #                                                                 'damage'),
    #     axis=1)
    # df[f'avg_game_mode_objectives_{player}'] = df.apply(
    #     lambda x: calculate_player_average_game_mode_statistics(x[f'{player}_id'], x['date'],
    #                                                             player_performance_df, 'objectives'),
    #     axis=1)
    # df[f'avg_map_game_mode_objectives_{player}'] = df.apply(
    #     lambda x: calculate_player_average_map_game_mode_statistics(x[f'{player}_id'], x['date'], x['map_id'],
    #                                                                 player_performance_df,
    #                                                                 'objectives'),
    #     axis=1)


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

# THE THREE METHODS BELOW ARE DEPRECATED - WERE USED PREVIOUSLY WITH DF.APPLY, FE IS NOW ENHANCED WITH GROUPBY
# def calculate_player_average_game_mode_kd(player_id, match_date, player_stats_df):
#     player_data = player_stats_df[(player_stats_df['player_id'] == player_id) & (player_stats_df['date'] < match_date)]
#
#     agg_kills = player_data['kills'].sum()
#     agg_deaths = player_data['deaths'].sum()
#     kd_ratio = agg_kills / max(agg_deaths, 1)
#
#     return kd_ratio if kd_ratio else np.nan
#
#
# def calculate_player_average_game_mode_statistics(player_id, match_date, player_stats_df, statistic):
#     player_data = player_stats_df[(player_stats_df['player_id'] == player_id) & (player_stats_df['date'] < match_date)]
#     if len(player_data) < 5:
#         player_data = player_stats_df[(player_stats_df['player_id'] == player_id)]
#     return player_data[statistic].mean()
#
#
# def calculate_player_average_map_game_mode_statistics(player_id, match_date, map_id, player_stats_df, statistic):
#     player_data = player_stats_df[
#         (player_stats_df['player_id'] == player_id) &
#         (player_stats_df['date'] < match_date) &
#         (player_stats_df['map_id'] == map_id)
#     ]
#     if len(player_data) < 5:
#         player_data = player_stats_df[(player_stats_df['player_id'] == player_id) & (player_stats_df['map_id'] == map_id)]
#     return player_data[statistic].mean()
