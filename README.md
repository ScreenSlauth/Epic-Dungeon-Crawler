# Epic Dungeon Crawler

A roguelike dungeon crawler game built with Pygame, featuring procedurally generated levels, multiple enemy types, progressive difficulty, and a robust player stats system.

[![Watch the video](https://img.youtube.com/vi/lOQLVXWYbmk/0.jpg)](https://youtu.be/gSwePsjVqFs?autoplay=1)

## Features

- **Procedurally generated dungeons** - Every playthrough is unique with random room layouts and connections
- **Multiple biomes** - Explore different themed areas (Cavern, Forest, Ice, Lava, Shadow)
- **Diverse enemies** - Face different enemy types with unique behaviors and AI
- **Items and equipment** - Find and use weapons, armor, and potions
- **Level progression** - Gain experience, level up, and unlock new abilities
- **Quest system** - Complete quests for rewards and story progression
- **Comprehensive player stats** - Monitor health, mana, XP, damage, defense, and more
- **Dual UI system** - Brute force direct stat rendering alongside an advanced HUD system
- **Dynamic lighting** - Field of view system for immersive exploration

## Installation

### Requirements
- Python 3.7 or higher
- Pygame 2.0.0 or higher

### Steps

1. Clone or download this repository
2. Install required packages:
```
pip install pygame
```
3. Run the game:
```
cd dungeon_crawler
python main.py
```

## Controls

- **Arrow Keys / WASD**: Move the player
- **Space**: Use item
- **ESC**: Pause game / Open menu

## Game Mechanics

### Combat
Combat is turn-based - when you move next to an enemy, you automatically attack. The enemy will counter-attack if it survives. Damage is calculated based on your attack power, weapon bonuses, and the enemy's defense.

### Stats System
The game features a comprehensive stats display showing:
- **Health**: Current and maximum health points
- **Mana**: Current and maximum mana points 
- **Level & XP**: Current level and progress to the next level
- **Attack Damage**: Calculated from base damage and equipment bonuses
- **Defense**: Protection against enemy attacks
- **Items**: Inventory count and equipped items
- **Gold**: Currency for future shops

### Items
- **Health Potions**: Restore health
- **Weapons**: Increase attack damage
- **Armor**: Increase defense
- **Gold**: Currency for future shops/upgrades

### Leveling
Defeat enemies to gain experience points. When you reach enough XP, you'll level up, increasing your stats and potentially unlocking new abilities.

### Quests
Speak to NPCs or find quest items to receive quests. Complete objectives to earn rewards and advance the story.

## Development

### Project Structure
- **main.py**: Game entry point with the main game loop and rendering
- **game/**: Main game modules
  - **player.py**: Player character logic and stats management
  - **world/dungeon.py**: Dungeon generation with biome system
  - **entity.py**: Base class for all game entities
  - **ui/**: User interface components including HUD and menus
  - **sound_manager.py**: Audio handling for music and sound effects
  - **settings.py**: Game constants and configuration
- **assets/**: Game assets (images, sounds, music)

### Technical Notes
- The player stats are displayed through a direct rendering system as a fallback method
- The game implements both a traditional HUD and a brute-force stats display for reliability
- Player data is managed through a centralized player object with accessor methods

### Future Plans
- Expanded item system with rarities and special effects
- More enemy types and boss battles
- Enhanced visual effects
- Saving/loading game progress
- Town/hub area between dungeon runs
- Trading and NPC interaction

## Credits

- Game Design & Programming: Pratul Sharma
- Art Assets: Placeholder graphics (to be replaced)
- Sound Effects: Placeholder sounds (to be replaced)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
