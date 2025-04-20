import pygame
import os
from ..settings import *
import math

class Button:
    """Interactive button class for menus"""
    
    def __init__(self, rect, text, action, color=UI_COLORS["BUTTON"], 
                 hover_color=UI_COLORS["BUTTON_HOVER"], 
                 text_color=UI_COLORS["TEXT"]):
        self.rect = rect
        self.text = text
        self.action = action
        self.color = color
        self.base_color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.clicked = False
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        
    def update(self, mouse_pos, mouse_clicked):
        """Update button state based on mouse interaction"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.color = self.hover_color
            if mouse_clicked:
                self.clicked = True
                return self.action
        else:
            self.color = self.base_color
            
        return None
        
    def draw(self, screen):
        """Draw the button on the screen"""
        # Draw button background
        pygame.draw.rect(screen, self.color, self.rect, border_radius=UI_BORDER_RADIUS)
        pygame.draw.rect(screen, UI_COLORS["BORDER"], self.rect, 
                        width=UI_BORDER_SIZE, border_radius=UI_BORDER_RADIUS)
        
        # Draw button text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
        # Add hover effect
        if self.hovered:
            # Draw glow effect
            glow_rect = self.rect.inflate(4, 4)
            pygame.draw.rect(screen, UI_COLORS["HIGHLIGHT"], glow_rect, 
                            width=2, border_radius=UI_BORDER_RADIUS + 2)

class MainMenu:
    """Main menu screen"""
    
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Menu title
        self.title = "Epic Dungeon Crawler"
        self.title_font = pygame.font.Font(None, UI_TITLE_SIZE)
        
        # Load background image if available
        self.background = None
        bg_path = os.path.join("assets", "images", "menu_bg.png")
        if os.path.exists(bg_path):
            try:
                self.background = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(self.background, (self.width, self.height))
            except:
                print(f"Could not load background image: {bg_path}")
        
        # Create buttons
        button_width = UI_ELEMENT_WIDTH
        button_height = UI_ELEMENT_HEIGHT
        button_spacing = 20
        button_x = (self.width - button_width) // 2
        button_y = self.height // 2
        
        self.buttons = [
            Button(
                pygame.Rect(button_x, button_y, button_width, button_height),
                "New Game", "start"
            ),
            Button(
                pygame.Rect(button_x, button_y + button_height + button_spacing, 
                          button_width, button_height),
                "Options", "options"
            ),
            Button(
                pygame.Rect(button_x, button_y + (button_height + button_spacing) * 2, 
                          button_width, button_height),
                "Quit", "quit"
            )
        ]
        
        # Animation variables for visual interest
        self.animation_timer = 0
        
    def handle_event(self, event):
        """Handle menu input events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check button clicks
            for button in self.buttons:
                action = button.update(mouse_pos, True)
                if action:
                    self.sound_manager.play_sound("menu_select")
                    return action
                    
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check button hover
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos) and not button.hovered:
                    self.sound_manager.play_sound("menu_move")
                button.update(mouse_pos, False)
                
        return None
        
    def render(self):
        """Render the main menu"""
        # Update animation timer
        self.animation_timer = (self.animation_timer + 1) % 360
        pulse = (math.sin(self.animation_timer * 0.05) * 0.1) + 0.9  # Value between 0.8 and 1.0
        
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Create a gradient background
            for y in range(self.height):
                # Calculate gradient color
                color_value = int(180 * (1 - y / self.height))
                color = (color_value // 3, color_value // 2, color_value)
                pygame.draw.line(self.screen, color, (0, y), (self.width, y))
                
            # Add some decoration
            for i in range(20):
                x = int(self.width * 0.1) + i * int(self.width * 0.04)
                pygame.draw.line(self.screen, 
                               (40, 60, 100), 
                               (x, 0), 
                               (x - 200, self.height), 
                               3)
        
        # Draw title with pulse effect
        title_surf = self.title_font.render(self.title, True, UI_COLORS["HIGHLIGHT"])
        # Apply pulse scaling
        scaled_width = int(title_surf.get_width() * pulse)
        scaled_height = int(title_surf.get_height() * pulse)
        if scaled_width > 0 and scaled_height > 0:
            title_surf = pygame.transform.scale(title_surf, (scaled_width, scaled_height))
        
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 4))
        
        # Add shadow for better visibility
        shadow_surf = self.title_font.render(self.title, True, COLOR_BLACK)
        shadow_rect = shadow_surf.get_rect(center=(title_rect.centerx + 3, title_rect.centery + 3))
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
            
        # Draw decorative elements
        pygame.draw.line(self.screen, UI_COLORS["BORDER_HIGHLIGHT"],
                       (self.width // 4, title_rect.bottom + 20),
                       (self.width * 3 // 4, title_rect.bottom + 20),
                       2)
                       
        # Add version info at bottom
        version_font = pygame.font.Font(None, 20)
        version_text = version_font.render("v1.0.0", True, UI_COLORS["TEXT_DARK"])
        version_rect = version_text.get_rect(bottomright=(self.width - 20, self.height - 20))
        self.screen.blit(version_text, version_rect)


class OptionsMenu:
    """Options menu screen"""
    
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Menu title
        self.title = "Options"
        self.title_font = pygame.font.Font(None, UI_HEADING_SIZE)
        
        # Create buttons for options
        option_width = UI_ELEMENT_WIDTH
        option_height = UI_ELEMENT_HEIGHT
        option_spacing = 20
        option_x = (self.width - option_width) // 2
        option_y = self.height // 3
        
        # Create option buttons
        self.options_buttons = [
            Button(
                pygame.Rect(option_x, option_y, option_width, option_height),
                "Sound: ON", "sound_toggle"
            ),
            Button(
                pygame.Rect(option_x, option_y + option_height + option_spacing, 
                          option_width, option_height),
                "Music: ON", "music_toggle"
            ),
            Button(
                pygame.Rect(option_x, option_y + (option_height + option_spacing) * 2, 
                          option_width, option_height),
                "Fullscreen: OFF", "fullscreen_toggle"
            )
        ]
        
        # Sound and music are on by default
        self.sound_on = True
        self.music_on = True
        self.fullscreen = False
        
        # Back button
        self.back_button = Button(
            pygame.Rect(option_x, self.height - 100, option_width, option_height),
            "Back", "back"
        )
        
    def handle_event(self, event):
        """Handle menu input events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check option buttons
            for i, button in enumerate(self.options_buttons):
                action = button.update(mouse_pos, True)
                if action:
                    self.sound_manager.play_sound("menu_select")
                    
                    # Handle option toggles
                    if action == "sound_toggle":
                        self.sound_on = not self.sound_on
                        self.options_buttons[0].text = f"Sound: {'ON' if self.sound_on else 'OFF'}"
                        self.sound_manager.toggle_sound(self.sound_on)
                        
                    elif action == "music_toggle":
                        self.music_on = not self.music_on
                        self.options_buttons[1].text = f"Music: {'ON' if self.music_on else 'OFF'}"
                        self.sound_manager.toggle_music(self.music_on)
                        
                    elif action == "fullscreen_toggle":
                        self.fullscreen = not self.fullscreen
                        self.options_buttons[2].text = f"Fullscreen: {'ON' if self.fullscreen else 'OFF'}"
                        # Toggle fullscreen
                        pygame.display.toggle_fullscreen()
                    
                    return None
            
            # Check back button
            action = self.back_button.update(mouse_pos, True)
            if action:
                self.sound_manager.play_sound("menu_select")
                return action
                
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check button hover for options
            for button in self.options_buttons:
                if button.rect.collidepoint(mouse_pos) and not button.hovered:
                    self.sound_manager.play_sound("menu_move")
                button.update(mouse_pos, False)
            
            # Check button hover for back
            if self.back_button.rect.collidepoint(mouse_pos) and not self.back_button.hovered:
                self.sound_manager.play_sound("menu_move")
            self.back_button.update(mouse_pos, False)
                
        return None
        
    def render(self):
        """Render the options menu"""
        # Draw background with gradient
        for y in range(self.height):
            # Calculate gradient color
            color_value = int(120 * (1 - y / self.height))
            color = (color_value // 4, color_value // 3, color_value // 2)
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
        
        # Draw title
        title_surf = self.title_font.render(self.title, True, UI_COLORS["TEXT"])
        title_rect = title_surf.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_surf, title_rect)
        
        # Draw decorative lines
        pygame.draw.line(self.screen, UI_COLORS["BORDER_HIGHLIGHT"],
                       (self.width // 4, title_rect.bottom + 10),
                       (self.width * 3 // 4, title_rect.bottom + 10),
                       2)
        
        # Draw option buttons
        for button in self.options_buttons:
            button.draw(self.screen)
        
        # Draw back button
        self.back_button.draw(self.screen) 