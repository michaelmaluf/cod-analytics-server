class GameModeNotFoundError(Exception):
    """Exception raised when a game mode is not found."""
    def __init__(self, game_mode_name, message="Game mode not found"):
        self.game_mode_name = game_mode_name
        self.message = f"{message}: {game_mode_name}"
        super().__init__(self.message)