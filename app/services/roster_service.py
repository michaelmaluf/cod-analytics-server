from app.models.team import Team
from app.models.player import Player
from app.models.player_team_status import PlayerTeamStatus

class RosterService:
    def __init__(self, session):
        self.session = session

    def find_team_by_name(self, team_name):
        team = self.session.query(Team).filter_by(name=team_name).first()
        if not team:
            return self.create_team(team_name)
        return team

    def find_player_by_name(self, player_name):
        player = self.session.query(Player).filter_by(name=player_name).first()
        if not player:
            return self.create_player(player_name)
        return player

    def find_player_team_status(self, team, player):
        player_team_status = self.session.query(PlayerTeamStatus).filter_by(team=team, player=player).first()
        if not player_team_status:
            return self.create_player_team_status(team, player)
        return player_team_status


    def create_team(self, team_name):
        new_team = Team(name=team_name)
        self.session.add(new_team)
        self.session.commit()
        return new_team

    def create_player(self, player_name):
        new_player = Player(name=player_name)
        self.session.add(new_player)
        self.session.commit()
        return new_player

    def create_player_team_status(self, team, player):
        # sets active flag to false for previous player_team statuses (necessary logic to facilitate a player changing teams)
        previous_player_team_statuses = self.session.query(PlayerTeamStatus).filter_by(player=player)
        for previous_player_team_status in previous_player_team_statuses:
            if previous_player_team_status.active:
                previous_player_team_status.active = False
                self.session.add(previous_player_team_status)


        player_team_status = PlayerTeamStatus(team=team, player=player)
        self.session.add(player_team_status)
        self.session.commit()
        return player_team_status

    def get_or_create_teams(self, data):
        team_one = self.find_team_by_name(data['team_one_name'])
        team_two = self.find_team_by_name(data['team_two_name'])
        return [team_one, team_two]

    def get_or_create_player(self, team, player_name):
        """
        Logic ensures each players team has already been created in the db at this point.
        Player is created if player does not already exist.
        Player_team_status is created to link the player with the given team
        """
        player = self.find_player_by_name(player_name)
        player_team_status = self.find_player_team_status(team, player)
        return player