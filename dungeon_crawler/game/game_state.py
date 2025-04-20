from enum import Enum, auto

class GameState(Enum):
    """Game state enumeration to track the current state of the game."""
    MAIN_MENU = auto()
    OPTIONS = auto()
    PLAYING = auto()
    PAUSED = auto()
    INVENTORY = auto()
    GAME_OVER = auto()
    LEVEL_UP = auto()
    SHOP = auto()
    QUEST_LOG = auto()
    VICTORY = auto()
    CHARACTER_SCREEN = auto()
    MINIMAP_SCREEN = auto()
    SETTINGS = auto()
    CREDITS = auto() 