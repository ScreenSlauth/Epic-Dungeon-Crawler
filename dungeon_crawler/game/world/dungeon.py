import pygame
import random
import math
from enum import Enum
from ..tile import Tile, TileType
from ..enemy import Enemy
from ..item import Item
from ..settings import *
import traceback  # For better error reporting

class Biome(Enum):
    """Dungeon biome/theme"""
    CAVERN = 0
    FOREST = 1
    ICE = 2
    LAVA = 3
    SHADOW = 4
    CRYSTAL = 5

# Define a basic Point class for coordinates
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Room:
    """Rectangular room in the dungeon"""
    
    def __init__(self, x, y, width, height, room_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_type = room_type  # normal, entrance, boss, treasure, etc.
        self.connected = False
        
    def center(self):
        """Get the center coordinates of the room"""
        return (self.x + self.width // 2, self.y + self.height // 2)
        
    def random_position(self, edge_buffer=0):
        """Get a random position within the room"""
        x = random.randint(self.x + edge_buffer, self.x + self.width - 1 - edge_buffer)
        y = random.randint(self.y + edge_buffer, self.y + self.height - 1 - edge_buffer)
        return (x, y)
        
    def overlaps(self, other, buffer=0):
        """Check if this room overlaps with another room"""
        return (self.x < other.x + other.width + buffer and
                self.x + self.width + buffer > other.x and
                self.y < other.y + other.height + buffer and
                self.y + self.height + buffer > other.y)
                
    def get_random_wall_position(self):
        """Get a random position along the room's walls"""
        # Decide which wall to use
        wall = random.randint(0, 3)
        
        if wall == 0:  # North wall
            return (random.randint(self.x + 1, self.x + self.width - 2), self.y)
        elif wall == 1:  # East wall
            return (self.x + self.width - 1, random.randint(self.y + 1, self.y + self.height - 2))
        elif wall == 2:  # South wall
            return (random.randint(self.x + 1, self.x + self.width - 2), self.y + self.height - 1)
        else:  # West wall
            return (self.x, random.randint(self.y + 1, self.y + self.height - 2))

class Dungeon:
    """Dungeon map generator and manager"""
    
    def __init__(self, width, height, max_rooms=15, room_min_size=6, room_max_size=12, level=1):
        """Initialize a new dungeon level"""
        try:
            print(f"Creating new dungeon (level {level}, size: {width}x{height})")
            self.width = width
            self.height = height
            self.level = level
            self.rooms = []
            self.grid = [[Tile() for _ in range(width)] for _ in range(height)]
            self.enemies = []
            self.items = []
            self.doors = []
            self.particles = []
            self.floating_texts = []
            self.crystal_formations = []
            self.stairs_down = None
            self.player_start = None
            
            # Animation variables
            self.animation_timer = 0
            
            # Field of view variables
            self.visibility_radius = VISIBILITY_RADIUS
            
            # Determine biome based on level
            print("Determining dungeon biome...")
            self.biome = self.determine_biome()
            print(f"Selected biome: {self.biome.name}")
            
            # Initialize biome-specific features
            print("Initializing biome features...")
            self.init_biome_features()
            
            # Generate the dungeon layout
            print("Generating dungeon layout...")
            self.generate(max_rooms, room_min_size, room_max_size)
            print(f"Dungeon generated with {len(self.rooms)} rooms")
            
            # Field of view variables
            self.visible_tiles = set()
            self.explored_tiles = set()
        except Exception as e:
            print(f"Error during dungeon creation: {e}")
            traceback.print_exc()
            # Set defaults to prevent crashes
            self.width = width
            self.height = height
            self.level = level
            self.rooms = []
            self.grid = [[Tile() for _ in range(width)] for _ in range(height)]
            self.enemies = []
            self.items = []
            self.doors = []
            self.particles = []
            self.floating_texts = []
            self.animation_timer = 0
            self.visibility_radius = VISIBILITY_RADIUS
            self.biome = Biome.CAVERN  # Default biome
            self.stairs_down = (width // 2, height // 2)
            self.player_start = (width // 2, height // 2)
            
    def determine_biome(self):
        """Determine dungeon biome based on level"""
        try:
            # Default biome pattern (can be changed for more complex progression)
            level_to_biome = {
                1: Biome.CAVERN,      # Levels 1-4: Cavern
                5: Biome.FOREST,      # Levels 5-9: Forest
                10: Biome.ICE,        # Levels 10-14: Ice
                15: Biome.LAVA,       # Levels 15-19: Lava
                20: Biome.SHADOW,     # Levels 20-24: Shadow
                25: Biome.CRYSTAL     # Levels 25+: Crystal
            }
            
            # Find the highest level key that is <= current level
            chosen_level = 1  # Default to first level's biome
            for level_threshold in sorted(level_to_biome.keys()):
                if self.level >= level_threshold:
                    chosen_level = level_threshold
                else:
                    break
                    
            return level_to_biome[chosen_level]
        except Exception as e:
            print(f"Error determining biome: {e}")
            return Biome.CAVERN  # Default to CAVERN on error
            
    def init_biome_features(self):
        """Initialize biome-specific features and settings"""
        try:
            # Get biome configurations
            biome_name = self.biome.name
            print(f"Initializing features for biome: {biome_name}")
            
            # Set visibility radius based on biome
            if biome_name in BIOME_FEATURES:
                light_mod = BIOME_FEATURES[biome_name].get("LIGHT_RADIUS", 0)
                self.visibility_radius = max(3, VISIBILITY_RADIUS + light_mod)
                print(f"Setting visibility radius to {self.visibility_radius}")
            
            # Add environmental particles based on biome
            if biome_name == "CAVERN":
                # Cavern: Dust particles and water puddles
                self.create_particle_emitters(15, "dust")
                
            elif biome_name == "FOREST":
                # Forest: Floating leaves, light rays, and small animals
                self.create_particle_emitters(20, "leaf")
                
            elif biome_name == "ICE":
                # Ice: Snowflakes, ice crystals
                self.create_particle_emitters(25, "snow")
                
            elif biome_name == "LAVA":
                # Lava: Embers, smoke, heat distortion
                self.create_particle_emitters(30, "ember")
                
            elif biome_name == "SHADOW":
                # Shadow: Void particles, shadow wisps
                self.create_particle_emitters(20, "shadow")
                
            elif biome_name == "CRYSTAL":
                # Crystal: Light reflections, crystal growth
                self.create_particle_emitters(15, "light")
                self.add_crystal_formations(10)
                
            print(f"Biome features initialized for {biome_name}")
        except Exception as e:
            print(f"Error initializing biome features: {e}")
            # Continue without biome features if there's an error
            
    def create_particle_emitters(self, count, particle_type):
        """Create particle emitters around the dungeon for ambient effects"""
        for _ in range(count):
            if self.rooms:
                room = random.choice(self.rooms)
                x, y = room.random_position(1)
                self.particles.append({
                    "type": particle_type,
                    "x": x,
                    "y": y,
                    "lifetime": random.randint(50, 200),
                    "max_lifetime": random.randint(50, 200),
                    "velocity_x": random.uniform(-0.1, 0.1),
                    "velocity_y": random.uniform(-0.1, 0.1),
                    "size": random.uniform(1, 3),
                    "color": self.get_particle_color(particle_type)
                })
                
    def get_particle_color(self, particle_type):
        """Get appropriate color for a particle based on type and biome"""
        biome_name = self.biome.name
        if particle_type == "dust":
            base_color = BIOME_COLORS[biome_name]["ACCENT"]
            return (base_color[0], base_color[1], base_color[2], random.randint(100, 180))
        elif particle_type == "leaf":
            return (random.randint(20, 80), random.randint(100, 180), random.randint(20, 60), random.randint(150, 200))
        elif particle_type == "snow":
            return (random.randint(200, 255), random.randint(200, 255), random.randint(220, 255), random.randint(150, 200))
        elif particle_type == "ember":
            r = random.randint(200, 255)
            g = random.randint(100, 180)
            b = random.randint(0, 50)
            return (r, g, b, random.randint(150, 200))
        elif particle_type == "shadow":
            return (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(150, 200))
        elif particle_type == "light":
            return (255, 255, 255, 150)  # Default white
        else:
            return (255, 255, 255, 150)  # Default white
            
    def add_crystal_formations(self, count):
        """Add crystal formations for crystal biome"""
        if self.biome == Biome.CRYSTAL and self.rooms:
            for _ in range(count):
                room = random.choice(self.rooms)
                x, y = room.random_position(1)
                self.crystal_formations.append({
                    "type": "crystal_formation",
                    "x": x,
                    "y": y,
                    "size": random.randint(1, 3),
                    "color": (
                        random.randint(150, 220),
                        random.randint(170, 230),
                        random.randint(200, 255)
                    ),
                    "glow_radius": random.randint(2, 5)
                })
                
                # Add light source for the crystal
                self.light_sources.append({
                    "x": x,
                    "y": y,
                    "radius": random.randint(3, 6),
                    "intensity": random.uniform(0.5, 1.0),
                    "color": (150, 200, 255),
                    "flicker": 0.1
                })
                
    def generate(self, max_rooms, room_min_size, room_max_size):
        """Generate a complete dungeon level"""
        # Initialize grid with walls
        self.grid = [[Tile(TileType.WALL) for _ in range(self.width)] for _ in range(self.height)]
        
        # Set minimum successful rooms and maximum generation attempts
        min_rooms = 5
        rooms_created = 0
        max_attempts = max_rooms * 5
        
        # Keep generating until we have enough rooms
        for _ in range(max_attempts):
            if rooms_created >= max_rooms:
                break
                
            # Generate random room dimensions and position
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)
            x = random.randint(1, self.width - w - 2)
            y = random.randint(1, self.height - h - 2)
            
            # Create room
            new_room = Room(x, y, w, h)
            
            # Check if room overlaps with existing rooms
            if not any(new_room.overlaps(room, buffer=1) for room in self.rooms):
                self.add_room(new_room)
                rooms_created += 1
                
                # Connect to previous room if not the first room
                if len(self.rooms) > 1:
                    prev_room = random.choice(self.rooms[:-1])
                    self.connect_rooms(new_room, prev_room)
                    
        # If we don't have enough rooms, start over
        if len(self.rooms) < min_rooms:
            self.generate(max_rooms, room_min_size, room_max_size)
            return
            
        # Make sure all rooms are connected
        self.ensure_connectivity()
        
        # Designate first room as entrance
        if self.rooms:
            self.rooms[0].room_type = "entrance"
            self.player_start = self.rooms[0].center()
            
        # Designate last room as exit (stairs down)
        if len(self.rooms) > 1:
            self.rooms[-1].room_type = "exit"
            x, y = self.rooms[-1].center()
            self.stairs_down = (x, y)
            self.grid[y][x] = Tile(TileType.STAIRS_DOWN)
            
        # Add some doors between rooms
        self.add_doors()
        
        # Add some floor variants for visual interest
        self.add_floor_variants()
        
        # Place entities (enemies, items)
        self.place_entities()
        
    def add_room(self, room):
        """Add a room to the dungeon by carving it out of the walls"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                self.grid[y][x] = Tile(TileType.FLOOR)
                
        self.rooms.append(room)
        
    def connect_rooms(self, room1, room2):
        """Connect two rooms with a corridor"""
        # Get center coordinates
        x1, y1 = room1.center()
        x2, y2 = room2.center()
        
        # Randomly decide if horizontal then vertical, or vertical then horizontal
        if random.choice([True, False]):
            self.create_h_tunnel(x1, x2, y1)
            self.create_v_tunnel(y1, y2, x2)
        else:
            self.create_v_tunnel(y1, y2, x1)
            self.create_h_tunnel(x1, x2, y2)
            
        # Mark both rooms as connected
        room1.connected = True
        room2.connected = True
        
    def create_h_tunnel(self, x1, x2, y):
        """Create a horizontal tunnel between x1 and x2 at y"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.grid[y][x] = Tile(TileType.FLOOR)
            
    def create_v_tunnel(self, y1, y2, x):
        """Create a vertical tunnel between y1 and y2 at x"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.grid[y][x] = Tile(TileType.FLOOR)
            
    def ensure_connectivity(self):
        """Make sure all rooms are connected to the dungeon"""
        # Mark all rooms as not connected
        for room in self.rooms:
            room.connected = False
            
        # Start with the first room
        if self.rooms:
            self.rooms[0].connected = True
            
        # Keep connecting rooms until all are connected
        while not all(room.connected for room in self.rooms):
            # Find a connected room
            connected_rooms = [room for room in self.rooms if room.connected]
            if not connected_rooms:
                break
                
            # Find unconnected rooms and sort by distance to connected rooms
            unconnected_rooms = [room for room in self.rooms if not room.connected]
            if not unconnected_rooms:
                break
                
            # Find the closest unconnected room to any connected room
            closest_pair = None
            min_distance = float('inf')
            
            for conn_room in connected_rooms:
                cx1, cy1 = conn_room.center()
                
                for unconn_room in unconnected_rooms:
                    cx2, cy2 = unconn_room.center()
                    distance = math.sqrt((cx2 - cx1)**2 + (cy2 - cy1)**2)
                    
                    if distance < min_distance:
                        min_distance = distance
                        closest_pair = (conn_room, unconn_room)
            
            # Connect the closest pair of rooms
            if closest_pair:
                self.connect_rooms(closest_pair[0], closest_pair[1])
            else:
                # Fallback to random connection if something went wrong
                self.connect_rooms(random.choice(connected_rooms), random.choice(unconnected_rooms))
                
        # Add some extra connections for better map flow (10% of room count)
        extra_connections = max(1, len(self.rooms) // 10)
        for _ in range(extra_connections):
            room1 = random.choice(self.rooms)
            room2 = random.choice(self.rooms)
            if room1 != room2:
                self.connect_rooms(room1, room2)
            
    def add_doors(self):
        """Add doors between rooms and corridors"""
        # Find potential door locations (floor tiles with exactly 2 orthogonally adjacent wall tiles)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x].type == TileType.FLOOR.value:
                    # Count orthogonal walls
                    wall_count = sum(1 for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)] 
                                    if self.grid[y + dy][x + dx].type == TileType.WALL.value)
                                    
                    # Check if this is potentially a corridor tile between rooms
                    if wall_count == 2 and random.random() < 0.2:  # 20% chance of door
                        # Check diagonal walls to confirm it's a corridor
                        diag_wall_count = sum(1 for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)] 
                                            if self.grid[y + dy][x + dx].type == TileType.WALL.value)
                                            
                        if diag_wall_count >= 2:
                            self.grid[y][x] = Tile(TileType.DOOR)
                            
    def add_floor_variants(self):
        """Add floor variants for visual variety"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].type == TileType.FLOOR.value and random.random() < 0.1:
                    self.grid[y][x].variant = random.randint(1, 2)
                    
    def place_entities(self):
        """Place enemies and items in the dungeon"""
        self.enemies = []
        self.items = []
        
        # Place enemies in all rooms except the first (entrance)
        for room in self.rooms[1:]:
            # More enemies in later rooms
            num_enemies = random.randint(0, 3 + min(self.level // 2, 3))
            
            # Skip exit room sometimes for breathing room
            if room.room_type == "exit" and random.random() < 0.5:
                num_enemies = 0
                
            for _ in range(num_enemies):
                x, y = room.random_position(edge_buffer=1)
                
                # Determine enemy type based on biome and level
                enemy_types = {
                    Biome.CAVERN: ["goblin", "skeleton", "orc"],
                    Biome.FOREST: ["lynx", "goblin", "orc"],
                    Biome.ICE: ["frost_troll", "skeleton", "lynx"],
                    Biome.LAVA: ["magma_elemental", "orc", "frost_troll"],
                    Biome.SHADOW: ["shadow_wraith", "skeleton", "magma_elemental"]
                }
                
                # Choose enemy type, weighted toward biome-specific enemies
                biome_enemies = enemy_types.get(self.biome, ["goblin"])
                enemy_type = random.choices(
                    [biome_enemies[0], biome_enemies[1], biome_enemies[2]],
                    weights=[0.6, 0.3, 0.1],
                    k=1
                )[0]
                
                # Create enemy with level scaling
                enemy = Enemy(x, y, enemy_type, level=self.level)
                self.enemies.append(enemy)
                
        # Place items in rooms
        for room in self.rooms:
            # Health potions are common
            if random.random() < 0.4:
                x, y = room.random_position(edge_buffer=1)
                potion = Item.create_random_item(x, y, level=self.level, force_type="HEALTH_POTION")
                self.items.append(potion)
                
            # Weapons and armor are less common
            if random.random() < 0.15 * self.level / 5:
                x, y = room.random_position(edge_buffer=1)
                item_type = random.choice(["WEAPON", "ARMOR"])
                item = Item.create_random_item(x, y, level=self.level, force_type=item_type)
                self.items.append(item)
                
            # Gold piles
            if random.random() < 0.3:
                x, y = room.random_position(edge_buffer=1)
                gold = Item.create_random_item(x, y, level=self.level, force_type="GOLD")
                self.items.append(gold)
                
        # Place a quest item if level is divisible by 5
        if self.level % 5 == 0:
            quest_room = random.choice(self.rooms[1:-1])  # Not in entrance or exit
            x, y = quest_room.random_position(edge_buffer=2)
            quest_item = Item(x, y, "QUEST_ITEM", None, f"artifact_{self.level}", rarity="legendary")
            self.items.append(quest_item)
            
    def compute_fov(self, player_x, player_y, radius):
        """Compute field of view for the player"""
        # Reset visibility
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].visible = False
                
        # Set player's position as visible and explored
        self.grid[player_y][player_x].visible = True
        self.grid[player_y][player_x].explored = True
        
        # Create a set to store visible tiles
        visible_tiles = set()
        visible_tiles.add((player_x, player_y))
        
        # Check visibility in a square around the player
        for y in range(max(0, player_y - radius), min(self.height, player_y + radius + 1)):
            for x in range(max(0, player_x - radius), min(self.width, player_x + radius + 1)):
                # Skip if outside circular radius
                if math.sqrt((x - player_x)**2 + (y - player_y)**2) > radius:
                    continue
                    
                # Cast ray from player to this position
                if self.has_line_of_sight(player_x, player_y, x, y):
                    self.grid[y][x].visible = True
                    self.grid[y][x].explored = True
                    visible_tiles.add((x, y))
                    
        return visible_tiles
        
    def has_line_of_sight(self, x0, y0, x1, y1):
        """Check if there is a clear line of sight between two points using Bresenham's line algorithm"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while x0 != x1 or y0 != y1:
            # Check if current position blocks sight
            if 0 <= x0 < self.width and 0 <= y0 < self.height:
                if not self.grid[y0][x0].is_transparent() and (x0 != x1 or y0 != y1):
                    return False
                    
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
                
        return True
        
    def update(self):
        """Update dynamic dungeon elements like particles and effects"""
        # Update animation timer
        self.animation_timer = (self.animation_timer + 0.1) % 100
        
        # Update floating text effects
        for text in self.floating_texts[:]:
            text["lifetime"] -= 1
            text["y"] += text["velocity"]
            if text["lifetime"] <= 0:
                self.floating_texts.remove(text)
                
        # Update particles
        for particle in self.particles[:]:
            particle["lifetime"] -= 1
            particle["x"] += particle["velocity_x"]
            particle["y"] += particle["velocity_y"]
            
            # Add some randomness to movement
            particle["velocity_x"] += random.uniform(-0.02, 0.02)
            particle["velocity_y"] += random.uniform(-0.02, 0.02)
            
            # Cap velocity
            particle["velocity_x"] = max(-0.2, min(0.2, particle["velocity_x"]))
            particle["velocity_y"] = max(-0.2, min(0.2, particle["velocity_y"]))
            
            # Remove expired particles
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)
                
        # Periodically create new particles to replace expired ones
        if random.random() < 0.05:
            self.create_particle_emitters(1, self.get_biome_particle_type())
                
    def get_biome_particle_type(self):
        """Get the appropriate particle type for the current biome"""
        biome_name = self.biome.name
        if biome_name == "CAVERN":
            return "dust"
        elif biome_name == "FOREST":
            return "leaf"
        elif biome_name == "ICE":
            return "snow"
        elif biome_name == "LAVA":
            return "ember"
        elif biome_name == "SHADOW":
            return "shadow"
        elif biome_name == "CRYSTAL":
            return "light"
        else:
            return "dust"

    def render(self, screen, player):
        """Render the dungeon with all its elements and apply biome-specific visual effects"""
        # Calculate camera offset to center on player
        # Add safety checks for player position
        if player.x < 0:
            player.x = 0
        if player.y < 0:
            player.y = 0
        if player.x >= self.width:
            player.x = self.width - 1
        if player.y >= self.height:
            player.y = self.height - 1
            
        # Calculate full map size in pixels
        map_width_px = self.width * TILE_SIZE
        map_height_px = self.height * TILE_SIZE
        
        # Calculate camera position (center on player)
        camera_x = player.x * TILE_SIZE - SCREEN_WIDTH // 2
        camera_y = player.y * TILE_SIZE - SCREEN_HEIGHT // 2
        
        # Keep camera within map bounds
        camera_offset_x = max(0, min(camera_x, map_width_px - SCREEN_WIDTH))
        camera_offset_y = max(0, min(camera_y, map_height_px - SCREEN_HEIGHT))
        camera_offset = (camera_offset_x, camera_offset_y)
        
        # Get current biome colors
        biome_name = self.biome.name
        biome_colors = BIOME_COLORS.get(biome_name, BIOME_COLORS["CAVERN"])
        
        # Calculate player's field of view with a fallback for safety
        try:
            visible_tiles = self.compute_fov(player.x, player.y, self.visibility_radius)
            if visible_tiles is None:
                visible_tiles = set()
                visible_tiles.add((player.x, player.y))
        except Exception as e:
            print(f"FOV calculation error: {e}")
            visible_tiles = set()
            visible_tiles.add((player.x, player.y))
        
        # Draw tiles
        for y in range(self.height):
            for x in range(self.width):
                # Screen position
                screen_x = x * TILE_SIZE - camera_offset[0]
                screen_y = y * TILE_SIZE - camera_offset[1]
                
                # Skip tiles outside the screen
                if (screen_x < -TILE_SIZE or screen_x > SCREEN_WIDTH or 
                    screen_y < -TILE_SIZE or screen_y > SCREEN_HEIGHT):
                    continue
                
                # Draw tile based on visibility
                tile = self.grid[y][x]
                if (x, y) in visible_tiles:
                    # Visible tile
                    if tile.type == 0:  # WALL
                        color = biome_colors["WALL"]
                    elif tile.type == 1:  # FLOOR
                        color = biome_colors["FLOOR"]
                    elif tile.type == 2:  # STAIRS_DOWN
                        color = biome_colors["ACCENT"]
                    else:
                        color = biome_colors["FLOOR"]
                        
                    # Apply lighting variation based on distance from player
                    distance = math.sqrt((x - player.x) ** 2 + (y - player.y) ** 2)
                    fade_factor = max(0.5, 1.0 - distance / self.visibility_radius)
                    
                    # Add subtle animation to certain biome elements
                    if biome_name == "LAVA" and tile.type == 1:
                        # Lava pulsing effect
                        pulse = (math.sin(self.animation_timer + x * 0.1 + y * 0.1) + 1) * 0.1
                        fade_factor += pulse
                    elif biome_name == "ICE" and tile.type == 1:
                        # Ice shimmer effect
                        shimmer = (math.sin(self.animation_timer * 2 + x * 0.2 + y * 0.2) + 1) * 0.05
                        fade_factor += shimmer
                    elif biome_name == "CRYSTAL":
                        # Crystal glow effect
                        crystal_pulse = (math.sin(self.animation_timer * 1.5 + x * 0.15 + y * 0.15) + 1) * 0.15
                        fade_factor += crystal_pulse
                        
                    # Apply fade factor to color
                    r = min(255, int(color[0] * fade_factor))
                    g = min(255, int(color[1] * fade_factor))
                    b = min(255, int(color[2] * fade_factor))
                    color = (r, g, b)
                    
                    # Draw the base tile
                    pygame.draw.rect(screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    
                    # Add tile details based on biome
                    if tile.type == 1:  # FLOOR
                        if biome_name == "CAVERN" and random.random() < 0.02:
                            # Draw small rocks
                            rock_size = random.randint(2, 5)
                            rock_x = screen_x + random.randint(5, TILE_SIZE - 5)
                            rock_y = screen_y + random.randint(5, TILE_SIZE - 5)
                            pygame.draw.circle(screen, biome_colors["ACCENT"], 
                                             (rock_x, rock_y), rock_size)
                        elif biome_name == "FOREST" and random.random() < 0.03:
                            # Draw grass tufts
                            grass_height = random.randint(3, 7)
                            grass_x = screen_x + random.randint(5, TILE_SIZE - 5)
                            grass_y = screen_y + random.randint(TILE_SIZE - 10, TILE_SIZE - 5)
                            pygame.draw.line(screen, biome_colors["VEGETATION"], 
                                           (grass_x, grass_y), 
                                           (grass_x, grass_y - grass_height), 2)
                        elif biome_name == "ICE" and random.random() < 0.02:
                            # Draw ice crystals
                            crystal_size = random.randint(2, 4)
                            crystal_x = screen_x + random.randint(5, TILE_SIZE - 5)
                            crystal_y = screen_y + random.randint(5, TILE_SIZE - 5)
                            pygame.draw.polygon(screen, (230, 240, 255), 
                                              [(crystal_x, crystal_y - crystal_size),
                                               (crystal_x + crystal_size, crystal_y),
                                               (crystal_x, crystal_y + crystal_size),
                                               (crystal_x - crystal_size, crystal_y)])
                    
                    # Draw special features
                    if tile.type == 2:  # STAIRS_DOWN
                        # Draw stairs
                        for i in range(4):
                            stair_y = screen_y + TILE_SIZE // 4 + i * TILE_SIZE // 8
                            pygame.draw.rect(screen, (40, 40, 40), 
                                           (screen_x + 2, stair_y, TILE_SIZE - 4, TILE_SIZE // 8))
                            
                else:
                    # Not visible - draw as darkness or fog
                    pygame.draw.rect(screen, COLOR_BLACK, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        
        # Draw special features
        for feature in self.crystal_formations:
            # Check if feature is visible
            if (feature["x"], feature["y"]) in visible_tiles:
                # Screen position
                screen_x = feature["x"] * TILE_SIZE - camera_offset[0]
                screen_y = feature["y"] * TILE_SIZE - camera_offset[1]
                
                if feature["type"] == "crystal_formation":
                    # Draw crystal
                    size = feature["size"]
                    color = feature["color"]
                    center_x = screen_x + TILE_SIZE // 2
                    center_y = screen_y + TILE_SIZE // 2
                    
                    # Draw crystal shape
                    points = []
                    for i in range(5):
                        angle = self.animation_timer * 0.1 + i * 2 * math.pi / 5
                        x = center_x + int(size * TILE_SIZE // 4 * math.cos(angle))
                        y = center_y + int(size * TILE_SIZE // 4 * math.sin(angle))
                        points.append((x, y))
                    
                    pygame.draw.polygon(screen, color, points)
                    
                    # Draw glow effect
                    glow_radius = feature["glow_radius"] * TILE_SIZE // 4
                    glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    
                    # Create radial gradient
                    for radius in range(glow_radius, 0, -1):
                        alpha = int(150 * (radius / glow_radius))
                        pygame.draw.circle(glow_surface, (*color, alpha), 
                                         (glow_radius, glow_radius), radius)
                                         
                    screen.blit(glow_surface, (center_x - glow_radius, center_y - glow_radius), 
                               special_flags=pygame.BLEND_ADD)
        
        # Draw items
        for item in self.items:
            if (item.x, item.y) in visible_tiles:
                item.draw(screen, camera_offset)
                
        # Draw enemies
        for enemy in self.enemies:
            if (enemy.x, enemy.y) in visible_tiles:
                enemy.draw(screen, camera_offset)
                
        # Draw player - always visible
        player.draw(screen, camera_offset)
        
        # Draw particles
        for particle in self.particles:
            # Check if particle is visible
            if (int(particle["x"]), int(particle["y"])) in visible_tiles:
                # Calculate screen position
                screen_x = int(particle["x"] * TILE_SIZE - camera_offset[0])
                screen_y = int(particle["y"] * TILE_SIZE - camera_offset[1])
                
                # Draw particle
                if particle["type"] == "dust":
                    pygame.draw.circle(screen, particle["color"], 
                                     (screen_x, screen_y), particle["size"])
                elif particle["type"] == "leaf":
                    # Draw simple leaf shape
                    pygame.draw.ellipse(screen, particle["color"], 
                                      (screen_x, screen_y, 
                                       particle["size"] * 2, particle["size"]))
                elif particle["type"] == "snow":
                    pygame.draw.circle(screen, particle["color"], 
                                     (screen_x, screen_y), particle["size"])
                elif particle["type"] == "ember":
                    # Flicker the ember
                    flicker = random.uniform(0.7, 1.3)
                    size = particle["size"] * flicker
                    # Draw with additive blending for glow effect
                    ember_surface = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)
                    pygame.draw.circle(ember_surface, particle["color"], 
                                     (int(size * 2), int(size * 2)), int(size))
                    screen.blit(ember_surface, (screen_x - int(size * 2), screen_y - int(size * 2)), 
                               special_flags=pygame.BLEND_ADD)
                elif particle["type"] == "shadow":
                    # Shadow particle with pulsating effect
                    pulse = (math.sin(self.animation_timer * 2) + 1) * 0.5
                    size = particle["size"] * (0.7 + pulse * 0.3)
                    pygame.draw.circle(screen, particle["color"], 
                                     (screen_x, screen_y), size)
                elif particle["type"] == "light":
                    # Light particle with pulsating effect
                    pulse = (math.sin(self.animation_timer * 2) + 1) * 0.5
                    size = particle["size"] * (0.7 + pulse * 0.3)
                    pygame.draw.circle(screen, particle["color"], 
                                     (screen_x, screen_y), size)
                else:
                    pygame.draw.circle(screen, particle["color"], 
                                     (screen_x, screen_y), particle["size"])
                                     
        # Apply biome-specific post-processing effects
        if biome_name == "SHADOW":
            # Shadow realm darkness effect
            shadow_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            shadow_overlay.fill((0, 0, 20, 50))  # Dark blue tint
            screen.blit(shadow_overlay, (0, 0))
            
            # Draw randomly appearing void tendrils
            if random.random() < 0.01:
                start_x = random.randint(0, SCREEN_WIDTH)
                start_y = random.randint(0, SCREEN_HEIGHT)
                for i in range(5):
                    end_x = start_x + random.randint(-100, 100)
                    end_y = start_y + random.randint(-100, 100)
                    # Draw with low alpha
                    pygame.draw.line(shadow_overlay, (80, 20, 120, 50), 
                                   (start_x, start_y), (end_x, end_y), 2)
                    start_x, start_y = end_x, end_y
                screen.blit(shadow_overlay, (0, 0))
        
        elif biome_name == "LAVA":
            # Heat distortion effect (subtle wavy overlay)
            distortion = (math.sin(self.animation_timer) + 1) * 0.5
            heat_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for y in range(0, SCREEN_HEIGHT, 10):
                wave = math.sin(y * 0.05 + self.animation_timer) * 5 * distortion
                pygame.draw.line(heat_overlay, (255, 100, 20, 5), 
                               (0, y), (SCREEN_WIDTH, y + wave))
            screen.blit(heat_overlay, (0, 0))
            
        # Draw floating text
        for text in self.floating_texts:
            # Calculate screen position
            screen_x = text["x"] * TILE_SIZE - camera_offset[0] + TILE_SIZE // 2
            screen_y = text["y"] * TILE_SIZE - camera_offset[1] + TILE_SIZE // 2
            
            # Scale opacity with lifetime
            alpha = min(255, int(255 * text["lifetime"] / 20))
            
            # Create text surface with alpha
            font = pygame.font.Font(None, 24)
            text_surf = font.render(text["text"], True, text["color"])
            text_surf.set_alpha(alpha)
            
            # Position text
            text_rect = text_surf.get_rect(center=(screen_x, screen_y))
            screen.blit(text_surf, text_rect)
        
    def is_position_valid(self, x, y):
        """Check if a position is valid for movement"""
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                self.grid[y][x].is_walkable()) 