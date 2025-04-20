import pygame
import random
import math
from .settings import *
from .entity import Entity

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = HEALTH_BASE
        self.max_health = HEALTH_BASE
        self.score = 0
        self.base_damage = DAMAGE_BASE
        self.defense = 0
        self.level = 1
        self.xp = 0
        self.xp_to_level_up = XP_BASE_REQUIREMENT
        self.gold = 10
        self.mana = 100
        self.max_mana = 100
        self.inventory = []
        self.equipment = {
            "weapon": None,
            "armor": None,
            "amulet": None,
            "ring": None
        }
        self.buffs = []
        self.skills = []
        self.direction = "down"  # For animation
        self.animation_frame = 0
        self.moving = False
        self.attack_cooldown = 0
        self.footstep_cooldown = 0
        
        # Initialize animations
        self.animations = {}
        self.load_animations()
        
    def load_animations(self):
        """Load player animation frames"""
        # This would normally load actual sprite images
        # For now we'll use placeholder colors for different animations
        self.animation_colors = {
            "idle_down": COLOR_BLUE,
            "idle_up": (0, 0, 200),
            "idle_left": (0, 0, 220),
            "idle_right": (0, 0, 180),
            "walk_down": (50, 50, 255),
            "walk_up": (50, 50, 200),
            "walk_left": (50, 50, 220),
            "walk_right": (50, 50, 180),
            "attack": (100, 100, 255)
        }
        
    def move(self, dx, dy, dungeon):
        """Move player by the given offset if the destination is valid"""
        try:
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Validate that new position is within map boundaries
            if new_x < 0 or new_x >= dungeon.width or new_y < 0 or new_y >= dungeon.height:
                return False
            
            # Check if the destination is valid for movement
            if dungeon.is_position_valid(new_x, new_y):
                # Check if there's an enemy at the destination
                for enemy in dungeon.enemies:
                    if enemy.x == new_x and enemy.y == new_y:
                        # Don't move into enemies, attack them instead
                        return False
                
                # Move player
                self.x = new_x
                self.y = new_y
                
                # Check for stairs down
                if dungeon.stairs_down and (self.x, self.y) == dungeon.stairs_down:
                    # Return a special value to indicate stairs were reached
                    return "next_floor"
                
                return True
            
            return False
        except Exception as e:
            print(f"Error during player movement: {e}")
            return False
        
    def get_attack_damage(self):
        """Calculate the player's total attack damage including equipment and buffs"""
        # Base damage + weapon damage + buff effects
        total_damage = self.base_damage
        
        # Add equipment bonuses
        if self.equipment["weapon"]:
            total_damage += self.equipment["weapon"].effect_value
            
        # Add buffs
        for buff in self.buffs:
            if buff["type"] == "damage":
                total_damage += buff["value"]
                
        # Add critical hit chance
        if random.random() < 0.1:  # 10% critical hit chance
            total_damage = int(total_damage * 1.5)
            
        return total_damage
        
    def update(self):
        """Update player state each turn"""
        # Reduce cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        if self.footstep_cooldown > 0:
            self.footstep_cooldown -= 1
            
        # Update buffs
        self.update_buffs()
        
        # Reset movement flag for animation
        self.moving = False
        
    def update_buffs(self):
        """Update active buffs and remove expired ones"""
        active_buffs = []
        for buff in self.buffs:
            buff["duration"] -= 1
            if buff["duration"] > 0:
                active_buffs.append(buff)
        self.buffs = active_buffs
        
    def regen_mana(self, amount):
        """Regenerate mana"""
        self.mana = min(self.max_mana, self.mana + amount)
        
    def pickup_item(self, item):
        """Add an item to the player's inventory or apply its effects"""
        if item.item_type == "HEALTH_POTION":
            self.health = min(self.max_health, self.health + item.effect_value)
        elif item.item_type == "GOLD":
            self.gold += item.effect_value
        else:
            # Add to inventory
            self.inventory.append(item)
            
        # Increase score
        self.add_score(20)
        
    def use_item(self, item_index=None):
        """Use an item from the inventory"""
        if not self.inventory:
            return False
            
        if item_index is None:
            # Use the first item if no index specified
            item = self.inventory[0]
            item_index = 0
        elif item_index < len(self.inventory):
            item = self.inventory[item_index]
        else:
            return False
            
        # Apply item effects
        if item.item_type == "HEALTH_POTION":
            self.health = min(self.max_health, self.health + item.effect_value)
            
        elif item.item_type == "WEAPON":
            # Equip the weapon, replacing any existing one
            old_weapon = self.equipment["weapon"]
            self.equipment["weapon"] = item
            if old_weapon:
                self.inventory.append(old_weapon)
                
        elif item.item_type == "ARMOR":
            # Equip the armor, replacing any existing one
            old_armor = self.equipment["armor"]
            self.equipment["armor"] = item
            if old_armor:
                self.inventory.append(old_armor)
        
        # Remove the used item from inventory
        self.inventory.pop(item_index)
        return True
        
    def add_xp(self, amount):
        """Add XP and level up if necessary"""
        self.xp += amount
        if self.xp >= self.xp_to_level_up:
            self.level_up()
            
    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.max_health += HEALTH_LEVEL_INCREASE
        self.health = self.max_health
        self.base_damage += DAMAGE_LEVEL_INCREASE
        self.max_mana += 10
        self.mana = self.max_mana
        
        # XP for next level
        self.xp -= self.xp_to_level_up
        self.xp_to_level_up = int(self.xp_to_level_up * XP_LEVEL_MULTIPLIER)
        
        # Unlock new skills at specific levels
        if self.level == 3:
            self.skills.append("cleave")
        elif self.level == 5:
            self.skills.append("fireball")
        elif self.level == 7:
            self.skills.append("heal")
        elif self.level == 10:
            self.skills.append("lightning")
            
        return self.level
        
    def add_score(self, amount):
        """Add to the player's score"""
        self.score += amount
        
    def get_status(self):
        """Get player's current status for UI display"""
        # Debug message to check if this method is being called
        print("Player.get_status() called - providing stats to HUD")
        
        # Return all player stats needed by the HUD with safe defaults
        return {
            "health": getattr(self, 'health', 100),
            "max_health": getattr(self, 'max_health', 100),
            "mana": getattr(self, 'mana', 100),
            "max_mana": getattr(self, 'max_mana', 100),
            "level": getattr(self, 'level', 1),
            "xp": getattr(self, 'xp', 0),
            "xp_to_level_up": getattr(self, 'xp_to_level_up', 100),
            "score": getattr(self, 'score', 0),
            "gold": getattr(self, 'gold', 0),
            "damage": self.get_attack_damage() if hasattr(self, 'get_attack_damage') else 10,
            "defense": getattr(self, 'defense', 0),
            "inventory_count": len(getattr(self, 'inventory', [])),
            "buffs": getattr(self, 'buffs', []),
            "skills": getattr(self, 'skills', [])
        }
        
    def draw(self, screen, camera_offset=(0, 0)):
        """Draw the player on the screen"""
        # Determine animation state
        anim_state = "walk_" if self.moving else "idle_"
        anim_state += self.direction
        
        # Get appropriate color from animation dictionary
        color = self.animation_colors.get(anim_state, COLOR_BLUE)
        
        # Calculate screen position
        screen_x = self.x * TILE_SIZE - camera_offset[0]
        screen_y = self.y * TILE_SIZE - camera_offset[1]
        
        # Draw player
        pygame.draw.rect(screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        
        # Draw equipment overlay if equipped
        if self.equipment["weapon"]:
            # Draw weapon indicator (in a real game, this would be part of the sprite)
            pygame.draw.line(screen, COLOR_ORANGE, 
                            (screen_x + TILE_SIZE//4, screen_y + TILE_SIZE//4),
                            (screen_x + TILE_SIZE*3//4, screen_y + TILE_SIZE*3//4), 3)
            
        if self.equipment["armor"]:
            # Draw armor indicator
            pygame.draw.circle(screen, COLOR_GRAY, 
                              (screen_x + TILE_SIZE//2, screen_y + TILE_SIZE//2),
                              TILE_SIZE//4, 2) 