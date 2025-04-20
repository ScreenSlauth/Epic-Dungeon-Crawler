# Epic Dungeon Crawler Game Package
# This file makes the 'game' directory a proper Python package 

"""Main game package containing all game logic, entities, and systems."""

# Import important classes for easier access
from .world.dungeon import Dungeon, Biome, Room
from .player import Player
from .enemy import Enemy
from .item import Item
from .game_state import GameState
from .sound_manager import SoundManager
from .quest_manager import QuestManager, Quest
from .tile import Tile, TileType
from .entity import Entity

# Import UI components
from .ui import HUD, MainMenu, OptionsMenu, Button

# Explicitly indicate what should be imported when using "from game import *"
__all__ = [
    'Dungeon', 'Biome', 'Room',
    'Player', 'Enemy', 'Item',
    'GameState', 'SoundManager', 'QuestManager', 'Quest',
    'Tile', 'TileType', 'Entity',
    'HUD', 'MainMenu', 'OptionsMenu', 'Button'
] 