from dotenv import load_dotenv

load_dotenv()

import copy

import pandas as pd
from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from app.database.models import Match, MatchMap
from app.enums import GameModeType


# create 3 df objects, one for each game mode

def fetch_match_data_from_match(game_mode, match):
    match_data_for_game_mode = []

    match_data = {
        'date': match.date,
        'stage': match.stage.value,
        'team_one': match.team_one_id,
        'team_two': match.team_two_id,
    }

    for match_map in match.match_maps:
        match_map_data = copy.deepcopy(match_data)
        if match_map.map_game_mode_pair.game_mode.name == game_mode:
            match_map_data['map_number'] = match_map.map_number
            match_map_data['map_id'] = match_map.map_game_mode_pair.map.id
            match_map_data['team_one_score'] = match_map.team_one_score
            match_map_data['team_two_score'] = match_map.team_two_score
            match_map_data.update(**fetch_player_data_from_match_map(game_mode, match_map.player_data))
            match_data_for_game_mode.append(match_map_data)

    return match_data_for_game_mode


def fetch_player_data_from_match_map(game_mode, player_data_for_match_map):
    player_data = {}

    player_idx = 0

    for team in ['team_one', 'team_two']:
        for player in ['player_one', 'player_two', 'player_three', 'player_four']:
            player_data[f'{team}_{player}_id'] = player_data_for_match_map[player_idx].player_id
            player_data[f'{team}_{player}_kills'] = player_data_for_match_map[player_idx].kills
            player_data[f'{team}_{player}_deaths'] = player_data_for_match_map[player_idx].deaths
            player_data[f'{team}_{player}_damage'] = player_data_for_match_map[player_idx].damage
            player_data[f'{team}_{player}_objectives'] = fetch_player_obj_for_match_map(game_mode, player_idx,
                                                                                        player_data_for_match_map)

            player_idx += 1

    return player_data


def fetch_player_obj_for_match_map(game_mode, player_idx, player_data_for_match_map):
    if game_mode == GameModeType.HARDPOINT:
        return player_data_for_match_map[player_idx].hill_time
    elif game_mode == GameModeType.SEARCH_AND_DESTROY:
        return player_data_for_match_map[player_idx].first_bloods
    else:
        return player_data_for_match_map[player_idx].captures


def fetch_data(game_mode, db_session):
    matches = db_session.query(Match).options(
        selectinload(Match.match_maps).selectinload(MatchMap.player_data)
    ).all()
    match_data_dicts = []
    for match in matches:
        match_data = fetch_match_data_from_match(game_mode, match)
        match_data_dicts.extend(match_data)
    df_for_game_mode = pd.DataFrame(match_data_dicts)
    return df_for_game_mode


def fetch_data_for_predictions(game_mode, db_session, team_one_id, team_two_id):
    matches = db_session.query(Match).filter(
        or_(
            Match.team_one_id == team_one_id,
            Match.team_two_id == team_one_id,
            Match.team_one_id == team_two_id,
            Match.team_two_id == team_two_id
        )
    ).all()
    match_data_dicts = []
    for match in matches:
        match_data = fetch_match_data_from_match(game_mode, match)
        match_data_dicts.extend(match_data)
    df_for_game_mode = pd.DataFrame(match_data_dicts)
    return df_for_game_mode
