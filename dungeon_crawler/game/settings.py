# Game settings

# Screen dimensions
TILE_SIZE = 32
GRID_WIDTH = 60
GRID_HEIGHT = 40
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT
FPS = 60

# Camera and Viewport
VIEWPORT_WIDTH = GRID_WIDTH
VIEWPORT_HEIGHT = GRID_HEIGHT
VIEW_PADDING = 5

# Minimap settings
MINIMAP_SIZE = 180
MINIMAP_SCALE = 0.2
MINIMAP_POSITION = (SCREEN_WIDTH - MINIMAP_SIZE - 20, 20)
MINIMAP_BORDER_COLOR = (200, 200, 200)
MINIMAP_PLAYER_COLOR = (0, 255, 0)
MINIMAP_ENEMY_COLOR = (255, 0, 0)
MINIMAP_ITEM_COLOR = (255, 255, 0)
MINIMAP_WALL_COLOR = (100, 100, 100)
MINIMAP_FLOOR_COLOR = (50, 50, 50)
MINIMAP_EXIT_COLOR = (0, 255, 255)
MINIMAP_UNEXPLORED_COLOR = (0, 0, 0)

# Layer rendering order
LAYERS = {
    "FLOOR": 0,
    "ITEMS": 1,
    "ENEMIES": 2,
    "PLAYER": 3,
    "EFFECTS": 4,
    "UI": 5
}

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_ORANGE = (255, 165, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)

# Enhanced Biome colors and features
BIOME_COLORS = {
    "CAVERN": {
        "WALL": (60, 60, 65),
        "FLOOR": (40, 40, 45),
        "AMBIENT": (100, 100, 120),
        "ACCENT": (70, 70, 90),
        "WATER": (30, 50, 120),
        "VEGETATION": (60, 70, 50),
        "HAZARD": (150, 30, 30),
        "DESCRIPTION": "Dark caverns with occasional water puddles and glowing fungi"
    },
    "FOREST": {
        "WALL": (60, 100, 60),
        "FLOOR": (30, 90, 30),
        "AMBIENT": (20, 150, 20),
        "ACCENT": (120, 150, 80),
        "WATER": (50, 150, 200),
        "VEGETATION": (30, 120, 40),
        "HAZARD": (180, 100, 30),
        "DESCRIPTION": "Lush forest with tall trees, dense vegetation, and forest streams"
    },
    "ICE": {
        "WALL": (200, 220, 255),
        "FLOOR": (170, 190, 255),
        "AMBIENT": (210, 230, 255),
        "ACCENT": (240, 240, 255),
        "WATER": (100, 150, 240),
        "VEGETATION": (200, 240, 240),
        "HAZARD": (150, 200, 240),
        "DESCRIPTION": "Frozen landscape with icy walls, slippery floors, and snow drifts"
    },
    "LAVA": {
        "WALL": (150, 60, 40),
        "FLOOR": (120, 40, 30),
        "AMBIENT": (255, 120, 40),
        "ACCENT": (220, 160, 50),
        "WATER": (255, 50, 20),
        "VEGETATION": (170, 100, 20),
        "HAZARD": (255, 70, 0),
        "DESCRIPTION": "Volcanic caverns with flowing lava, smoke vents, and scorched ground"
    },
    "SHADOW": {
        "WALL": (30, 15, 40),
        "FLOOR": (20, 10, 30),
        "AMBIENT": (60, 0, 120),
        "ACCENT": (90, 30, 120),
        "WATER": (40, 0, 80),
        "VEGETATION": (70, 20, 100),
        "HAZARD": (150, 0, 150),
        "DESCRIPTION": "Shadowy realm with void-like terrain, eerie lights, and strange formations"
    },
    "CRYSTAL": {
        "WALL": (120, 150, 180),
        "FLOOR": (90, 130, 170),
        "AMBIENT": (150, 200, 255),
        "ACCENT": (200, 220, 255),
        "WATER": (100, 200, 220),
        "VEGETATION": (150, 220, 230),
        "HAZARD": (230, 100, 200),
        "DESCRIPTION": "Gleaming crystal caverns with refractive surfaces and glowing minerals"
    }
}

# Biome-specific game features
BIOME_FEATURES = {
    "CAVERN": {
        "ENEMY_TYPES": ["goblin", "skeleton", "orc"],
        "ITEM_RARITY_BONUS": 0,
        "LIGHT_RADIUS": 0,
        "AMBIENT_SOUNDS": ["drip", "rumble", "wind"],
        "SPECIAL_EFFECTS": ["dust_particles"]
    },
    "FOREST": {
        "ENEMY_TYPES": ["lynx", "goblin", "spider"],
        "ITEM_RARITY_BONUS": 1,
        "LIGHT_RADIUS": 2,
        "AMBIENT_SOUNDS": ["birds", "leaves", "wind"],
        "SPECIAL_EFFECTS": ["leaf_particles", "sunbeams"]
    },
    "ICE": {
        "ENEMY_TYPES": ["frost_troll", "ice_elemental", "wolf"],
        "ITEM_RARITY_BONUS": 2,
        "LIGHT_RADIUS": 3,
        "AMBIENT_SOUNDS": ["wind", "ice_crack", "howl"],
        "SPECIAL_EFFECTS": ["snow_particles", "breath_fog"]
    },
    "LAVA": {
        "ENEMY_TYPES": ["magma_elemental", "fire_demon", "salamander"],
        "ITEM_RARITY_BONUS": 3,
        "LIGHT_RADIUS": 4,
        "AMBIENT_SOUNDS": ["lava_bubble", "rumble", "roar"],
        "SPECIAL_EFFECTS": ["ember_particles", "heat_distortion"]
    },
    "SHADOW": {
        "ENEMY_TYPES": ["shadow_wraith", "void_beast", "corrupted_one"],
        "ITEM_RARITY_BONUS": 4,
        "LIGHT_RADIUS": -2,
        "AMBIENT_SOUNDS": ["whispers", "void_noise", "heartbeat"],
        "SPECIAL_EFFECTS": ["shadow_tendrils", "void_particles"]
    },
    "CRYSTAL": {
        "ENEMY_TYPES": ["crystal_golem", "light_elemental", "crystal_spider"],
        "ITEM_RARITY_BONUS": 5,
        "LIGHT_RADIUS": 5,
        "AMBIENT_SOUNDS": ["crystal_chime", "resonance", "ping"],
        "SPECIAL_EFFECTS": ["light_refraction", "crystal_growth"]
    }
}

# Gameplay constants
VISIBILITY_RADIUS = 8
MAX_LEVEL = 20
XP_BASE_REQUIREMENT = 100
XP_LEVEL_MULTIPLIER = 1.5
HEALTH_BASE = 100
HEALTH_LEVEL_INCREASE = 20
DAMAGE_BASE = 10
DAMAGE_LEVEL_INCREASE = 5

# Enemy stats
ENEMY_STATS = {
    "goblin": {
        "health": 50,
        "damage": 10,
        "speed": 0.5,
        "xp_reward": 20,
        "gold_reward": 5
    },
    "skeleton": {
        "health": 70,
        "damage": 15,
        "speed": 0.3,
        "xp_reward": 30,
        "gold_reward": 8
    },
    "orc": {
        "health": 100,
        "damage": 20,
        "speed": 0.4,
        "xp_reward": 40,
        "gold_reward": 12
    },
    "lynx": {
        "health": 60,
        "damage": 25,
        "speed": 0.7,
        "xp_reward": 35,
        "gold_reward": 7
    },
    "frost_troll": {
        "health": 120,
        "damage": 30,
        "speed": 0.3,
        "xp_reward": 50,
        "gold_reward": 15
    },
    "magma_elemental": {
        "health": 150,
        "damage": 35,
        "speed": 0.4,
        "xp_reward": 60,
        "gold_reward": 20
    },
    "shadow_wraith": {
        "health": 80,
        "damage": 40,
        "speed": 0.6,
        "xp_reward": 45,
        "gold_reward": 10
    },
    # New enemies for additional biomes
    "spider": {
        "health": 40,
        "damage": 15,
        "speed": 0.8,
        "xp_reward": 25,
        "gold_reward": 6
    },
    "ice_elemental": {
        "health": 90,
        "damage": 25,
        "speed": 0.4,
        "xp_reward": 40,
        "gold_reward": 12
    },
    "wolf": {
        "health": 70,
        "damage": 20,
        "speed": 0.6,
        "xp_reward": 30,
        "gold_reward": 8
    },
    "fire_demon": {
        "health": 130,
        "damage": 40,
        "speed": 0.3,
        "xp_reward": 55,
        "gold_reward": 18
    },
    "salamander": {
        "health": 85,
        "damage": 30,
        "speed": 0.5,
        "xp_reward": 45,
        "gold_reward": 14
    },
    "void_beast": {
        "health": 110,
        "damage": 45,
        "speed": 0.4,
        "xp_reward": 60,
        "gold_reward": 20
    },
    "corrupted_one": {
        "health": 95,
        "damage": 35,
        "speed": 0.5,
        "xp_reward": 50,
        "gold_reward": 15
    },
    "crystal_golem": {
        "health": 140,
        "damage": 30,
        "speed": 0.3,
        "xp_reward": 60,
        "gold_reward": 20
    },
    "light_elemental": {
        "health": 100,
        "damage": 30,
        "speed": 0.5,
        "xp_reward": 55,
        "gold_reward": 18
    },
    "crystal_spider": {
        "health": 70,
        "damage": 25,
        "speed": 0.7,
        "xp_reward": 40,
        "gold_reward": 12
    }
}

# Item effects
ITEM_EFFECTS = {
    # Consumables
    "health_potion_small": {
        "health": 30,
        "description": "Restores 30 health points",
        "rarity": "common",
        "spawn_rate": 0.7
    },
    "health_potion_medium": {
        "health": 75,
        "description": "Restores 75 health points",
        "rarity": "uncommon",
        "spawn_rate": 0.5
    },
    "health_potion_large": {
        "health": 150,
        "description": "Restores 150 health points",
        "rarity": "rare", 
        "spawn_rate": 0.3
    },
    "mana_potion_small": {
        "mana": 30,
        "description": "Restores 30 mana points",
        "rarity": "common",
        "spawn_rate": 0.6
    },
    "mana_potion_medium": {
        "mana": 75,
        "description": "Restores 75 mana points",
        "rarity": "uncommon",
        "spawn_rate": 0.4
    },
    "mana_potion_large": {
        "mana": 150,
        "description": "Restores 150 mana points",
        "rarity": "rare",
        "spawn_rate": 0.2
    },
    "strength_potion": {
        "damage": 10,
        "duration": 20,
        "description": "Increases damage by 10 for 20 turns",
        "rarity": "uncommon",
        "spawn_rate": 0.3
    },
    "elixir_of_life": {
        "health": 100,
        "health_regen": 5,
        "duration": 10,
        "description": "Restores 100 health and grants 5 health regeneration for 10 turns",
        "rarity": "rare",
        "spawn_rate": 0.15
    },
    "potion_of_invisibility": {
        "stealth": 50,
        "duration": 15,
        "description": "Grants 50% stealth, making enemies less likely to notice you for 15 turns",
        "rarity": "rare",
        "spawn_rate": 0.15
    },
    "potion_of_haste": {
        "speed": 2,
        "duration": 10,
        "description": "Doubles movement speed for 10 turns",
        "rarity": "uncommon",
        "spawn_rate": 0.2
    },
    
    # Weapons
    "wooden_stick": {
        "damage": 5,
        "description": "A simple wooden stick",
        "rarity": "common",
        "spawn_rate": 0.5,
        "min_level": 1
    },
    "iron_dagger": {
        "damage": 10,
        "description": "A small iron dagger",
        "rarity": "common",
        "spawn_rate": 0.4,
        "min_level": 1
    },
    "iron_sword": {
        "damage": 15,
        "description": "A basic iron sword that increases damage by 15",
        "rarity": "common",
        "spawn_rate": 0.3,
        "min_level": 2
    },
    "steel_sword": {
        "damage": 25,
        "description": "A sturdy steel sword that increases damage by 25",
        "rarity": "uncommon",
        "spawn_rate": 0.25,
        "min_level": 5
    },
    "enchanted_blade": {
        "damage": 35,
        "magic_damage": 15,
        "description": "Magical sword that deals physical and magical damage",
        "rarity": "rare",
        "spawn_rate": 0.15,
        "min_level": 8
    },
    "obsidian_axe": {
        "damage": 45,
        "cleave": 15,
        "description": "Obsidian axe that can cleave through multiple enemies",
        "rarity": "rare",
        "spawn_rate": 0.1,
        "min_level": 10
    },
    "frost_wand": {
        "magic_damage": 30,
        "freeze_chance": 0.2,
        "description": "Staff that deals magic damage with a chance to freeze enemies",
        "rarity": "rare",
        "spawn_rate": 0.1,
        "min_level": 12
    },
    "flame_sword": {
        "damage": 40,
        "fire_damage": 20,
        "description": "Flaming sword that deals additional fire damage",
        "rarity": "epic",
        "spawn_rate": 0.05,
        "min_level": 15
    },
    
    # Armor
    "leather_armor": {
        "defense": 5,
        "description": "Basic leather armor that provides 5 defense",
        "rarity": "common",
        "spawn_rate": 0.4,
        "min_level": 1
    },
    "chainmail": {
        "defense": 10,
        "description": "Chainmail armor that provides 10 defense",
        "rarity": "common",
        "spawn_rate": 0.3,
        "min_level": 3
    },
    "steel_armor": {
        "defense": 15,
        "description": "Steel armor that provides 15 defense",
        "rarity": "uncommon",
        "spawn_rate": 0.25,
        "min_level": 6
    },
    "plate_armor": {
        "defense": 20,
        "description": "Heavy plate armor that provides 20 defense",
        "rarity": "uncommon",
        "spawn_rate": 0.2,
        "min_level": 9
    },
    "crystal_shield": {
        "defense": 15,
        "magic_resist": 20,
        "description": "Crystal shield that blocks physical and magical attacks",
        "rarity": "rare",
        "spawn_rate": 0.15,
        "min_level": 12
    },
    "dragonscale_armor": {
        "defense": 30,
        "fire_resist": 50,
        "description": "Dragon scale armor providing excellent protection, especially against fire",
        "rarity": "epic",
        "spawn_rate": 0.05,
        "min_level": 15
    },
    
    # Accessories
    "ring_of_health": {
        "health": 25,
        "health_regen": 1,
        "description": "Increases max health by 25 and adds 1 health regeneration per turn",
        "rarity": "uncommon",
        "spawn_rate": 0.2,
        "slot": "ring"
    },
    "ring_of_power": {
        "damage": 10,
        "description": "Increases damage by 10",
        "rarity": "uncommon",
        "spawn_rate": 0.2,
        "slot": "ring"
    },
    "amulet_of_protection": {
        "defense": 10,
        "description": "Increases defense by a flat 10 points",
        "rarity": "uncommon",
        "spawn_rate": 0.2,
        "slot": "amulet"
    },
    "pendant_of_shadows": {
        "stealth": 25,
        "description": "Shrouds the wearer in shadows, making them harder to detect",
        "rarity": "rare",
        "spawn_rate": 0.1,
        "slot": "amulet"
    },
    "amulet_of_reflection": {
        "reflect_damage": 0.15,
        "description": "Reflects 15% of damage back to attackers",
        "rarity": "rare",
        "spawn_rate": 0.1,
        "slot": "amulet"
    },
    "crown_of_wisdom": {
        "mana": 50,
        "mana_regen": 3,
        "description": "Increases max mana by 50 and adds 3 mana regeneration per turn",
        "rarity": "epic",
        "spawn_rate": 0.05,
        "slot": "amulet"
    },
    
    # Gold and treasure
    "gold_small": {
        "gold": 20,
        "description": "A small pile of gold",
        "rarity": "common",
        "spawn_rate": 0.8
    },
    "gold_medium": {
        "gold": 50,
        "description": "A medium pile of gold",
        "rarity": "common",
        "spawn_rate": 0.5
    },
    "gold_large": {
        "gold": 100,
        "description": "A large pile of gold",
        "rarity": "uncommon",
        "spawn_rate": 0.3
    },
    "treasure_chest": {
        "gold": 200,
        "item_chance": 0.5,
        "description": "A treasure chest containing gold and possibly other items",
        "rarity": "rare",
        "spawn_rate": 0.1
    }
}

# Item rarity colors
RARITY_COLORS = {
    "common": (200, 200, 200),      # Grey
    "uncommon": (30, 255, 30),      # Green
    "rare": (30, 144, 255),         # Blue
    "epic": (138, 43, 226),         # Purple
    "legendary": (255, 165, 0)      # Orange
}

# Add item drop rates by biome
BIOME_ITEM_DROP_RATES = {
    "CAVERN": {
        "common_multiplier": 1.0,
        "uncommon_multiplier": 0.8,
        "rare_multiplier": 0.6,
        "epic_multiplier": 0.4,
        "legendary_multiplier": 0.2,
        "special_items": ["iron_sword", "leather_armor", "chainmail"]
    },
    "FOREST": {
        "common_multiplier": 1.2,
        "uncommon_multiplier": 1.0,
        "rare_multiplier": 0.7,
        "epic_multiplier": 0.5,
        "legendary_multiplier": 0.25,
        "special_items": ["wooden_stick", "ring_of_health", "potion_of_haste"]
    },
    "ICE": {
        "common_multiplier": 0.9,
        "uncommon_multiplier": 1.2,
        "rare_multiplier": 0.9,
        "epic_multiplier": 0.6,
        "legendary_multiplier": 0.3,
        "special_items": ["frost_wand", "crystal_shield"]
    },
    "LAVA": {
        "common_multiplier": 0.8,
        "uncommon_multiplier": 1.0,
        "rare_multiplier": 1.2,
        "epic_multiplier": 0.8,
        "legendary_multiplier": 0.4,
        "special_items": ["flame_sword", "obsidian_axe"]
    },
    "SHADOW": {
        "common_multiplier": 0.7,
        "uncommon_multiplier": 0.9,
        "rare_multiplier": 1.3,
        "epic_multiplier": 1.0,
        "legendary_multiplier": 0.5,
        "special_items": ["pendant_of_shadows", "potion_of_invisibility"]
    },
    "CRYSTAL": {
        "common_multiplier": 0.5,
        "uncommon_multiplier": 0.8,
        "rare_multiplier": 1.5,
        "epic_multiplier": 1.2,
        "legendary_multiplier": 0.7,
        "special_items": ["crystal_shield", "crown_of_wisdom"]
    }
}

# Level-based item drop rates
LEVEL_DROP_RATES = {
    # Level ranges (inclusive): multipliers for different rarities
    (1, 4): {"common": 1.5, "uncommon": 0.8, "rare": 0.3, "epic": 0.1, "legendary": 0.01},
    (5, 9): {"common": 1.0, "uncommon": 1.2, "rare": 0.6, "epic": 0.2, "legendary": 0.05},
    (10, 14): {"common": 0.7, "uncommon": 1.0, "rare": 1.0, "epic": 0.4, "legendary": 0.1},
    (15, 19): {"common": 0.5, "uncommon": 0.8, "rare": 1.2, "epic": 0.8, "legendary": 0.2},
    (20, 100): {"common": 0.3, "uncommon": 0.6, "rare": 1.0, "epic": 1.0, "legendary": 0.3}
}

# UI constants - Enhanced for better visuals
UI_PADDING = 12
UI_BORDER_SIZE = 2
UI_BORDER_RADIUS = 8
UI_FONT_SIZE = 24
UI_HEADING_SIZE = 32
UI_TITLE_SIZE = 48
UI_ELEMENT_HEIGHT = 50
UI_ELEMENT_WIDTH = 220
UI_COLORS = {
    "BACKGROUND": (20, 22, 30, 220),         # Darker, slightly blue-tinted, more transparent
    "BACKGROUND_ALT": (30, 34, 45, 220),     # Alternative background for variety
    "PANEL_BG": (25, 27, 35, 240),           # Panel background
    "BORDER": (70, 90, 120),                 # Blueish border
    "BORDER_HIGHLIGHT": (100, 140, 180),     # Highlighted border
    "TEXT": (230, 230, 240),                 # Slightly blue-tinted white text
    "TEXT_DARK": (180, 180, 190),            # Darker text for secondary information
    "HIGHLIGHT": (255, 180, 50),             # Golden highlight color
    "HIGHLIGHT_ALT": (100, 200, 255),        # Alternative highlight (blue)
    "BUTTON": (50, 60, 80),                  # Darker blue button
    "BUTTON_HOVER": (70, 85, 110),           # Lighter blue when hovering
    "BUTTON_ACTIVE": (90, 110, 140),         # Button active/pressed state
    "HEALTH_BAR": (220, 50, 50),             # Red health bar
    "HEALTH_BAR_BG": (80, 25, 25),           # Health bar background
    "XP_BAR": (90, 200, 90),                 # Green XP bar
    "XP_BAR_BG": (30, 70, 30),               # XP bar background
    "MANA_BAR": (50, 90, 220),               # Blue mana bar
    "MANA_BAR_BG": (20, 35, 80),             # Mana bar background
    "ENERGY_BAR": (220, 200, 50),            # Yellow energy bar
    "ENERGY_BAR_BG": (80, 70, 20),           # Energy bar background
    "INVENTORY_SLOT": (40, 45, 60),          # Inventory slot background
    "INVENTORY_SELECTED": (70, 85, 120),     # Selected inventory slot
    "TOOLTIP_BG": (30, 35, 50, 240),         # Tooltip background
    "SUCCESS": (100, 200, 100),              # Success messages/indicators
    "WARNING": (255, 180, 50),               # Warning messages/indicators
    "ERROR": (230, 60, 60),                  # Error messages/indicators
    "CAVERN_THEME": (60, 60, 80),            # Cavern theme color for UI
    "FOREST_THEME": (60, 100, 60),           # Forest theme
    "ICE_THEME": (170, 190, 255),            # Ice theme
    "LAVA_THEME": (150, 60, 40),             # Lava theme
    "SHADOW_THEME": (50, 30, 80),            # Shadow theme
    "CRYSTAL_THEME": (120, 150, 180)         # Crystal theme
}

# Animation settings
ANIMATION_SPEEDS = {
    "VERY_SLOW": 0.2,
    "SLOW": 0.5,
    "NORMAL": 1.0,
    "FAST": 1.5,
    "VERY_FAST": 2.0
}

# UI Animation effects
UI_ANIMATIONS = {
    "BUTTON_PULSE": True,        # Pulsing effect for buttons
    "HEALTH_BAR_PULSE": True,    # Health bar pulses when low
    "DAMAGE_NUMBERS": True,      # Floating damage numbers
    "XP_GAIN_EFFECT": True,      # Visual effect when gaining XP
    "LEVEL_UP_EFFECT": True,     # Special effect on level up
    "MENU_TRANSITIONS": True     # Smooth transitions between menus
}

# Advanced game settings
ADVANCED_SETTINGS = {
    "DIFFICULTY": "normal",             # easy, normal, hard, nightmare
    "PERMADEATH": False,                # If true, game over is permanent
    "FOG_OF_WAR": True,                 # If true, previously explored areas remain visible
    "MINIMAP_ENABLED": True,            # Enable/disable minimap
    "ENEMY_HEALTH_BARS": True,          # Show enemy health bars
    "AUTO_PICKUP_GOLD": True,           # Automatically pick up gold
    "SCREEN_SHAKE_INTENSITY": 0.5,      # Screen shake effect intensity (0.0-1.0)
    "COMBAT_TEXT_SIZE": 1.0,            # Size of combat text (0.5-1.5)
    "SHOW_HINTS": True                  # Show tutorial hints
} 