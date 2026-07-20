# Epic Dungeon Crawler

Epic Dungeon Crawler is a polished roguelike built with Python and Pygame. Explore procedurally generated dungeons, battle varied foes, and progress through equipment, leveling, and quest systems.

## Demo

<div style="width:100%; max-width:100%;">
  <a href="https://imgflip.com/gif/ax04cf">
    <img src="https://i.imgflip.com/ax04cf.gif" alt="Gameplay Demo" style="width:100%; height:auto; display:block;" />
  </a>
</div>

## Features

- **Procedural Dungeon Generation** – Every run creates a unique layout with randomized rooms and pathways
- **Distinct Biomes** – Traverse Caverns, Forests, Ice Vaults, Lava Chambers, and Shadow Realms
- **Diverse Enemy Types** – Fight enemies with different movement and combat behaviors
- **Equipment & Items** – Acquire weapons, armor, potions, and consumables to strengthen your hero
- **Experience & Leveling** – Gain experience, increase stats, and improve your capabilities
- **Quest System** – Complete goals for rewards and story progression
- **Comprehensive HUD** – Monitor health, mana, XP, attack, defense, inventory, and gold in real time
- **Reliable UI** – Uses dual rendering for HUD and fallback direct stat display
- **Field of View** – Explore the dungeon with vision-based reveal mechanics

## Installation

### Requirements

- Python 3.7 or newer
- Pygame 2.0.0 or newer

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Not-Just-Pratul/Epic-Dungeon-Crawler.git
   cd Epic-Dungeon-Crawler
   ```

2. Install dependencies:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   cd dungeon_crawler
   python main.py
   ```

## Controls

| Action | Input |
|--------|-------|
| Move | Arrow Keys / WASD |
| Use Item | Space |
| Pause / Menu | ESC |

## Gameplay Overview

### Combat

Combat is triggered when the player moves adjacent to an enemy. Attacks resolve automatically, and surviving enemies counterattack based on their stats.

### Progression

Defeat enemies to earn experience. Leveling up increases core stats and improves your ability to survive deeper dungeon runs.

### Items

- **Health Potions** – Restore health during gameplay
- **Weapons** – Increase attack power
- **Armor** – Reduce damage taken
- **Gold** – Collect currency for future upgrades

### Quests

Discover quests through NPC encounters or objective items. Completing quests rewards the player and advances the game narrative.

## Project Structure

```
dungeon_crawler/
├── main.py                  # Game entry point and main loop
├── settings.py              # Game configuration and constants
├── game/
│   ├── player.py            # Player character and stats management
│   ├── enemy.py             # Enemy behavior and combat logic
│   ├── entity.py            # Base entity definitions
│   ├── item.py              # Item systems and inventory handling
│   ├── quest_manager.py     # Quest progression and tracking
│   ├── sound_manager.py     # Audio playback and effects handling
│   ├── pathfinding.py       # Navigation and AI movement logic
│   ├── game_state.py        # Game state flow and management
│   ├── tile.py              # Tile definitions and map logic
│   ├── world/
│   │   └── dungeon.py       # Procedural world generation
│   └── ui/
│       ├── hud.py           # Heads-up display rendering
│       └── menu.py          # Menu screens and user input
└── assets/
    ├── images/              # Sprites and visual assets
    ├── sounds/              # Sound effects
    └── music/               # Background audio
```

## Technical Highlights

- **Reliable HUD** – Structured UI rendering with fallback stat display
- **Procedural Generation** – Multi-biome dungeon generation for replay value
- **Centralized State** – Unified player and game state management
- **Modular AI** – Flexible enemy behavior implemented through entity classes

## Roadmap

- [ ] Add item rarity tiers and special equipment effects
- [ ] Introduce boss encounters and elite enemies
- [ ] Enhance visuals with particle effects and lighting
- [ ] Add save/load support
- [ ] Implement a hub area and safe zones
- [ ] Expand NPC interactions and trading

## Credits

- **Development & Design:** Pratul Sharma
- **Assets:** Placeholder art and audio
