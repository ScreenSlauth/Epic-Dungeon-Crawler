import pygame
from enum import Enum

class TileType(Enum):
    """Enumeration of tile types"""
    WALL = 0
    FLOOR = 1
    WATER = 2
    LAVA = 3
    DOOR = 4
    STAIRS_DOWN = 5
    STAIRS_UP = 6
    
class Tile:
    """Representation of a dungeon tile"""
    
    def __init__(self, type=TileType.WALL, variant=0):
        self.type = type.value if isinstance(type, TileType) else type
        self.variant = variant  # For visual variety
        self.explored = False   # If player has seen this tile
        self.visible = False    # If currently visible to player
        self.entity = None      # Entity on this tile
        
    def is_walkable(self):
        """Check if this tile can be walked on"""
        return self.type in [TileType.FLOOR.value, TileType.DOOR.value, 
                           TileType.STAIRS_DOWN.value, TileType.STAIRS_UP.value]
        
    def is_transparent(self):
        """Check if this tile blocks line of sight"""
        return self.type != TileType.WALL.value
        
    def get_color(self, biome):
        """Get the color for rendering based on tile type and biome"""
        from .settings import BIOME_COLORS
        
        # Convert biome string to dictionary key
        biome_key = biome.name if hasattr(biome, 'name') else biome
        
        # Default color if biome not found
        default_colors = {
            TileType.WALL.value: (50, 50, 50),
            TileType.FLOOR.value: (30, 30, 30),
            TileType.WATER.value: (0, 0, 100),
            TileType.LAVA.value: (150, 30, 0),
            TileType.DOOR.value: (120, 80, 40),
            TileType.STAIRS_DOWN.value: (70, 70, 70),
            TileType.STAIRS_UP.value: (100, 100, 100)
        }
        
        # Get biome colors from settings
        biome_colors = BIOME_COLORS.get(biome_key, {})
        
        if self.type == TileType.WALL.value:
            return biome_colors.get("WALL", default_colors[self.type])
        elif self.type == TileType.FLOOR.value:
            return biome_colors.get("FLOOR", default_colors[self.type])
        else:
            return default_colors.get(self.type, (200, 200, 200))
            
    def draw(self, screen, x, y, tile_size, biome, explored_only=True):
        """Draw the tile at the specified screen position"""
        # Skip rendering if not explored and we're only showing explored tiles
        if explored_only and not self.explored:
            return
            
        # Get base color based on tile type and biome
        color = self.get_color(biome)
        
        # Darken if explored but not visible
        if self.explored and not self.visible:
            color = tuple(max(0, c // 2) for c in color)
            
        # Draw the tile
        pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
        
        # Draw special tile features
        if self.type == TileType.DOOR.value:
            # Draw door frame
            door_color = (150, 100, 50) if self.visible else (75, 50, 25)
            pygame.draw.rect(screen, door_color, 
                            (x + tile_size//4, y + tile_size//4, 
                             tile_size//2, tile_size//2))
                             
        elif self.type == TileType.STAIRS_DOWN.value:
            # Draw stairs down symbol
            stairs_color = (200, 200, 200) if self.visible else (100, 100, 100)
            pygame.draw.polygon(screen, stairs_color, 
                              [(x + tile_size//4, y + tile_size//4), 
                               (x + 3*tile_size//4, y + tile_size//4),
                               (x + 3*tile_size//4, y + 3*tile_size//4)])
                               
        elif self.type == TileType.STAIRS_UP.value:
            # Draw stairs up symbol
            stairs_color = (200, 200, 200) if self.visible else (100, 100, 100)
            pygame.draw.polygon(screen, stairs_color, 
                              [(x + tile_size//4, y + 3*tile_size//4), 
                               (x + 3*tile_size//4, y + 3*tile_size//4),
                               (x + tile_size//2, y + tile_size//4)])
                               
        # Add tile variants/details for visual variety
        if self.type == TileType.FLOOR.value and self.variant > 0:
            detail_size = max(1, tile_size // 8)
            detail_color = tuple(max(0, c - 30) for c in color)
            
            if self.variant == 1:  # Small crack
                pygame.draw.line(screen, detail_color, 
                                (x + tile_size//3, y + tile_size//3),
                                (x + 2*tile_size//3, y + 2*tile_size//3), 1)
            elif self.variant == 2:  # Small dots
                pygame.draw.circle(screen, detail_color,
                                  (x + tile_size//3, y + tile_size//3), detail_size)
                pygame.draw.circle(screen, detail_color,
                                  (x + 2*tile_size//3, y + 2*tile_size//3), detail_size) 