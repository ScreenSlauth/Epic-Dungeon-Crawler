import pygame
import random
import math
from .entity import Entity
from .settings import *

class Item(Entity):
    """Game item that can be picked up and used by the player"""
    
    def __init__(self, x, y, item_type, effect_value=None, icon=None, rarity="common"):
        super().__init__(x, y)
        self.item_type = item_type
        self.effect_value = effect_value
        self.icon = icon
        self.rarity = rarity
        self.animation_frame = 0
        self.hover_offset = 0
        self.hover_direction = 1
        
        # Initialize properties dictionary
        self.properties = {}
        
        # Set description based on item type and effect
        self.description = self.generate_description()
        
        # Set visual properties
        self.color = self.get_item_color()
        
    def get_item_color(self):
        """Get the color for rendering the item based on type and rarity"""
        base_colors = {
            "HEALTH_POTION": COLOR_GREEN,
            "MANA_POTION": (50, 50, 255),
            "WEAPON": COLOR_ORANGE,
            "ARMOR": COLOR_GRAY,
            "GOLD": COLOR_YELLOW,
            "QUEST_ITEM": COLOR_PURPLE,
            "SCROLL": (200, 180, 50),
            "KEY": (150, 150, 0)
        }
        
        rarity_modifiers = {
            "common": 0.8,
            "uncommon": 1.0,
            "rare": 1.2,
            "epic": 1.4,
            "legendary": 1.6
        }
        
        base_color = base_colors.get(self.item_type, COLOR_WHITE)
        modifier = rarity_modifiers.get(self.rarity, 1.0)
        
        # Adjust color based on rarity (make it brighter/more saturated)
        r = min(255, int(base_color[0] * modifier))
        g = min(255, int(base_color[1] * modifier))
        b = min(255, int(base_color[2] * modifier))
        
        return (r, g, b)
        
    def generate_description(self):
        """Generate a description for the item based on its type and effect"""
        if self.item_type == "HEALTH_POTION":
            return f"Restores {self.effect_value} health points"
            
        elif self.item_type == "MANA_POTION":
            return f"Restores {self.effect_value} mana points"
            
        elif self.item_type == "WEAPON":
            weapon_names = {
                "common": "Rusty Dagger",
                "uncommon": "Iron Sword",
                "rare": "Steel Greatsword",
                "epic": "Enchanted Blade",
                "legendary": "Dragonslayer"
            }
            name = weapon_names.get(self.rarity, "Sword")
            return f"{name}: Increases damage by {self.effect_value}"
            
        elif self.item_type == "ARMOR":
            armor_names = {
                "common": "Leather Scraps",
                "uncommon": "Chainmail",
                "rare": "Steel Plate",
                "epic": "Enchanted Armor",
                "legendary": "Dragonscale"
            }
            name = armor_names.get(self.rarity, "Armor")
            return f"{name}: Increases defense by {self.effect_value}"
            
        elif self.item_type == "GOLD":
            return f"{self.effect_value} gold coins"
            
        elif self.item_type == "QUEST_ITEM":
            return f"A special item needed for a quest: {self.icon}"
            
        elif self.item_type == "SCROLL":
            return f"A magical scroll with unknown powers"
            
        elif self.item_type == "KEY":
            return f"A key that unlocks something"
            
        return "Unknown item"
        
    def update(self):
        """Update item animation"""
        self.animation_frame = (self.animation_frame + 0.1) % 4
        
        # Floating animation
        self.hover_offset += 0.2 * self.hover_direction
        if abs(self.hover_offset) > 3:
            self.hover_direction *= -1
            
    def draw(self, screen, camera_offset=(0, 0)):
        """Draw the item on the screen"""
        # Calculate screen position
        screen_x = self.x * TILE_SIZE - camera_offset[0]
        screen_y = self.y * TILE_SIZE - camera_offset[1] + self.hover_offset
        
        # Return if outside visible area
        if (screen_x < -TILE_SIZE or screen_x > SCREEN_WIDTH or 
            screen_y < -TILE_SIZE or screen_y > SCREEN_HEIGHT):
            return
            
        # Draw item based on type
        if self.item_type == "HEALTH_POTION":
            # Draw potion bottle
            pygame.draw.rect(screen, self.color, 
                            (screen_x + TILE_SIZE//4, screen_y + TILE_SIZE//4, 
                             TILE_SIZE//2, TILE_SIZE//2))
            # Draw bottle neck
            pygame.draw.rect(screen, (100, 100, 100), 
                            (screen_x + 3*TILE_SIZE//8, screen_y + TILE_SIZE//8, 
                             TILE_SIZE//4, TILE_SIZE//8))
            
        elif self.item_type == "WEAPON":
            # Draw sword
            pygame.draw.line(screen, self.color, 
                            (screen_x + TILE_SIZE//4, screen_y + TILE_SIZE//4),
                            (screen_x + 3*TILE_SIZE//4, screen_y + 3*TILE_SIZE//4), 3)
            # Draw handle
            pygame.draw.line(screen, (100, 80, 0), 
                            (screen_x + TILE_SIZE//5, screen_y + TILE_SIZE//5),
                            (screen_x + TILE_SIZE//3, screen_y + TILE_SIZE//3), 3)
            
        elif self.item_type == "ARMOR":
            # Draw armor shape
            pygame.draw.rect(screen, self.color, 
                            (screen_x + TILE_SIZE//4, screen_y + TILE_SIZE//4, 
                             TILE_SIZE//2, TILE_SIZE//2))
            # Draw details
            pygame.draw.line(screen, (50, 50, 50), 
                            (screen_x + TILE_SIZE//4, screen_y + TILE_SIZE//2),
                            (screen_x + 3*TILE_SIZE//4, screen_y + TILE_SIZE//2), 2)
            
        elif self.item_type == "GOLD":
            # Draw gold coin
            pygame.draw.circle(screen, self.color, 
                              (screen_x + TILE_SIZE//2, screen_y + TILE_SIZE//2), 
                              TILE_SIZE//3)
            # Draw coin details
            pygame.draw.circle(screen, (150, 120, 0), 
                              (screen_x + TILE_SIZE//2, screen_y + TILE_SIZE//2), 
                              TILE_SIZE//4, 1)
            
        elif self.item_type == "QUEST_ITEM":
            # Draw quest item as a special star shape
            points = []
            for i in range(5):
                angle = math.pi/2 + i * 2*math.pi/5
                x = screen_x + TILE_SIZE//2 + int(TILE_SIZE//3 * math.cos(angle))
                y = screen_y + TILE_SIZE//2 + int(TILE_SIZE//3 * math.sin(angle))
                points.append((x, y))
                
                angle += math.pi/5
                x = screen_x + TILE_SIZE//2 + int(TILE_SIZE//6 * math.cos(angle))
                y = screen_y + TILE_SIZE//2 + int(TILE_SIZE//6 * math.sin(angle))
                points.append((x, y))
                
            pygame.draw.polygon(screen, self.color, points)
            
        else:
            # Default item display
            item_size = int(TILE_SIZE * 0.7)
            pygame.draw.rect(screen, self.color, 
                            (screen_x + (TILE_SIZE - item_size)//2, 
                             screen_y + (TILE_SIZE - item_size)//2, 
                             item_size, item_size))
                             
        # Draw a glowing effect for rare+ items
        if self.rarity in ["rare", "epic", "legendary"]:
            glow_alpha = int(127 + 64 * math.sin(self.animation_frame * math.pi/2))
            glow_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            
            # Different glow colors based on rarity
            if self.rarity == "rare":
                glow_color = (0, 0, 255, glow_alpha)
            elif self.rarity == "epic":
                glow_color = (128, 0, 128, glow_alpha)
            else:  # legendary
                glow_color = (255, 165, 0, glow_alpha)
                
            pygame.draw.circle(glow_surface, glow_color, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2)
            screen.blit(glow_surface, (screen_x, screen_y))
            
    @classmethod
    def create_random_item(cls, x, y, level=1, force_type=None, biome_name="CAVERN"):
        """Create a random item appropriate for the given level"""
        item_pool = []
        
        # Filter items by level
        for item_name, item_data in ITEM_EFFECTS.items():
            # Skip if item requires higher level
            min_level = item_data.get("min_level", 1)
            if min_level > level:
                continue
                
            item_type = get_item_type(item_name)
            if force_type and item_type != force_type:
                continue
                
            # Get item rarity and base spawn rate
            rarity = item_data.get("rarity", "common")
            spawn_rate = item_data.get("spawn_rate", 0.3)
            
            # Apply level-based multiplier
            level_multiplier = cls.get_level_drop_rate_multiplier(level, rarity)
            
            # Apply biome-based multiplier
            biome_multiplier = cls.get_biome_drop_rate_multiplier(biome_name, rarity)
            
            # Special biome items get a higher chance
            biome_special_bonus = 1.0
            if biome_name in BIOME_ITEM_DROP_RATES:
                if item_name in BIOME_ITEM_DROP_RATES[biome_name].get("special_items", []):
                    biome_special_bonus = 2.0
                    
            # Calculate final weight
            weight = spawn_rate * level_multiplier * biome_multiplier * biome_special_bonus
            
            # Add to item pool
            item_pool.append((item_name, weight))
        
        # If no items match the criteria, return a default item
        if not item_pool:
            if force_type == "HEALTH_POTION":
                return cls(x, y, "HEALTH_POTION", 50, "health_potion_small", "common")
            elif force_type == "WEAPON":
                return cls(x, y, "WEAPON", 5, "wooden_stick", "common")
            elif force_type == "ARMOR":
                return cls(x, y, "ARMOR", 5, "leather_armor", "common")
            elif force_type == "GOLD":
                return cls(x, y, "GOLD", 20, "gold_small", "common")
            else:
                return cls(x, y, "HEALTH_POTION", 50, "health_potion_small", "common")
                
        # Select an item based on weights
        weights = [weight for _, weight in item_pool]
        item_names = [name for name, _ in item_pool]
        
        try:
            selected_item = random.choices(item_names, weights=weights, k=1)[0]
            item_data = ITEM_EFFECTS[selected_item]
            
            # Determine item type and effect value based on the selected item
            item_type = get_item_type(selected_item)
            
            # For potions, primarily use the health/mana value
            if "health" in item_data:
                effect_value = item_data["health"]
            elif "mana" in item_data:
                effect_value = item_data["mana"]
            elif "damage" in item_data:
                effect_value = item_data["damage"]
            elif "defense" in item_data:
                effect_value = item_data["defense"]
            elif "gold" in item_data:
                effect_value = item_data["gold"]
            else:
                effect_value = 0
                
            # Create item with appropriate properties
            item = cls(x, y, item_type, effect_value, selected_item, item_data.get("rarity", "common"))
            
            # Add additional properties
            for key, value in item_data.items():
                if key not in ["description", "rarity", "spawn_rate", "min_level"]:
                    item.properties[key] = value
                    
            return item
            
        except (IndexError, ValueError) as e:
            print(f"Error creating random item: {e}")
            # Fallback to a basic health potion
            return cls(x, y, "HEALTH_POTION", 50, "health_potion_small", "common")
    
    @staticmethod
    def get_level_drop_rate_multiplier(level, rarity):
        """Get the drop rate multiplier based on current level"""
        for level_range, multipliers in LEVEL_DROP_RATES.items():
            min_level, max_level = level_range
            if min_level <= level <= max_level:
                return multipliers.get(rarity, 1.0)
        return 1.0
        
    @staticmethod
    def get_biome_drop_rate_multiplier(biome_name, rarity):
        """Get the drop rate multiplier based on biome"""
        if biome_name in BIOME_ITEM_DROP_RATES:
            biome_data = BIOME_ITEM_DROP_RATES[biome_name]
            multiplier_key = f"{rarity}_multiplier"
            return biome_data.get(multiplier_key, 1.0)
        return 1.0

def get_item_type(item_name):
    """Determine item type based on name"""
    if "sword" in item_name or "axe" in item_name or "wand" in item_name or "blade" in item_name or "stick" in item_name or "dagger" in item_name:
        return "WEAPON"
    elif "armor" in item_name or "shield" in item_name or "plate" in item_name or "mail" in item_name:
        return "ARMOR"
    elif "potion" in item_name and "health" in item_name:
        return "HEALTH_POTION"
    elif "potion" in item_name and "mana" in item_name:
        return "MANA_POTION"
    elif "potion" in item_name or "elixir" in item_name:
        return "POTION"
    elif "ring" in item_name:
        return "RING"
    elif "amulet" in item_name or "pendant" in item_name or "crown" in item_name:
        return "AMULET"
    elif "gold" in item_name or "treasure" in item_name:
        return "GOLD"
    else:
        return "MISC" 