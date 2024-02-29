from app.models.match import Match
from app.schemas import MatchSchema
from app.models.match_map import MatchMap
from app.models.player_data import PlayerData
from app.enums import GameModeType, type_to_objective_key


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
        objective_key = type_to_objective_key(map_game_mode_pair.game_mode)

        player_data_kwargs = {
            'player': player,
            'kills': raw_player_data['kills'],
            'deaths': raw_player_data['deaths'],
            'damage': raw_player_data['damage'],
            objective_key: raw_player_data['objectives']
        }

        player_data = PlayerData(**player_data_kwargs)

        return player_data
