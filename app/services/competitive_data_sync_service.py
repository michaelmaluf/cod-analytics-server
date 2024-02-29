
from .match_service import MatchService
from .roster_service import RosterService
from .map_game_mode_service import MapGameModeService

class CompetitiveDataSyncService:
    def __init__(self, session):
        self.session = session
        self.MatchService = MatchService(session)
        self.RosterService = RosterService(session)
        self.MapGameModeService = MapGameModeService(session)

    def populate_all_data(self, scraped_data):
        for data in scraped_data:
            team_one, team_two = self.RosterService.get_or_create_teams(data)
            match = self.MatchService.create_match(team_one, team_two, data)
            self.session.add(match)

            match_maps_data = data['match_maps']

            for match_map_data in match_maps_data:
                map_game_mode_pair = self.MapGameModeService.get_or_create_map_mode_pair(match_map_data.get('map'), match_map_data.get('game_mode'))
                match_map = self.MatchService.create_match_map(match, map_game_mode_pair, match_map_data)
                self.session.add(match_map)

                for raw_player_data in match_map_data['team_one_player_data']:
                    player = self.RosterService.get_or_create_player(team_one, raw_player_data['name'])
                    match_map.player_data.append(self.MatchService.create_player_data(player, raw_player_data, map_game_mode_pair))

                for raw_player_data in match_map_data['team_two_player_data']:
                    player = self.RosterService.get_or_create_player(team_two, raw_player_data['name'])
                    match_map.player_data.append(self.MatchService.create_player_data(player, raw_player_data, map_game_mode_pair))

                match.match_maps.append(match_map)

            self.session.commit()
