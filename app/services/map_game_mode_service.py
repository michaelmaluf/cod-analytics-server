from app.errors import GameModeNotFoundError
from app.database.models import Map, GameMode, MapGameModePair
from app.enums import GameModeType


class MapGameModeService:
    def __init__(self, session):
        self.session = session

    def get_or_create_map_mode_pair(self, map_name, mode_name):
        map = self.find_map_by_name(map_name)
        mode = self.find_mode_by_name(mode_name)
        map_mode_pair = self.find_pair_by_map_mode(map, mode)
        return map_mode_pair

    def find_map_by_name(self, map_name):
        map = self.session.query(Map).filter_by(name=map_name).first()
        if not map:
            return self.create_map(map_name)
        return map

    def find_mode_by_name(self, mode_name):
        try:
            game_mode_type = GameModeType.get_mode_by_value(mode_name)
            mode = self.session.query(GameMode).filter_by(name=game_mode_type).first()
            if not mode:
                return self.create_mode(game_mode_type)
            return mode
        except GameModeNotFoundError as e:
            print(e)

    def find_pair_by_map_mode(self, map, mode):
        map_mode_pair = self.session.query(MapGameModePair).filter_by(map=map, game_mode=mode).first()
        if not map_mode_pair:
            return self.create_map_mode_pair(map, mode)
        return map_mode_pair

    def create_map(self, map_name):
        new_map = Map(name=map_name)
        self.session.add(new_map)
        self.session.commit()
        return new_map

    def create_mode(self, game_mode_type):
        new_mode = GameMode(name=game_mode_type)
        self.session.add(new_mode)
        self.session.commit()
        return new_mode

    def create_map_mode_pair(self, map, mode):
        new_map_mode_pair = MapGameModePair()
        new_map_mode_pair.map = map
        new_map_mode_pair.game_mode = mode
        self.session.add(new_map_mode_pair)
        self.session.commit()
        return new_map_mode_pair
