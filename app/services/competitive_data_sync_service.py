import pandas as pd

from .match_service import MatchService
from .roster_service import RosterService
from .map_game_mode_service import MapGameModeService
from app.scraper import fetch_match_and_player_data
from app.enums import GameModeType
from app.database.models import PlayerTeamStatus, Player
import app.const as const


class CompetitiveDataSyncService:
    def __init__(self, session):
        self.session = session
        self.MatchService = MatchService(session)
        self.RosterService = RosterService(session)
        self.MapGameModeService = MapGameModeService(session)

    def populate_all_data(self):
        scraped_data = fetch_match_and_player_data()
        for data in scraped_data:
            team_one, team_two = self.RosterService.get_or_create_teams(data)
            match = self.MatchService.create_match(team_one, team_two, data)
            self.session.add(match)

            match_maps_data = data['match_maps']
            team_one_player_ids = set()
            team_two_player_ids = set()

            for match_map_data in match_maps_data:
                map_game_mode_pair = self.MapGameModeService.get_or_create_map_mode_pair(match_map_data.get('map'),
                                                                                         match_map_data.get(
                                                                                             'game_mode'))
                match_map = self.MatchService.create_match_map(match, map_game_mode_pair, match_map_data)
                self.session.add(match_map)

                for raw_player_data in match_map_data['team_one_player_data']:
                    player = self.RosterService.get_or_create_player(team_one, raw_player_data['name'])
                    team_one_player_ids.add(player.id)
                    match_map.player_data.append(
                        self.MatchService.create_player_data(player, raw_player_data, map_game_mode_pair))

                for raw_player_data in match_map_data['team_two_player_data']:
                    player = self.RosterService.get_or_create_player(team_two, raw_player_data['name'])
                    team_two_player_ids.add(player.id)
                    match_map.player_data.append(
                        self.MatchService.create_player_data(player, raw_player_data, map_game_mode_pair))

                match.match_maps.append(match_map)

            # updates team statuses for players who are no longer on the team
            for player_team_status in team_one.player_statuses:
                if player_team_status.active and player_team_status.player_id not in team_one_player_ids:
                    player_team_status.active = False
                elif not player_team_status.active and player_team_status.player_id in team_one_player_ids:
                    player_team_status.active = True

            for player_team_status in team_two.player_statuses:
                if player_team_status.active and player_team_status.player_id not in team_two_player_ids:
                    player_team_status.active = False
                elif not player_team_status.active and player_team_status.player_id in team_two_player_ids:
                    player_team_status.active = True

            self.session.commit()
            self.session.close()

    def update_player_rankings_for_game_modes(self):
        all_rankings = pd.DataFrame()

        for game_mode in GameModeType:
            player_averages_df = self.MatchService.get_all_player_averages_for_game_mode(game_mode)

            for index, player in player_averages_df.iterrows():
                if self.session.query(PlayerTeamStatus).filter_by(player_id=player['player_id'], active=True).count() == 0:
                    player_averages_df.drop(index, inplace=True)

            players = player_averages_df.iloc[:, [0]]
            player_averages_df.drop(player_averages_df.columns[0], axis=1, inplace=True)

            player_averages_df['kd_ratio'] = player_averages_df['average_kills'] / player_averages_df['average_deaths']
            player_averages_df['average_engagements'] = player_averages_df['average_kills'] + player_averages_df['average_deaths']
            df_normalized = (player_averages_df - player_averages_df.min()) / (player_averages_df.max() - player_averages_df.min())

            players['aggregate_normalized_score'] = self.calculate_aggregate_normalized_scores(df_normalized, game_mode)
            players[f'{game_mode.name}_rank'] = players['aggregate_normalized_score'].rank(ascending=False, method='dense').astype(int)
            players.drop('aggregate_normalized_score', axis=1, inplace=True)

            if all_rankings.empty:
                all_rankings = players
            else:
                all_rankings = pd.merge(all_rankings, players, on='player_id', how='inner')

        for index, row in all_rankings.iterrows():
            player = self.session.query(Player).filter_by(id=row['player_id']).first()
            if player:
                player.hardpoint_rank = row['HARDPOINT_rank']
                player.search_and_destroy_rank = row['SEARCH_AND_DESTROY_rank']
                player.control_rank = row['CONTROL_rank']

        self.session.commit()
        self.session.close()

    def calculate_aggregate_normalized_scores(self, df_normalized, game_mode):
        weights = const.WEIGHTS_PER_GAME_MODE[game_mode.value]

        aggregate_normalized_scores = df_normalized['average_kills'] * weights['kills'] - \
                                      df_normalized['average_deaths'] * weights['deaths'] + \
                                      df_normalized['average_damage'] * weights['damage'] + \
                                      df_normalized['average_objectives'] * weights['objectives'] + \
                                      df_normalized['kd_ratio'] * weights['kd'] + \
                                      df_normalized['average_engagements'] * weights['engagements']

        return aggregate_normalized_scores