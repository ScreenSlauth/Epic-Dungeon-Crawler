import pygame
import math
from .settings import *

class Entity:
    """Base class for all game entities (player, enemies, items)"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = id(self)  # Unique identifier
        
    def distance_to(self, other):
        """Calculate Manhattan distance to another entity"""
        return abs(self.x - other.x) + abs(self.y - other.y)
        
    def euclidean_distance_to(self, other):
        """Calculate Euclidean distance to another entity"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        
    def is_adjacent_to(self, other):
        """Check if entity is adjacent to another entity"""
        return self.distance_to(other) <= 1
        
    def get_position(self):
        """Get current grid position"""
        return (self.x, self.y)
        
    def set_position(self, x, y):
        """Set position"""
        self.x = x
        self.y = y
        
    def draw(self, screen, camera_offset=(0, 0)):
        """Draw the entity (to be overridden by subclasses)"""
        # Default rendering as a simple rectangle
        screen_x = self.x * TILE_SIZE - camera_offset[0]
        screen_y = self.y * TILE_SIZE - camera_offset[1]
        
        # Return if outside visible area
        if (screen_x < -TILE_SIZE or screen_x > SCREEN_WIDTH or 
            screen_y < -TILE_SIZE or screen_y > SCREEN_HEIGHT):
            return
            
        pygame.draw.rect(screen, COLOR_WHITE, (screen_x, screen_y, TILE_SIZE, TILE_SIZE)) 