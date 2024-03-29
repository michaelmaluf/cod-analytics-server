from .match_service import MatchService
from .roster_service import RosterService
from .map_game_mode_service import MapGameModeService
from app.scraper import fetch_match_and_player_data


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

            for player_team_status in team_two.player_statuses:
                if player_team_status.active and player_team_status.player_id not in team_two_player_ids:
                    player_team_status.active = False

            self.session.commit()
            self.session.close()
