def clean_data(df):
    clean_df = df.dropna(axis=1, how='all')
    return clean_df


def separate_features_and_labels(df):
    features = df.drop(['team_one_score', 'team_two_score'], axis=1)
    labels = df[['team_one_score', 'team_two_score']]
    return features, labels


def drop_columns(df):
    columns_to_drop = []

    for team in ['team_one', 'team_two']:
        # columns_to_drop.append(team)
        for player in ['player_one', 'player_two', 'player_three', 'player_four']:
            columns_to_drop.append(f'{team}_{player}_id')
            columns_to_drop.append(f'{team}_{player}_kills')
            columns_to_drop.append(f'{team}_{player}_deaths')
            columns_to_drop.append(f'{team}_{player}_damage')
            columns_to_drop.append(f'{team}_{player}_objectives')

    return df.drop(columns_to_drop, axis=1)
