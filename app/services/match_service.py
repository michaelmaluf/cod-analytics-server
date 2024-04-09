from sqlalchemy import func
import pandas as pd

from app.database.models import Match, MatchMap, PlayerData, MapGameModePair, GameMode
from app.schemas import MatchSchema


class MatchService:
    def __init__(self, session):
        self.session = session
        self.match_schema = MatchSchema()

    def create_match(self, team_one, team_two, data):
        match_data = self.match_schema.load(data)
        match = Match(**match_data)
        match.team_one = team_one
        match.team_two = team_two
        return match

    def create_match_map(self, match, map_game_mode_pair, match_map_data):
        match_map = MatchMap(
            match=match,
            map_game_mode_pair=map_game_mode_pair,
            map_number=match_map_data['map_number'],
            team_one_score=match_map_data['team_one_score'],
            team_two_score=match_map_data['team_two_score']
        )
        return match_map

    def create_player_data(self, player, raw_player_data, map_game_mode_pair):
        objective_key = map_game_mode_pair.game_mode.name.to_objective_key()

        player_data_kwargs = {
            'player': player,
            'kills': raw_player_data['kills'],
            'deaths': raw_player_data['deaths'],
            'damage': raw_player_data['damage'],
            objective_key: raw_player_data['objectives']
        }

        player_data = PlayerData(**player_data_kwargs)

        return player_data

    def get_all_player_averages_for_game_mode(self, game_mode):
        objective_key = game_mode.to_objective_key()

        player_averages = self.session.query(
            PlayerData.player_id,
            func.avg(PlayerData.kills).label('average_kills'),
            func.avg(PlayerData.deaths).label('average_deaths'),
            func.avg(PlayerData.damage).label('average_damage'),
            func.avg(getattr(PlayerData, objective_key)).label(f'average_objectives')
        ).join(PlayerData.match_map
               ).join(MatchMap.map_game_mode_pair
                      ).join(MapGameModePair.game_mode
                             ).filter(GameMode.name == game_mode
                                      ).group_by(PlayerData.player_id
                                                 ).all()

        return pd.DataFrame(player_averages)
