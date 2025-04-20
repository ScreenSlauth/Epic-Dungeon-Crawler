import pygame
from ..settings import *
import math

class HUD:
    """Heads-up display showing player stats and game information"""
    
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Define HUD regions
        self.left_panel_rect = pygame.Rect(UI_PADDING, UI_PADDING, 
                                      UI_ELEMENT_WIDTH, SCREEN_HEIGHT - UI_PADDING * 2)
        self.right_panel_rect = pygame.Rect(SCREEN_WIDTH - UI_ELEMENT_WIDTH - UI_PADDING, 
                                       UI_PADDING, UI_ELEMENT_WIDTH, 
                                       SCREEN_HEIGHT - UI_PADDING * 2)
        self.bottom_panel_rect = pygame.Rect(UI_ELEMENT_WIDTH + UI_PADDING * 2, 
                                        SCREEN_HEIGHT - UI_ELEMENT_HEIGHT - UI_PADDING,
                                        SCREEN_WIDTH - UI_ELEMENT_WIDTH * 2 - UI_PADDING * 4,
                                        UI_ELEMENT_HEIGHT)
                                        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, UI_TITLE_SIZE)
        self.heading_font = pygame.font.Font(None, UI_HEADING_SIZE)
        self.normal_font = pygame.font.Font(None, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(None, UI_FONT_SIZE - 6)
        self.smaller_font = pygame.font.Font(None, UI_FONT_SIZE - 10)
        
        # HUD element dimensions
        self.stat_bar_height = 20
        self.stat_bar_width = 200
        self.padding = UI_PADDING
        
        # Initialize animation variables
        self.animation_timer = 0
        self.low_health_flash = 0
        
        # Load or create HUD elements
        self.initialize_hud_elements()
        
    def initialize_hud_elements(self):
        """Initialize static HUD elements like backgrounds"""
        # Create semi-transparent surface for panels
        self.panel_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw left panel background
        pygame.draw.rect(self.panel_surface, UI_COLORS["BACKGROUND"], 
                        self.left_panel_rect, border_radius=5)
        pygame.draw.rect(self.panel_surface, UI_COLORS["BORDER"], 
                        self.left_panel_rect, width=UI_BORDER_SIZE, border_radius=5)
        
        # Draw right panel background
        pygame.draw.rect(self.panel_surface, UI_COLORS["BACKGROUND"], 
                        self.right_panel_rect, border_radius=5)
        pygame.draw.rect(self.panel_surface, UI_COLORS["BORDER"], 
                        self.right_panel_rect, width=UI_BORDER_SIZE, border_radius=5)
        
        # Draw bottom panel background
        pygame.draw.rect(self.panel_surface, UI_COLORS["BACKGROUND"], 
                        self.bottom_panel_rect, border_radius=5)
        pygame.draw.rect(self.panel_surface, UI_COLORS["BORDER"], 
                        self.bottom_panel_rect, width=UI_BORDER_SIZE, border_radius=5)
        
    def render(self, player, active_quest=None, current_floor=1, theme_color=None):
        """Render the HUD with all elements"""
        # Draw HUD background panels first
        self.render_background_panels(theme_color)
        
        # Draw player stats panel
        self.render_stats_panel(player, current_floor, theme_color)
        
        # Draw quest panel if there is an active quest
        if active_quest:
            self.render_quest_panel(active_quest, theme_color)
            
        # Draw floor info
        floor_text = f"Floor {current_floor}"
        floor_surf = self.normal_font.render(floor_text, True, UI_COLORS["HIGHLIGHT"])
        floor_rect = floor_surf.get_rect(topleft=(20, 20))
        self.screen.blit(floor_surf, floor_rect)
        
        # Render minimap if enabled
        if hasattr(player, 'dungeon') and player.dungeon:
            self.render_minimap(player.dungeon, player)
        elif ADVANCED_SETTINGS.get("MINIMAP_ENABLED", True):
            # Fallback to placeholder minimap if no dungeon reference
            self.render_placeholder_minimap()
    
    def render_background_panels(self, theme_color=None):
        """Render the background panels for the HUD"""
        # Apply biome theming if provided
        if theme_color is None:
            panel_bg = UI_COLORS["PANEL_BG"]
            border_color = UI_COLORS["BORDER"]
        else:
            # Use biome colors for theming
            panel_bg = UI_COLORS["PANEL_BG"]  # Keep standard background
            border_color = theme_color  # Use biome color for borders
        
        # Create semi-transparent surface for panels with rounded corners
        panel_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw left panel background with rounded corners
        pygame.draw.rect(panel_surface, panel_bg, 
                       self.left_panel_rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(panel_surface, border_color, 
                       self.left_panel_rect, width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        
        # Draw right panel background with rounded corners
        pygame.draw.rect(panel_surface, panel_bg, 
                       self.right_panel_rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(panel_surface, border_color, 
                       self.right_panel_rect, width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        
        # Draw bottom panel background with rounded corners
        pygame.draw.rect(panel_surface, panel_bg, 
                       self.bottom_panel_rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(panel_surface, border_color, 
                       self.bottom_panel_rect, width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        
        # Blit the panel surface onto the screen
        self.screen.blit(panel_surface, (0, 0))
        
    def render_stats_panel(self, player, current_floor, theme_color):
        """Render the player stats panel"""
        self.animation_timer = (self.animation_timer + 1) % 360
        
        # Apply biome theming if provided
        if theme_color is None:
            text_color = UI_COLORS["TEXT"]
            highlight_color = UI_COLORS["HIGHLIGHT"]
        else:
            # Use biome colors for theming
            text_color = UI_COLORS["TEXT"]  # Keep standard text
            highlight_color = UI_COLORS["HIGHLIGHT"]  # Keep standard highlights
        
        # Get player status
        status = player.get_status()
        
        # Update low health flash animation if health is critical
        if status['health'] < status['max_health'] * 0.25:
            self.low_health_flash = (self.low_health_flash + 1) % 30  # Flash cycle
        else:
            self.low_health_flash = 0
        
        # Draw health bar
        self.draw_health_bar(status)
        
        # Draw XP bar
        self.draw_xp_bar(status)
        
        # Draw mana bar
        self.draw_mana_bar(status)
        
        # Draw level and score
        self.draw_player_stats(status)
        
        # Draw current floor
        self.draw_floor_info(current_floor, theme_color)
        
        # Draw inventory count
        self.draw_inventory_status(status)
        
    def draw_health_bar(self, player_status):
        """Draw player health bar"""
        # Get health information
        health = player_status["health"]
        max_health = player_status["max_health"]
        health_percent = max(0, min(1, health / max_health))
        
        # Bar position
        x = self.padding
        y = self.padding
        
        # Draw bar background
        bar_rect = pygame.Rect(x, y, self.stat_bar_width, self.stat_bar_height)
        pygame.draw.rect(self.screen, UI_COLORS["HEALTH_BAR_BG"], bar_rect, border_radius=5)
        
        # Draw health fill
        fill_width = int(self.stat_bar_width * health_percent)
        fill_rect = pygame.Rect(x, y, fill_width, self.stat_bar_height)
        
        # Add low health flash effect
        health_color = UI_COLORS["HEALTH_BAR"]
        if health_percent < 0.25 and self.low_health_flash > 15:
            # Flash to brighter red when critically low
            health_color = (255, 100, 100)
            
        pygame.draw.rect(self.screen, health_color, fill_rect, border_radius=5)
        
        # Draw border
        pygame.draw.rect(self.screen, UI_COLORS["BORDER"], bar_rect, width=1, border_radius=5)
        
        # Draw text
        health_text = f"HP: {health}/{max_health}"
        text_surf = self.normal_font.render(health_text, True, UI_COLORS["TEXT"])
        text_rect = text_surf.get_rect(center=bar_rect.center)
        self.screen.blit(text_surf, text_rect)
        
    def draw_xp_bar(self, player_status):
        """Draw player XP bar"""
        # Get XP information
        xp = player_status["xp"]
        xp_to_level = player_status["xp_to_level_up"]
        xp_percent = max(0, min(1, xp / xp_to_level))
        
        # Bar position
        x = self.padding
        y = self.padding * 2 + self.stat_bar_height
        
        # Draw bar background
        bar_rect = pygame.Rect(x, y, self.stat_bar_width, self.stat_bar_height)
        pygame.draw.rect(self.screen, UI_COLORS["XP_BAR_BG"], bar_rect, border_radius=5)
        
        # Draw XP fill
        fill_width = int(self.stat_bar_width * xp_percent)
        fill_rect = pygame.Rect(x, y, fill_width, self.stat_bar_height)
        pygame.draw.rect(self.screen, UI_COLORS["XP_BAR"], fill_rect, border_radius=5)
        
        # Draw border
        pygame.draw.rect(self.screen, UI_COLORS["BORDER"], bar_rect, width=1, border_radius=5)
        
        # Draw text
        xp_text = f"XP: {xp}/{xp_to_level}"
        text_surf = self.normal_font.render(xp_text, True, UI_COLORS["TEXT"])
        text_rect = text_surf.get_rect(center=bar_rect.center)
        self.screen.blit(text_surf, text_rect)
        
    def draw_mana_bar(self, player_status):
        """Draw player mana bar"""
        # Get mana information
        mana = player_status["mana"]
        max_mana = player_status["max_mana"]
        mana_percent = max(0, min(1, mana / max_mana))
        
        # Bar position
        x = self.padding
        y = self.padding * 3 + self.stat_bar_height * 2
        
        # Draw bar background
        bar_rect = pygame.Rect(x, y, self.stat_bar_width, self.stat_bar_height)
        pygame.draw.rect(self.screen, UI_COLORS["MANA_BAR_BG"], bar_rect, border_radius=5)
        
        # Draw mana fill
        fill_width = int(self.stat_bar_width * mana_percent)
        fill_rect = pygame.Rect(x, y, fill_width, self.stat_bar_height)
        pygame.draw.rect(self.screen, UI_COLORS["MANA_BAR"], fill_rect, border_radius=5)
        
        # Draw border
        pygame.draw.rect(self.screen, UI_COLORS["BORDER"], bar_rect, width=1, border_radius=5)
        
        # Draw text
        mana_text = f"MP: {mana}/{max_mana}"
        text_surf = self.normal_font.render(mana_text, True, UI_COLORS["TEXT"])
        text_rect = text_surf.get_rect(center=bar_rect.center)
        self.screen.blit(text_surf, text_rect)
        
    def draw_player_stats(self, player_status):
        """Draw player level, gold, attack and defense"""
        # Stats position
        x = self.padding
        y = self.padding * 4 + self.stat_bar_height * 3
        
        # Draw level
        level_text = f"Level: {player_status['level']}"
        level_surf = self.normal_font.render(level_text, True, UI_COLORS["TEXT"])
        self.screen.blit(level_surf, (x, y))
        
        # Draw gold
        gold_text = f"Gold: {player_status['gold']}"
        gold_surf = self.normal_font.render(gold_text, True, UI_COLORS["HIGHLIGHT"])
        gold_y = y + level_surf.get_height() + 5
        self.screen.blit(gold_surf, (x, gold_y))
        
        # Draw attack
        attack_text = f"ATK: {player_status['damage']}"
        attack_surf = self.normal_font.render(attack_text, True, UI_COLORS["TEXT"])
        attack_y = gold_y + gold_surf.get_height() + 5
        self.screen.blit(attack_surf, (x, attack_y))
        
        # Draw defense
        defense_text = f"DEF: {player_status['defense']}"
        defense_surf = self.normal_font.render(defense_text, True, UI_COLORS["TEXT"])
        defense_y = attack_y + attack_surf.get_height() + 5
        self.screen.blit(defense_surf, (x, defense_y))
        
        # Draw score
        score_text = f"Score: {player_status['score']}"
        score_surf = self.normal_font.render(score_text, True, UI_COLORS["HIGHLIGHT_ALT"])
        score_y = defense_y + defense_surf.get_height() + 5
        self.screen.blit(score_surf, (x, score_y))
        
    def draw_floor_info(self, current_floor, theme_color=None):
        """Draw current dungeon floor information"""
        # Use theme color or default
        text_color = theme_color if theme_color else UI_COLORS["TEXT"]
        
        # Floor text with pulsing effect
        pulse = (math.sin(self.animation_timer * 0.05) * 0.2) + 0.8  # Value between 0.8 and 1.0
        
        floor_text = f"Floor {current_floor}"
        text_surf = self.title_font.render(floor_text, True, text_color)
        
        # Apply subtle pulse scaling for emphasis
        if current_floor % 5 == 0:  # Special floors get a pulse effect
            width = int(text_surf.get_width() * pulse)
            height = int(text_surf.get_height() * pulse)
            if width > 0 and height > 0:
                text_surf = pygame.transform.scale(text_surf, (width, height))
        
        # Position at top center
        text_rect = text_surf.get_rect(midtop=(self.width // 2, self.padding))
        self.screen.blit(text_surf, text_rect)
        
    def draw_quest_info(self, quest):
        """Draw active quest information"""
        # Quest panel position
        panel_width = 250
        panel_height = 100
        panel_x = self.width - panel_width - self.padding
        panel_y = self.padding
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, UI_COLORS["PANEL_BG"], panel_rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(self.screen, UI_COLORS["BORDER"], panel_rect, 
                       width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        
        # Draw quest title
        title_surf = self.title_font.render("Active Quest", True, UI_COLORS["HIGHLIGHT"])
        title_rect = title_surf.get_rect(midtop=(panel_rect.centerx, panel_rect.top + 10))
        self.screen.blit(title_surf, title_rect)
        
        # Draw quest name
        name_surf = self.normal_font.render(quest.name, True, UI_COLORS["TEXT"])
        name_rect = name_surf.get_rect(midtop=(panel_rect.centerx, title_rect.bottom + 5))
        self.screen.blit(name_surf, name_rect)
        
        # Draw progress
        progress_text = f"Progress: {quest.get_progress_text()}"
        progress_surf = self.small_font.render(progress_text, True, UI_COLORS["TEXT"])
        progress_rect = progress_surf.get_rect(midtop=(panel_rect.centerx, name_rect.bottom + 5))
        self.screen.blit(progress_surf, progress_rect)
        
        # Draw reward
        reward_text = f"Reward: {quest.get_reward_text()}"
        reward_surf = self.small_font.render(reward_text, True, UI_COLORS["TEXT"])
        reward_rect = reward_surf.get_rect(midtop=(panel_rect.centerx, progress_rect.bottom + 5))
        self.screen.blit(reward_surf, reward_rect)
        
    def draw_inventory_status(self, player_status):
        """Draw inventory item count"""
        # Inventory position - right side bottom
        inventory_text = f"Items: {player_status['inventory_count']}"
        inv_surf = self.normal_font.render(inventory_text, True, UI_COLORS["TEXT"])
        inv_rect = inv_surf.get_rect(bottomright=(self.width - self.padding, self.height - self.padding))
        self.screen.blit(inv_surf, inv_rect)
        
        # Draw skills if player has any
        if player_status["skills"]:
            skills_text = f"Skills: {', '.join(player_status['skills'])}"
            skills_surf = self.small_font.render(skills_text, True, UI_COLORS["HIGHLIGHT_ALT"])
            skills_rect = skills_surf.get_rect(bottomright=(self.width - self.padding, inv_rect.top - 5))
            self.screen.blit(skills_surf, skills_rect)
        
    def render_quest_panel(self, quest, theme_color=None):
        """Render the quest information panel"""
        # Apply biome theming if provided
        if theme_color is None:
            panel_bg = UI_COLORS["PANEL_BG"]
            border_color = UI_COLORS["BORDER"]
            text_color = UI_COLORS["TEXT"]
            highlight_color = UI_COLORS["HIGHLIGHT"]
        else:
            panel_bg = UI_COLORS["PANEL_BG"]
            border_color = theme_color
            text_color = UI_COLORS["TEXT"]
            highlight_color = UI_COLORS["HIGHLIGHT"]
            
        # Create quest panel rectangle
        quest_panel_rect = pygame.Rect(
            SCREEN_WIDTH - 250, 
            SCREEN_HEIGHT - 150, 
            230, 
            130
        )
        
        # Draw quest panel background
        panel_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, panel_bg, 
                       quest_panel_rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(panel_surface, border_color, 
                       quest_panel_rect, width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        self.screen.blit(panel_surface, (0, 0))
        
        # Draw quest title
        quest_title = quest.name
        title_surf = self.small_font.render(quest_title, True, highlight_color)
        title_rect = title_surf.get_rect(topleft=(quest_panel_rect.x + 10, quest_panel_rect.y + 10))
        self.screen.blit(title_surf, title_rect)
        
        # Draw quest description
        desc_surf = self.small_font.render(quest.description[:40], True, text_color)
        self.screen.blit(desc_surf, (title_rect.x, title_rect.y + 25))
        
        # Draw quest progress
        progress_text = f"Progress: {quest.get_progress_text()}"
        progress_surf = self.small_font.render(progress_text, True, text_color)
        self.screen.blit(progress_surf, (title_rect.x, title_rect.y + 50))
        
        # Draw completion status
        status_text = "Complete" if quest.completed else "In Progress"
        status_color = UI_COLORS["SUCCESS"] if quest.completed else UI_COLORS["TEXT_DARK"]
        status_surf = self.small_font.render(status_text, True, status_color)
        self.screen.blit(status_surf, (title_rect.x, title_rect.y + 75))
        
        # Draw rewards
        reward_text = f"Reward: {quest.get_reward_text()}"
        reward_surf = self.small_font.render(reward_text[:30], True, UI_COLORS["HIGHLIGHT"])
        self.screen.blit(reward_surf, (title_rect.x, title_rect.y + 100))
        
    def render_minimap(self, dungeon, player):
        """Render a minimap of the dungeon"""
        # Create a surface for the minimap
        minimap_surface = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE), pygame.SRCALPHA)
        minimap_surface.fill((0, 0, 0, 180))  # Semi-transparent black background
        
        # Calculate the minimap scale and tile size
        minimap_tile_size = max(2, int(TILE_SIZE * MINIMAP_SCALE))
        
        # Calculate offsets to center the player
        center_x = MINIMAP_SIZE // 2
        center_y = MINIMAP_SIZE // 2
        offset_x = center_x - int(player.x * minimap_tile_size)
        offset_y = center_y - int(player.y * minimap_tile_size)
        
        # Draw dungeon tiles (only explored areas)
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                # Skip if not explored
                if not hasattr(dungeon.grid[y][x], 'explored') or not dungeon.grid[y][x].explored:
                    continue
                    
                # Calculate minimap position
                mini_x = offset_x + int(x * minimap_tile_size)
                mini_y = offset_y + int(y * minimap_tile_size)
                
                # Skip if outside minimap bounds
                if (mini_x < 0 or mini_x > MINIMAP_SIZE - minimap_tile_size or
                    mini_y < 0 or mini_y > MINIMAP_SIZE - minimap_tile_size):
                    continue
                
                # Draw tile based on type
                tile = dungeon.grid[y][x]
                
                if tile.type == 0:  # WALL
                    color = MINIMAP_WALL_COLOR
                elif tile.type == 1:  # FLOOR
                    color = MINIMAP_FLOOR_COLOR
                elif tile.type == 2:  # STAIRS
                    color = MINIMAP_EXIT_COLOR
                else:
                    color = MINIMAP_FLOOR_COLOR
                    
                pygame.draw.rect(minimap_surface, color, 
                               (mini_x, mini_y, minimap_tile_size, minimap_tile_size))
        
        # Draw items
        for item in dungeon.items:
            mini_x = offset_x + int(item.x * minimap_tile_size)
            mini_y = offset_y + int(item.y * minimap_tile_size)
            
            if (mini_x >= 0 and mini_x < MINIMAP_SIZE and 
                mini_y >= 0 and mini_y < MINIMAP_SIZE):
                pygame.draw.rect(minimap_surface, MINIMAP_ITEM_COLOR, 
                               (mini_x, mini_y, minimap_tile_size, minimap_tile_size))
        
        # Draw enemies
        for enemy in dungeon.enemies:
            mini_x = offset_x + int(enemy.x * minimap_tile_size)
            mini_y = offset_y + int(enemy.y * minimap_tile_size)
            
            if (mini_x >= 0 and mini_x < MINIMAP_SIZE and 
                mini_y >= 0 and mini_y < MINIMAP_SIZE):
                pygame.draw.rect(minimap_surface, MINIMAP_ENEMY_COLOR, 
                               (mini_x, mini_y, minimap_tile_size, minimap_tile_size))
        
        # Draw player (always visible)
        player_x = center_x
        player_y = center_y
        pygame.draw.rect(minimap_surface, MINIMAP_PLAYER_COLOR, 
                       (player_x, player_y, minimap_tile_size, minimap_tile_size))
        
        # Draw border
        pygame.draw.rect(minimap_surface, MINIMAP_BORDER_COLOR, 
                       (0, 0, MINIMAP_SIZE, MINIMAP_SIZE), 2)
        
        # Draw minimap title
        minimap_title = self.small_font.render("Minimap", True, UI_COLORS["TEXT"])
        minimap_title_rect = minimap_title.get_rect(centerx=MINIMAP_SIZE//2, top=2)
        minimap_surface.blit(minimap_title, minimap_title_rect)
        
        # Blit minimap to screen
        self.screen.blit(minimap_surface, MINIMAP_POSITION)

    def render_placeholder_minimap(self):
        """Render a placeholder minimap when dungeon data is not available"""
        minimap_rect = pygame.Rect(MINIMAP_POSITION[0], MINIMAP_POSITION[1], MINIMAP_SIZE, MINIMAP_SIZE)
        
        # Draw minimap background
        pygame.draw.rect(self.screen, UI_COLORS["PANEL_BG"], minimap_rect, border_radius=5)
        pygame.draw.rect(self.screen, UI_COLORS["BORDER"], minimap_rect, width=1, border_radius=5)
        
        # Draw minimap title
        minimap_title = self.small_font.render("Minimap", True, UI_COLORS["TEXT"])
        minimap_title_rect = minimap_title.get_rect(centerx=minimap_rect.centerx, top=minimap_rect.top + 5)
        self.screen.blit(minimap_title, minimap_title_rect)
        
        # Draw placeholder text
        placeholder_text = self.small_font.render("Map Data", True, UI_COLORS["TEXT_DARK"])
        placeholder_rect = placeholder_text.get_rect(center=minimap_rect.center)
        self.screen.blit(placeholder_text, placeholder_rect) 