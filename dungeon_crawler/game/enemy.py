import pygame
import random
import math
from .entity import Entity
from .settings import *
from .pathfinding import astar

class Enemy(Entity):
    """Enemy entity with AI movement and combat capabilities"""
    
    def __init__(self, x, y, enemy_type, level=1):
        super().__init__(x, y)
        self.enemy_type = enemy_type
        self.level = level
        
        # Get base stats from settings based on enemy type
        base_stats = ENEMY_STATS.get(enemy_type, ENEMY_STATS["goblin"])
        
        # Scale stats based on level
        level_multiplier = 1 + (level - 1) * 0.2
        self.max_health = int(base_stats["health"] * level_multiplier)
        self.health = self.max_health
        self.base_damage = int(base_stats["damage"] * level_multiplier)
        self.speed = base_stats["speed"]
        self.xp_reward = base_stats["xp_reward"]
        self.gold_reward = base_stats["gold_reward"]
        
        self.alive = True
        self.path = []
        self.aggro_range = 10
        self.move_cooldown = 0
        self.attack_cooldown = 0
        
        # Visual properties
        self.animation_frame = 0
        self.direction = "down"
        self.colors = self.get_enemy_colors()
        
    def get_enemy_colors(self):
        """Get color scheme based on enemy type"""
        color_schemes = {
            "goblin": {
                "primary": (0, 200, 0),
                "secondary": (0, 150, 0)
            },
            "skeleton": {
                "primary": (220, 220, 220),
                "secondary": (180, 180, 180)
            },
            "orc": {
                "primary": (0, 150, 0),
                "secondary": (0, 100, 0)
            },
            "lynx": {
                "primary": (200, 150, 50),
                "secondary": (150, 100, 30)
            },
            "frost_troll": {
                "primary": (150, 200, 255),
                "secondary": (100, 150, 220)
            },
            "magma_elemental": {
                "primary": (230, 80, 0),
                "secondary": (180, 30, 0)
            },
            "shadow_wraith": {
                "primary": (80, 0, 130),
                "secondary": (50, 0, 80)
            }
        }
        return color_schemes.get(self.enemy_type, color_schemes["goblin"])
        
    def update(self, player, dungeon):
        """Update enemy state and AI"""
        if not self.alive:
            return
            
        # Reduce cooldowns
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Check if player is in aggro range
        distance_to_player = self.euclidean_distance_to(player)
        
        if distance_to_player <= self.aggro_range:
            # Player is in range, try to pathfind
            if not self.path and self.move_cooldown <= 0:
                self.path = self.calculate_path_to_player(player, dungeon)
                
            # Try to move along path
            if self.path and self.move_cooldown <= 0:
                self.follow_path(dungeon)
                self.move_cooldown = max(1, int(20 * (1 - self.speed)))  # Faster enemies move more frequently
        else:
            # Random wandering
            if random.random() < 0.1 and self.move_cooldown <= 0:
                self.random_move(dungeon)
                self.move_cooldown = max(1, int(30 * (1 - self.speed)))
                
        # Update animation
        self.animation_frame = (self.animation_frame + 0.15) % 4
                
    def calculate_path_to_player(self, player, dungeon):
        """Calculate path to player using A* pathfinding"""
        # Convert positions to tuples for pathfinding
        start = (self.x, self.y)
        goal = (player.x, player.y)
        
        # If player is adjacent, no need for pathfinding
        if self.is_adjacent_to(player):
            return []
        
        # Create a walkable grid for pathfinding
        walkable = [[dungeon.grid[y][x].type == 1 for x in range(GRID_WIDTH)] 
                    for y in range(GRID_HEIGHT)]
                    
        # Make enemy positions unwalkable
        for enemy in dungeon.enemies:
            if enemy != self and enemy.alive and 0 <= enemy.y < GRID_HEIGHT and 0 <= enemy.x < GRID_WIDTH:
                walkable[enemy.y][enemy.x] = False
                
        # Find path
        path = astar(walkable, start, goal)
        
        # Remove the first node, which is the current position
        if path and len(path) > 1:
            return path[1:]
        return []
        
    def follow_path(self, dungeon):
        """Move along calculated path"""
        if not self.path:
            return False
            
        next_pos = self.path[0]
        
        # Check if next position is valid
        if self.is_valid_move(next_pos[0], next_pos[1], dungeon):
            self.x, self.y = next_pos
            self.path.pop(0)
            
            # Update direction based on movement
            dx = next_pos[0] - self.x
            dy = next_pos[1] - self.y
            
            if abs(dx) > abs(dy):
                self.direction = "right" if dx > 0 else "left"
            else:
                self.direction = "down" if dy > 0 else "up"
                
            return True
        else:
            # Path is now invalid, clear it
            self.path = []
            return False
            
    def random_move(self, dungeon):
        """Move in a random direction"""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            
            if self.is_valid_move(new_x, new_y, dungeon):
                self.x = new_x
                self.y = new_y
                
                # Update direction
                if dx > 0:
                    self.direction = "right"
                elif dx < 0:
                    self.direction = "left"
                elif dy > 0:
                    self.direction = "down"
                else:
                    self.direction = "up"
                    
                return True
                
        return False
        
    def is_valid_move(self, x, y, dungeon):
        """Check if a move is valid"""
        # Check boundaries
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            return False
            
        # Check if tile is walkable
        if dungeon.grid[y][x].type != 1:  # FLOOR
            return False
            
        # Check for other enemies
        for enemy in dungeon.enemies:
            if enemy != self and enemy.alive and enemy.x == x and enemy.y == y:
                return False
                
        return True
        
    def attack(self, target):
        """Attack a target"""
        if self.attack_cooldown > 0:
            return 0
            
        damage = random.randint(self.base_damage - 5, self.base_damage + 5)
        self.attack_cooldown = 10
        return damage
        
    def take_damage(self, amount):
        """Take damage and return True if enemy died"""
        self.health -= amount
        
        if self.health <= 0:
            self.alive = False
            return True
        return False
        
    def draw(self, screen, camera_offset=(0, 0)):
        """Draw the enemy on the screen"""
        if not self.alive:
            return
            
        # Calculate screen position
        screen_x = self.x * TILE_SIZE - camera_offset[0]
        screen_y = self.y * TILE_SIZE - camera_offset[1]
        
        # Return if outside visible area
        if (screen_x < -TILE_SIZE or screen_x > SCREEN_WIDTH or 
            screen_y < -TILE_SIZE or screen_y > SCREEN_HEIGHT):
            return
            
        # Draw enemy body
        color = self.colors["primary"]
        pygame.draw.rect(screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        
        # Draw enemy detail
        detail_color = self.colors["secondary"]
        
        # Draw different patterns based on enemy type
        if self.enemy_type == "goblin":
            # Draw small ears
            pygame.draw.rect(screen, detail_color, 
                            (screen_x + 2, screen_y, TILE_SIZE//4, TILE_SIZE//4))
            pygame.draw.rect(screen, detail_color, 
                            (screen_x + TILE_SIZE - TILE_SIZE//4 - 2, screen_y, TILE_SIZE//4, TILE_SIZE//4))
        elif self.enemy_type == "skeleton":
            # Draw skull pattern
            pygame.draw.rect(screen, detail_color, 
                            (screen_x + TILE_SIZE//4, screen_y + TILE_SIZE//4, 
                             TILE_SIZE//2, TILE_SIZE//2))
        elif self.enemy_type == "frost_troll":
            # Draw icy spikes
            pygame.draw.polygon(screen, detail_color, 
                              [(screen_x + TILE_SIZE//2, screen_y),
                               (screen_x + TILE_SIZE//4, screen_y + TILE_SIZE//4),
                               (screen_x + 3*TILE_SIZE//4, screen_y + TILE_SIZE//4)])
        elif self.enemy_type == "magma_elemental":
            # Draw flame pattern
            pygame.draw.polygon(screen, detail_color, 
                              [(screen_x + TILE_SIZE//2, screen_y + TILE_SIZE),
                               (screen_x + TILE_SIZE//4, screen_y + 3*TILE_SIZE//4),
                               (screen_x + 3*TILE_SIZE//4, screen_y + 3*TILE_SIZE//4)])
        
        # Draw health bar
        bar_width = TILE_SIZE
        bar_height = 4
        pygame.draw.rect(screen, (100, 0, 0), 
                        (screen_x, screen_y - bar_height - 1, bar_width, bar_height))
        health_width = max(0, (self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, (0, 200, 0), 
                        (screen_x, screen_y - bar_height - 1, health_width, bar_height))
                        
    def get_loot(self):
        """Generate loot when enemy dies"""
        loot = {
            "gold": self.gold_reward,
            "items": []
        }
        
        # Chance to drop health potion
        if random.random() < 0.3:
            loot["items"].append(("HEALTH_POTION", 20 + self.level * 5))
            
        # Chance to drop equipment based on enemy type and level
        if random.random() < 0.05 * self.level:
            if self.enemy_type in ["skeleton", "orc", "frost_troll"]:
                loot["items"].append(("WEAPON", 5 + self.level * 2))
            elif self.enemy_type in ["goblin", "lynx", "magma_elemental", "shadow_wraith"]:
                loot["items"].append(("ARMOR", 3 + self.level))
                
        return loot 