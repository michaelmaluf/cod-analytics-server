from datetime import datetime

from sqlalchemy.sql import text
import pandas as pd

from .model_service import ModelService
from .roster_service import RosterService
from .map_game_mode_service import MapGameModeService
from database.models import Team, PlayerTeamStatus, Player, GameMode, Map
from machine_learning.data_preparation import fetch_data_for_predictions, get_team_performance_df, \
    get_player_performance_df, scale_predictions
from app.enums import GameModeType, Stage
from app import const


class PredictionService:
    def __init__(self, session):
        self.session = session
        self.ModelService = ModelService(session)
        self.RosterService = RosterService(session)
        self.MapGameModeService = MapGameModeService(session)

    def get_map_predictions(self, prediction_request):
        game_mode = GameModeType[prediction_request['game_mode'].upper()]
        prediction_df = self.compute_prediction_df(game_mode, prediction_request)

        if game_mode == GameModeType.HARDPOINT:
            predictions = self.ModelService.HardpointModel.predict(prediction_df)
            scaled_predictions = scale_predictions(predictions, const.HARDPOINT_TARGET_SCORE)
        elif game_mode == GameModeType.SEARCH_AND_DESTROY:
            predictions = self.ModelService.SearchAndDestroyModel.predict(prediction_df)
            scaled_predictions = scale_predictions(predictions, const.SEARCH_AND_DESTROY_TARGET_SCORE)
        else:
            predictions = self.ModelService.ControlModel.predict(prediction_df)
            scaled_predictions = scale_predictions(predictions, const.CONTROL_TARGET_SCORE)

        return scaled_predictions

    def compute_prediction_df(self, game_mode, prediction_request):
        map_id = self.MapGameModeService.find_map_by_name(prediction_request['map']).id

        prediction_dict = {
            'stage': self.compute_current_stage(),
            'map_id': map_id,
            **self.get_teams_and_player_data(game_mode, map_id, prediction_request),
        }

        return pd.DataFrame(prediction_dict, index=[0])


    def get_teams_and_player_data(self, game_mode, map_id, prediction_request):
        team_one = self.RosterService.find_team_by_team_name(prediction_request['team_one_name'])
        team_two = self.RosterService.find_team_by_team_name(prediction_request['team_two_name'])
        team_one_players = self.RosterService.find_active_players_on_team(team_one)
        team_two_players = self.RosterService.find_active_players_on_team(team_two)

        df = fetch_data_for_predictions(game_mode, self.session, team_one.id, team_two.id)
        team_df = get_team_performance_df(df)
        player_df = get_player_performance_df(df)

        team_one_averages = self.compute_team_averages('team_one', map_id, team_df, team_one.id)
        team_two_averages = self.compute_team_averages('team_two', map_id, team_df, team_two.id)

        team_one_player_averages = self.compute_player_averages('team_one', map_id, player_df, team_one_players)
        team_two_player_averages = self.compute_player_averages('team_two', map_id, player_df, team_two_players)

        team_and_player_data = {
            'team_one': team_one.id,
            'team_two': team_two.id,
            **team_one_averages,
            **team_two_averages,
            **team_one_player_averages,
            **team_two_player_averages
        }

        return team_and_player_data

    def compute_team_averages(self, team_number, map_id, team_df, team_id):
        team_averages = {}

        df_all_maps = team_df[team_df['team'] == team_id]
        df_with_map_id = df_all_maps[df_all_maps['map_id'] == map_id]

        team_averages[f'avg_game_mode_score_{team_number}'] = df_all_maps['team_score'].mean()
        team_averages[f'avg_game_mode_score_{team_number}_against'] = df_all_maps['opponent_score'].mean()
        team_averages[f'avg_map_game_mode_score_{team_number}'] = df_with_map_id['team_score'].mean()
        team_averages[f'avg_map_game_mode_score_{team_number}_against'] = df_with_map_id['opponent_score'].mean()

        return team_averages

    def compute_player_averages(self, team_number, map_id, player_df, players):
        player_averages = {}
        player_numbers = ['player_one', 'player_two', 'player_three', 'player_four']

        # Group by 'player_id' for overall averages
        overall_averages = player_df.groupby('player_id')[['kills', 'deaths', 'damage', 'objectives']].mean()

        # Group by both 'player_id' and 'map_id' for map-specific averages
        map_specific_averages = player_df[player_df['map_id'] == map_id].groupby('player_id')[
            ['kills', 'deaths', 'damage', 'objectives']].mean()

        for player, player_number in zip(players, player_numbers):
            player_id = player.player_id
            player_avg = {
                f'avg_game_mode_kills_{team_number}_{player_number}': overall_averages.at[player_id, 'kills'],
                f'avg_game_mode_deaths_{team_number}_{player_number}': overall_averages.at[player_id, 'deaths'],
                f'avg_game_mode_damage_{team_number}_{player_number}': overall_averages.at[player_id, 'damage'],
                f'avg_game_mode_objectives_{team_number}_{player_number}': overall_averages.at[player_id, 'objectives'],
                f'avg_map_game_mode_kills_{team_number}_{player_number}': map_specific_averages.at[
                    player_id, 'kills'] if player_id in map_specific_averages.index else None,
                f'avg_map_game_mode_deaths_{team_number}_{player_number}': map_specific_averages.at[
                    player_id, 'deaths'] if player_id in map_specific_averages.index else None,
                f'avg_map_game_mode_damage_{team_number}_{player_number}': map_specific_averages.at[
                    player_id, 'damage'] if player_id in map_specific_averages.index else None,
                f'avg_map_game_mode_objectives_{team_number}_{player_number}': map_specific_averages.at[
                    player_id, 'objectives'] if player_id in map_specific_averages.index else None,
            }

            player_averages.update(player_avg)

        return player_averages


    def compute_current_stage(self):
        current_date = datetime.now()

        if current_date >= datetime(2024, 6, 24):
            return Stage.CHAMPS
        elif current_date >= datetime(2024, 5, 20):
            return Stage.MAJOR_4
        elif current_date >= datetime(2024, 3, 25):
            return Stage.MAJOR_3
        elif current_date >= datetime(2024, 1, 29):
            return Stage.MAJOR_2
        else:
            return Stage.MAJOR_1
