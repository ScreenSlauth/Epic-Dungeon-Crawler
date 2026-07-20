# Epic Dungeon Crawler

A roguelike dungeon crawler game built with Python and Pygame, featuring procedurally generated levels, dynamic enemy AI, progressive difficulty scaling, and comprehensive player progression systems.

## Demo

![Gameplay Demo](https://imgflip.com/gif/ax04cf)

## Features

- **Procedurally Generated Dungeons** – Experience unique layouts and connections on each playthrough
- **Multiple Biomes** – Explore distinct themed environments including Caverns, Forests, Icy Peaks, Lava Chambers, and Shadow Realms
- **Dynamic Enemy AI** – Engage with diverse enemy types, each with unique behaviors and strategies
- **Equipment System** – Discover and equip weapons, armor, and consumables to enhance your character
- **Character Progression** – Level up your character, gain experience, and unlock new abilities
- **Quest System** – Complete quests for rewards and story advancement
- **Comprehensive Statistics** – Monitor and manage health, mana, experience, damage, defense, and inventory
- **Dual UI System** – Leverages both direct stat rendering and advanced HUD for optimal reliability
- **Field of View Mechanics** – Immersive exploration with dynamic vision-based discovery

## Installation

### Requirements

- Python 3.7+
- Pygame 2.0.0+

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Not-Just-Pratul/Epic-Dungeon-Crawler.git
   cd Epic-Dungeon-Crawler
   ```

2. Install dependencies:
   ```bash
   pip install pygame
   ```

3. Launch the game:
   ```bash
   cd dungeon_crawler
   python main.py
   ```

## Controls

| Action | Input |
|--------|-------|
| Move Player | Arrow Keys / WASD |
| Use Item | Space |
| Pause / Menu | ESC |

## Game Mechanics

### Combat System

Combat operates on a turn-based framework where proximity to enemies triggers automatic attacks. Enemies retaliate if they survive the initial encounter. Damage calculations incorporate your attack power, weapon bonuses, and the opponent's defense rating.

### Player Statistics

Track your character's progression through the following metrics:

| Stat | Purpose |
|------|---------|
| Health | Current and maximum health points |
| Mana | Current and maximum mana reserves |
| Level & Experience | Current level and progress toward next rank |
| Attack Damage | Total offensive power including equipment bonuses |
| Defense | Damage reduction against enemy attacks |
| Inventory | Item count and equipped gear |
| Currency | Gold available for future transactions |

### Item Categories

- **Restorative Items** – Health potions for in-battle recovery
- **Weapons** – Equipment to increase attack damage
- **Armor** – Protective gear to enhance defense
- **Currency** – Gold for future transactions and upgrades

### Progression System

Defeat enemies to accumulate experience points. Upon reaching the experience threshold, your character levels up, increasing core statistics and unlocking new abilities.

### Quest Framework

Engage with NPCs or discover quest objectives to initiate quests. Successfully complete quest requirements to earn rewards and advance the narrative.

## Development

### Project Architecture

```
dungeon_crawler/
├── main.py                  # Application entry point and main game loop
├── settings.py              # Configuration and game constants
├── game/
│   ├── player.py           # Player entity and statistics management
│   ├── enemy.py            # Enemy entity implementations
│   ├── entity.py           # Base entity class
│   ├── item.py             # Item system and management
│   ├── quest_manager.py    # Quest tracking and progression
│   ├── sound_manager.py    # Audio playback and management
│   ├── pathfinding.py      # Navigation algorithms
│   ├── game_state.py       # Game state management
│   ├── tile.py             # Tile definitions and properties
│   ├── world/
│   │   └── dungeon.py      # Procedural dungeon generation with biome support
│   └── ui/
│       ├── hud.py          # Heads-up display implementation
│       └── menu.py         # Menu system
└── assets/                 # Game resources
    ├── images/             # Sprite sheets and textures
    ├── sounds/             # Sound effects
    └── music/              # Background music
```

### Technical Highlights

- **Dual Rendering System** – Combines direct stat rendering with an advanced HUD for maximum reliability
- **Procedural Generation** – Sophisticated dungeon generation algorithm supporting multiple biome types
- **Centralized State Management** – Unified player object with accessor methods for consistent data handling
- **AI System** – Diverse enemy behaviors implemented through polymorphic entity classes

### Roadmap

- [ ] Enhanced item system with rarity tiers and special effects
- [ ] Boss encounters and challenging combat scenarios
- [ ] Advanced visual effects and particle systems
- [ ] Save/Load game progression
- [ ] Town hub and safe zones
- [ ] Extended NPC interactions and trading mechanics

## Credits

- **Development & Design:** Pratul Sharma
- **Art Direction:** Placeholder assets (pending replacement)
- Sound Effects: Placeholder sounds (to be replaced)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
