import pygame
import sys
import os
import math
import traceback  # Added for better error reporting
from game.game_state import GameState
from game.world.dungeon import Dungeon, Biome  # Explicitly import Biome
from game.player import Player
from game.ui.menu import MainMenu, OptionsMenu  # Import OptionsMenu directly
from game.ui.hud import HUD
from game.quest_manager import QuestManager
from game.sound_manager import SoundManager
from game.settings import *

# Add absolute path resolution helper
def resolve_path(relative_path):
    """Resolve a relative path to an absolute path based on the script location"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

class DungeonCrawler:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up logging for debugging
        print("Initializing Epic Dungeon Crawler...")
        print(f"Working directory: {os.getcwd()}")
        
        # Initialize audio systems with error handling
        try:
            pygame.mixer.init(44100, -16, 2, 1024)
            print("Audio system initialized successfully")
        except pygame.error as e:
            print(f"Warning: Audio system initialization failed: {e}")
            print("The game will run without sound")
        
        pygame.font.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Epic Dungeon Crawler")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Load game icon with proper error handling
        icon_path = resolve_path(os.path.join("assets", "images", "icon.png"))
        print(f"Looking for icon at: {icon_path}")
        if os.path.exists(icon_path):
            try:
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
                print("Game icon loaded successfully")
            except pygame.error as e:
                print(f"Warning: Could not load game icon: {e}")
        else:
            print(f"Warning: Icon file not found at {icon_path}")
        
        # Initialize game state
        self.game_state = GameState.MAIN_MENU
        
        # Initialize managers and UI elements with error handling
        try:
            print("Initializing sound manager...")
            self.sound_manager = SoundManager()
            
            print("Initializing quest manager...")
            self.quest_manager = QuestManager()
            
            print("Initializing main menu...")
            self.main_menu = MainMenu(self.screen, self.sound_manager)
            
            print("Initializing options menu...")
            self.options_menu = OptionsMenu(self.screen, self.sound_manager)
            
            print("Initializing HUD...")
            self.hud = HUD(self.screen)
            
            print("All managers and UI elements initialized successfully")
        except Exception as e:
            print(f"Error during initialization of game components: {e}")
            traceback.print_exc()
            
        # Initialize game objects
        self.current_floor = 1
        self.dungeon = None
        self.player = None
        
        # Initialize game variables
        self.running = True
        self.paused = False
        
        # Start background music with error handling
        try:
            print("Starting menu music...")
            self.sound_manager.play_music("menu")
            print("Menu music started successfully")
        except Exception as e:
            print(f"Warning: Could not play menu music: {e}")

    def initialize_game(self):
        """Initialize a new game"""
        print("Initializing new game at floor", self.current_floor, "...")
        
        # Create a dungeon for the current floor
        self.dungeon = Dungeon(GRID_WIDTH, GRID_HEIGHT, 
                              max_rooms=12, 
                              room_min_size=6, 
                              room_max_size=12,
                              level=max(1, self.current_floor))

        # Determine biome type based on current floor
        self.dungeon.determine_biome()
        print(f"Dungeon created with biome: {self.dungeon.biome.name}")

        # Initialize biome-specific features
        self.dungeon.init_biome_features()
        
        # Create player at a valid position
        valid_room = self.dungeon.rooms[0]  # Use first room for player
        player_x, player_y = valid_room.center()
        self.player = Player(player_x, player_y)
        self.player.dungeon = self.dungeon  # Give player reference to dungeon
        print(f"Player created at position {player_x}, {player_y}")
        
        # Generate enemies and items in the dungeon
        self.dungeon.place_entities()
        
        # Initialize quest for this floor
        self.quest_manager = QuestManager()
        new_quest = self.quest_manager.generate_quest(self.current_floor, self.dungeon.biome)
        self.quest_manager.active_quest = new_quest
        
        # Start dungeon background music
        print("Starting dungeon background music...")
        self.sound_manager.play_music("dungeon")
        print("Dungeon music started successfully")
        
        print("Game initialized successfully")

    def handle_events(self):
        """Process all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Handle menu events
            if self.game_state == GameState.MAIN_MENU:
                menu_action = self.main_menu.handle_event(event)
                if menu_action == "start":
                    # Initialize game and UI components
                    self.initialize_game()
                    
                    # Ensure all UI components are properly initialized
                    if not hasattr(self, 'hud') or self.hud is None:
                        print("Initializing HUD...")
                        self.hud = HUD(self.screen)
                    
                    if not hasattr(self, 'quest_manager') or self.quest_manager is None:
                        print("Initializing quest manager...")
                        self.quest_manager = QuestManager()
                    
                    # Set the game state to PLAYING after initialization
                    self.game_state = GameState.PLAYING
                    print("Game state changed to PLAYING")
                elif menu_action == "options":
                    # Transition to options menu
                    self.game_state = GameState.OPTIONS
                elif menu_action == "quit":
                    self.running = False
                    
            # Handle options menu events
            elif self.game_state == GameState.OPTIONS:
                options_action = self.options_menu.handle_event(event)
                if options_action == "back":
                    # Print a debug message to verify this code is being reached
                    print("Back button clicked, returning to main menu")
                    self.game_state = GameState.MAIN_MENU
                    
            # Handle gameplay events
            elif self.game_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    
                    if not self.paused:
                        self.handle_player_input(event)
            
            # Handle game over events
            elif self.game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_state = GameState.MAIN_MENU
                    
    def handle_player_input(self, event):
        """Handle player keyboard input during gameplay"""
        try:
            if event.key in (pygame.K_UP, pygame.K_w):
                result = self.player.move(0, -1, self.dungeon)
                self.handle_move_result(result)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                result = self.player.move(0, 1, self.dungeon)
                self.handle_move_result(result)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                result = self.player.move(-1, 0, self.dungeon)
                self.handle_move_result(result)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                result = self.player.move(1, 0, self.dungeon)
                self.handle_move_result(result)
            elif event.key == pygame.K_SPACE:
                self.player.use_item()
        except Exception as e:
            print(f"Error handling player input: {e}")
            
    def handle_move_result(self, result):
        """Handle the result of a player movement attempt"""
        if result == True:
            self.sound_manager.play_sound("step")
        elif result == "next_floor":
            self.advance_floor()
            
    def update(self):
        """Update game state"""
        if self.game_state == GameState.PLAYING and not self.paused:
            try:
                # Update dungeon elements
                if self.dungeon:
                    self.dungeon.update()
                
                # Update player
                if self.player:
                    self.player.update()
                
                # Update enemies
                for enemy in self.dungeon.enemies[:]:  # Use a copy to safely modify during iteration
                    enemy.update(self.player, self.dungeon)
                    
                # Check for combat
                self.check_combat()
                    
                # Check for item pickup
                self.check_item_pickup()
                    
                # Update quest
                self.quest_manager.update_quest(self.player, self.dungeon)
                    
                # Check if floor is cleared
                if not self.dungeon.enemies:
                    self.advance_floor()
                    
                # Check player health
                if self.player.health <= 0:
                    self.game_state = GameState.GAME_OVER
                    self.sound_manager.play_sound("game_over")
                    self.sound_manager.play_music("game_over")
            except Exception as e:
                print(f"Error during game update: {e}")
    
    def check_combat(self):
        """Check for player-enemy combat"""
        for enemy in self.dungeon.enemies[:]:
            if (abs(self.player.x - enemy.x) <= 1 and abs(self.player.y - enemy.y) <= 1):
                # Player attacks enemy
                damage_to_enemy = self.player.get_attack_damage()
                enemy.health -= damage_to_enemy
                
                # Show damage numbers
                self.dungeon.floating_texts.append({
                    "x": enemy.x, 
                    "y": enemy.y,
                    "text": str(damage_to_enemy),
                    "color": (255, 0, 0),
                    "lifetime": 20,
                    "velocity": -0.2
                })
                
                # Play attack sound
                self.sound_manager.play_sound("attack")
                
                if enemy.health <= 0:
                    enemy.alive = False
                    self.dungeon.enemies.remove(enemy)
                    self.player.add_xp(50)
                    self.player.add_score(50)
                    self.sound_manager.play_sound("enemy_die")
                else:
                    # Enemy counterattacks
                    damage_to_player = max(0, enemy.base_damage - self.player.defense)
                    self.player.health -= damage_to_player
                    
                    # Show damage numbers
                    self.dungeon.floating_texts.append({
                        "x": self.player.x, 
                        "y": self.player.y,
                        "text": str(damage_to_player),
                        "color": (255, 255, 0),
                        "lifetime": 20,
                        "velocity": -0.2
                    })
                    
                    if damage_to_player > 0:
                        self.sound_manager.play_sound("player_hurt")
    
    def check_item_pickup(self):
        """Check for item pickup by player"""
        for item in self.dungeon.items[:]:
            if (self.player.x, self.player.y) == (item.x, item.y):
                self.player.pickup_item(item)
                self.dungeon.items.remove(item)
                self.sound_manager.play_sound("pickup")
                
    def advance_floor(self):
        """Advance to the next dungeon floor"""
        try:
            self.current_floor += 1
            
            # Save player state before creating new dungeon
            player_health = self.player.health
            player_max_health = self.player.max_health
            player_level = self.player.level
            player_xp = self.player.xp
            player_inventory = self.player.inventory.copy() if hasattr(self.player, 'inventory') else []
            
            # Handle equipment items safely
            player_equipment = {}
            if hasattr(self.player, 'equipment'):
                player_equipment = self.player.equipment.copy()
            
            player_score = self.player.score
            
            # Create new dungeon
            self.dungeon = Dungeon(GRID_WIDTH, GRID_HEIGHT, level=self.current_floor)
            
            # Verify player start position
            if not hasattr(self.dungeon, 'player_start') or not self.dungeon.player_start:
                self.dungeon.player_start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
                
            # Create new player at the start position but maintain stats from previous floor
            self.player = Player(*self.dungeon.player_start)
            self.player.health = player_health
            self.player.max_health = player_max_health
            self.player.level = player_level
            self.player.xp = player_xp
            self.player.inventory = player_inventory
            
            # Set equipment items
            if hasattr(self.player, 'equipment') and player_equipment:
                self.player.equipment = player_equipment
                
            self.player.score = player_score
            
            # Give player a reference to the dungeon for minimap
            self.player.dungeon = self.dungeon
            
            # Update equipment stats if method exists
            if hasattr(self.player, 'recalculate_stats'):
                self.player.recalculate_stats()
            
            # Play sound effect and briefly heal player
            self.sound_manager.play_sound("level_up")
            self.player.health = min(self.player.max_health, self.player.health + 20)
            
            # Add a message about reaching a new floor
            if self.dungeon.floating_texts is not None:
                self.dungeon.floating_texts.append({
                    "x": self.player.x,
                    "y": self.player.y,
                    "text": f"Floor {self.current_floor}",
                    "color": (255, 255, 0),
                    "lifetime": 60,
                    "velocity": -0.1
                })
                
            # Change music based on floor number for variety
            if self.current_floor % 5 == 0:  # Boss floors
                self.sound_manager.play_music("boss")
            else:
                self.sound_manager.play_music("dungeon")
                
        except Exception as e:
            print(f"Error advancing floor: {e}")
            # Emergency fallback - create a simple viable dungeon
            self.current_floor += 1
            self.dungeon = Dungeon(GRID_WIDTH, GRID_HEIGHT, level=self.current_floor)
            self.player.x, self.player.y = self.dungeon.player_start
            self.player.dungeon = self.dungeon
        
    def render(self):
        """Render the current game state"""
        try:
            self.screen.fill(COLOR_BLACK)
            
            if self.game_state == GameState.MAIN_MENU:
                self.main_menu.render()
                
            elif self.game_state == GameState.OPTIONS:
                self.options_menu.render()
                
            elif self.game_state == GameState.PLAYING:
                # Ensure dungeon and player exist
                if self.dungeon is None or self.player is None:
                    print("Error: Dungeon or player missing during rendering")
                    self.game_state = GameState.MAIN_MENU
                    return
                
                # Make sure player has dungeon reference
                if not hasattr(self.player, 'dungeon'):
                    self.player.dungeon = self.dungeon
                    print("Fixed missing player.dungeon reference")
                
                # Draw dungeon with biome-specific visual effects
                self.dungeon.render(self.screen, self.player)
                
                # Draw a semi-transparent UI panel at the top
                ui_panel = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
                ui_panel.fill((30, 40, 60, 200))  # RGBA
                self.screen.blit(ui_panel, (-160, 240))
                        # === DIRECT UI RENDERING - BRUTE FORCE APPROACH ===
        
                # Draw player health bar directly
                health_bar_width = 200
                health_percent = max(0, min(1.0, self.player.health / self.player.max_health))
                
                # Health bar background
                pygame.draw.rect(self.screen, 
                                (80, 25, 25), 
                                pygame.Rect(-80, 100, health_bar_width, 24), 
                                border_radius=5)
                
                # Health bar fill
                pygame.draw.rect(self.screen, 
                                (220, 50, 50), 
                                pygame.Rect(-80, 120, int(health_bar_width * health_percent), 24), 
                                border_radius=5)
                
                # Health text
                font = pygame.font.Font(None, 24)
                hp_text = f"HP: {self.player.health}/{self.player.max_health}"
                hp_surf = font.render(hp_text, True, (230, 230, 240))
                hp_rect = hp_surf.get_rect(center=(-80 + health_bar_width//2, 72))
                self.screen.blit(hp_surf, hp_rect)
                
                # Draw floor info
                floor_text = f"Floor {self.current_floor} | Level {self.player.level}"
                floor_surf = font.render(floor_text, True, (230, 230, 240))
                self.screen.blit(floor_surf, (SCREEN_WIDTH - floor_surf.get_width() - 120, -120))
                
                # Draw score
                score_text = f"Score: {self.player.score}"
                score_surf = font.render(score_text, True, (200, 200, 100))
                self.screen.blit(score_surf, (SCREEN_WIDTH - score_surf.get_width() - 60, 60))
                
                # BRUTE FORCE STATS DISPLAY
                try:
                    # Create a stats panel on the right
                    stats_panel = pygame.Surface((200, 300), pygame.SRCALPHA)
                    stats_panel.fill((20, 30, 40, 200))  # RGBA
                    self.screen.blit(stats_panel, (SCREEN_WIDTH - 360, 220))
                    
                    # Draw player stats directly accessing attributes
                    stats_font = pygame.font.Font(None, 24)
                    y_offset = 10
                    stats_lines = [
                        f"Health: {self.player.health}/{self.player.max_health}",
                        f"Level: {self.player.level}",
                        f"XP: {self.player.xp}/{self.player.xp_to_level_up}",
                        f"Score: {self.player.score}",
                        f"Gold: {self.player.gold}",
                        f"Mana: {self.player.mana}/{self.player.max_mana}",
                        f"Damage: {self.player.get_attack_damage()}",
                        f"Defense: {self.player.defense}",
                        f"Items: {len(self.player.inventory)}",
                        f"Skills: {len(self.player.skills)}"
                    ]
                    
                    for line in stats_lines:
                        text_surf = stats_font.render(line, True, (220, 220, 220))
                        self.screen.blit(text_surf, (SCREEN_WIDTH - 360, 240 + y_offset))
                        y_offset += 25
                    
                    # Draw a title for the stats panel
                    title_font = pygame.font.Font(None, 28)
                    title_text = title_font.render("PLAYER STATS", True, (255, 255, 200))
                    title_rect = pygame.Rect(SCREEN_WIDTH - 420, 100, 200, 30)
                    pygame.draw.rect(self.screen, (50, 60, 80), title_rect)
                    self.screen.blit(title_text, (SCREEN_WIDTH - 420, 210))
                    print("Successfully rendered brute force stats")
                except Exception as e:
                    print(f"Error rendering brute force stats: {e}")
                    traceback.print_exc()
                
                # Try to render HUD if available as a fallback
                if hasattr(self, 'hud') and self.hud:
                    try:
                        print("Attempting to render HUD...")
                        biome_type = self.dungeon.biome.name if hasattr(self.dungeon, 'biome') else "CAVERN"
                        biome_theme = UI_COLORS.get(f"{biome_type}_THEME", UI_COLORS["BACKGROUND"])
                        print(f"Using biome type: {biome_type}, theme: {biome_theme}")
                        print(f"Player obj: {self.player}, Quest: {self.quest_manager.active_quest}, Floor: {self.current_floor}")
                        self.hud.render(self.player, self.quest_manager.active_quest, self.current_floor, biome_theme)
                        print("HUD rendered successfully")
                    except Exception as e:
                        print(f"HUD rendering failed: {e}")
                        traceback.print_exc()
                else:
                    print(f"HUD not available: has_hud={hasattr(self, 'hud')}, hud_obj={self.hud if hasattr(self, 'hud') else None}")
                
                # Draw pause overlay if game is paused
                if self.paused:
                    self.render_pause_screen()
                
            elif self.game_state == GameState.GAME_OVER:
                self.render_game_over_screen()
                
            pygame.display.flip()
        except Exception as e:
            print(f"Error during rendering: {e}")
            traceback.print_exc()
        
    def render_pause_screen(self):
        """Render the pause screen overlay with modern UI elements"""
        # Create semi-transparent overlay with a gradient
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Create a gradient background
        for y in range(SCREEN_HEIGHT):
            alpha = 150 + int(y / SCREEN_HEIGHT * 50)  # Gradient from 150 to 200 alpha
            pygame.draw.line(overlay, (20, 25, 35, alpha), 
                           (0, y), (SCREEN_WIDTH, y))
        
        self.screen.blit(overlay, (0, 0))
        
        # Create a center panel
        panel_width = 400
        panel_height = 300
        panel_rect = pygame.Rect(
            (SCREEN_WIDTH - panel_width) // 2,
            (SCREEN_HEIGHT - panel_height) // 2,
            panel_width, panel_height
        )
        
        # Draw panel background with rounded corners
        pygame.draw.rect(self.screen, UI_COLORS["PANEL_BG"], 
                        panel_rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(self.screen, UI_COLORS["BORDER_HIGHLIGHT"], 
                        panel_rect, width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        
        # Calculate a pulse effect for the text
        pulse = math.sin(pygame.time.get_ticks() * 0.003) * 0.2 + 0.8  # Value between 0.6 and 1.0
        
        # Draw pause text with pulse effect
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, UI_COLORS["HIGHLIGHT"])
        
        # Apply pulse scaling
        text_width, text_height = text.get_size()
        scaled_width = int(text_width * pulse)
        scaled_height = int(text_height * pulse)
        if scaled_width > 0 and scaled_height > 0:  # Ensure positive dimensions
            text = pygame.transform.scale(text, (scaled_width, scaled_height))
        
        text_rect = text.get_rect(centerx=panel_rect.centerx, top=panel_rect.top + 40)
        self.screen.blit(text, text_rect)
        
        # Draw a decorative line
        line_y = text_rect.bottom + 20
        pygame.draw.line(self.screen, UI_COLORS["BORDER_HIGHLIGHT"], 
                       (panel_rect.left + 40, line_y),
                       (panel_rect.right - 40, line_y), 2)
        
        # Draw controls info
        y_pos = line_y + 30
        controls = [
            ("ESC", "Resume Game"),
            ("ARROW KEYS / WASD", "Movement"),
            ("SPACE", "Use Item")
        ]
        
        for key, action in controls:
            # Key
            key_font = pygame.font.Font(None, 32)
            key_text = key_font.render(key, True, UI_COLORS["HIGHLIGHT_ALT"])
            key_rect = pygame.Rect(panel_rect.left + 50, y_pos, 200, 36)
            self.screen.blit(key_text, key_rect)
            
            # Action
            action_font = pygame.font.Font(None, 28)
            action_text = action_font.render(action, True, UI_COLORS["TEXT"])
            action_rect = pygame.Rect(panel_rect.left + 220, y_pos, 200, 36)
            self.screen.blit(action_text, action_rect)
            
            y_pos += 45
        
        # Draw a "Resume" button at the bottom
        button_rect = pygame.Rect(
            panel_rect.centerx - 100,
            panel_rect.bottom - 60,
            200, 40
        )
        pygame.draw.rect(self.screen, UI_COLORS["BUTTON"], 
                        button_rect, border_radius=5)
        pygame.draw.rect(self.screen, UI_COLORS["BORDER"], 
                        button_rect, width=1, border_radius=5)
        
        resume_font = pygame.font.Font(None, 32)
        resume_text = resume_font.render("Resume Game", True, UI_COLORS["TEXT"])
        resume_rect = resume_text.get_rect(center=button_rect.center)
        self.screen.blit(resume_text, resume_rect)
        
    def render_game_over_screen(self):
        """Render the game over screen with modern UI elements and animations"""
        # Create dark background with a vignette effect
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Create vignette effect (darker at the edges)
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for radius in range(0, max(SCREEN_WIDTH, SCREEN_HEIGHT), 2):
            alpha = int(radius / max(SCREEN_WIDTH, SCREEN_HEIGHT) * 200)  # Increasing alpha outward
            pygame.draw.circle(vignette, (0, 0, 0, alpha), 
                             (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                             max(SCREEN_WIDTH, SCREEN_HEIGHT) - radius)
        self.screen.blit(vignette, (0, 0))
        
        # Create a center panel
        panel_width = 500
        panel_height = 400
        panel_rect = pygame.Rect(
            (SCREEN_WIDTH - panel_width) // 2,
            (SCREEN_HEIGHT - panel_height) // 2,
            panel_width, panel_height
        )
        
        # Draw panel background with rounded corners
        pygame.draw.rect(self.screen, UI_COLORS["PANEL_BG"], 
                        panel_rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(self.screen, UI_COLORS["ERROR"], 
                        panel_rect, width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        
        # Calculate a pulse effect for the text
        pulse = math.sin(pygame.time.get_ticks() * 0.005) * 0.2 + 0.8  # Value between 0.6 and 1.0
        
        # Draw game over text with pulse effect and glow
        font = pygame.font.Font(None, 80)
        text = font.render("GAME OVER", True, UI_COLORS["ERROR"])
        
        # Create a glow effect
        glow_surfaces = []
        for size in range(5, 0, -1):
            glow_surf = pygame.Surface((text.get_width() + size * 2, text.get_height() + size * 2), pygame.SRCALPHA)
            temp_surf = pygame.transform.scale(text, (text.get_width() + size, text.get_height() + size))
            alpha = 50 - size * 10  # Decreasing alpha for outer glow
            temp_surf.set_alpha(alpha)
            glow_surf.blit(temp_surf, (size // 2, size // 2))
            glow_surfaces.append(glow_surf)
        
        # Draw the glow layers
        text_rect = text.get_rect(centerx=panel_rect.centerx, top=panel_rect.top + 40)
        for glow_surf in glow_surfaces:
            glow_rect = glow_surf.get_rect(center=text_rect.center)
            self.screen.blit(glow_surf, glow_rect)
        
        # Apply pulse scaling to the main text
        text_width, text_height = text.get_size()
        scaled_width = int(text_width * pulse)
        scaled_height = int(text_height * pulse)
        if scaled_width > 0 and scaled_height > 0:  # Ensure positive dimensions
            scaled_text = pygame.transform.scale(text, (scaled_width, scaled_height))
            scaled_rect = scaled_text.get_rect(center=text_rect.center)
            self.screen.blit(scaled_text, scaled_rect)
        else:
            self.screen.blit(text, text_rect)
        
        # Draw a decorative line
        line_y = text_rect.bottom + 20
        pygame.draw.line(self.screen, UI_COLORS["ERROR"], 
                       (panel_rect.left + 40, line_y),
                       (panel_rect.right - 40, line_y), 2)
        
        # Draw dungeon floor reached
        floor_font = pygame.font.Font(None, 32)
        floor_text = floor_font.render(f"Dungeon Floor: {self.current_floor}", 
                                     True, UI_COLORS["TEXT"])
        floor_rect = floor_text.get_rect(centerx=panel_rect.centerx, top=line_y + 30)
        self.screen.blit(floor_text, floor_rect)
        
        # Draw score with animated counting effect
        score_font = pygame.font.Font(None, 48)
        
        # Simulate counting animation with sin wave
        display_pct = (math.sin(pygame.time.get_ticks() * 0.002 - math.pi/2) + 1) / 2  # 0 to 1 over time
        display_score = int(self.player.score * min(1.0, display_pct + 0.5))  # Show 50-100% of score
        
        score_text = score_font.render(f"Final Score: {display_score}", 
                                     True, UI_COLORS["HIGHLIGHT"])
        score_rect = score_text.get_rect(centerx=panel_rect.centerx, top=floor_rect.bottom + 20)
        self.screen.blit(score_text, score_rect)
        
        # Draw player stats summary
        y_pos = score_rect.bottom + 30
        stats = [
            f"Level: {self.player.level}",
            f"Enemies Defeated: {self.player.score // 50}",  # Assuming 50 points per enemy
            f"Items Collected: {len(self.player.inventory)}"
        ]
        
        for stat in stats:
            stat_font = pygame.font.Font(None, 32)
            stat_text = stat_font.render(stat, True, UI_COLORS["TEXT"])
            stat_rect = stat_text.get_rect(centerx=panel_rect.centerx, top=y_pos)
            self.screen.blit(stat_text, stat_rect)
            y_pos += 35
        
        # Draw restart button with hover effect
        button_rect = pygame.Rect(
            panel_rect.centerx - 120,
            panel_rect.bottom - 60,
            240, 45
        )
        
        # Simulate button hover effect with sin wave
        hover_effect = (math.sin(pygame.time.get_ticks() * 0.004) + 1) / 2  # 0 to 1
        button_color = UI_COLORS["BUTTON"]
        hover_color = UI_COLORS["BUTTON_HOVER"]
        
        # Interpolate between normal and hover color
        r = int(button_color[0] * (1 - hover_effect) + hover_color[0] * hover_effect)
        g = int(button_color[1] * (1 - hover_effect) + hover_color[1] * hover_effect)
        b = int(button_color[2] * (1 - hover_effect) + hover_color[2] * hover_effect)
        
        pygame.draw.rect(self.screen, (r, g, b), button_rect, border_radius=10)
        pygame.draw.rect(self.screen, UI_COLORS["BORDER"], button_rect, width=2, border_radius=10)
        
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Return to Main Menu", True, UI_COLORS["TEXT"])
        restart_rect = restart_text.get_rect(center=button_rect.center)
        self.screen.blit(restart_text, restart_rect)
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    game = DungeonCrawler()
    game.run() 