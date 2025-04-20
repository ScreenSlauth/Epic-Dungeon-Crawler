import pygame
import os

def resolve_path(relative_path):
    """Resolve a relative path to an absolute path based on the script location"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

class SoundManager:
    """Manages all game sounds and music"""
    
    def __init__(self):
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(44100, -16, 2, 1024)
                print("Sound manager initialized audio system successfully")
            except pygame.error as e:
                print(f"Warning: Unable to initialize audio system: {e}")
                self.sound_enabled = False
                self.music_enabled = False
                return
                
        # Sound settings
        self.sound_enabled = True
        self.music_enabled = True
        
        # Sound effect volume (0.0 to 1.0)
        self.sound_volume = 0.7
        
        # Music volume (0.0 to 1.0)
        self.music_volume = 0.5
        
        # Current playing music track
        self.current_music = None
        
        # Sound effects dictionary
        self.sounds = {}
        
        # Music tracks dictionary
        self.music = {}
        
        # Load sound effects and music
        self.load_sounds()
        self.load_music()
        
    def load_sounds(self):
        """Load all sound effects"""
        if not self.sound_enabled:
            return
            
        sounds_dir = resolve_path(os.path.join("assets", "sounds"))
        print(f"Loading sounds from directory: {sounds_dir}")
        
        # Default sounds if files are missing
        self.sounds = {
            "step": None,
            "attack": None,
            "player_hurt": None,
            "enemy_die": None,
            "pickup": None,
            "level_up": None,
            "menu_select": None,
            "menu_move": None,
            "door_open": None,
            "game_over": None,
            "potion": None,
            "equip": None,
            "spell": None,
            "chest_open": None
        }
        
        # Check directory exists
        if os.path.exists(sounds_dir):
            # Load sound files if they exist
            for sound_name in self.sounds.keys():
                sound_path = os.path.join(sounds_dir, f"{sound_name}.wav")
                if os.path.exists(sound_path):
                    try:
                        self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                        self.sounds[sound_name].set_volume(self.sound_volume)
                        print(f"Loaded sound: {sound_name}")
                    except pygame.error as e:
                        print(f"Could not load sound: {sound_path} - {e}")
                else:
                    print(f"Warning: Sound file not found: {sound_path}")
        else:
            print(f"Warning: Sound directory not found: {sounds_dir}")
        
    def load_music(self):
        """Load all music tracks"""
        if not self.music_enabled:
            return
            
        music_dir = resolve_path(os.path.join("assets", "music"))
        print(f"Loading music from directory: {music_dir}")
        
        # Define music tracks
        music_tracks = {
            "menu": "menu.mp3",
            "dungeon": "dungeon.mp3",
            "battle": "battle.mp3",
            "boss": "boss.mp3",
            "victory": "victory.mp3",
            "game_over": "game_over.mp3"
        }
        
        # Check directory exists
        if os.path.exists(music_dir):
            # Store paths to music files
            for track_name, filename in music_tracks.items():
                track_path = os.path.join(music_dir, filename)
                if os.path.exists(track_path):
                    self.music[track_name] = track_path
                    print(f"Found music track: {track_name}")
                else:
                    print(f"Warning: Music file not found: {track_path}")
        else:
            print(f"Warning: Music directory not found: {music_dir}")
        
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sound_enabled or self.sound_volume <= 0.01:
            return
            
        try:
            if sound_name in self.sounds and self.sounds[sound_name]:
                self.sounds[sound_name].play()
        except Exception as e:
            print(f"Error playing sound '{sound_name}': {e}")
            
    def play_music(self, track_name, loops=-1, fade_ms=500):
        """Play a music track with optional fading"""
        if not self.music_enabled or self.music_volume <= 0.01:
            return
            
        try:
            if track_name in self.music and self.music[track_name]:
                if self.current_music != track_name:
                    print(f"Playing music track: {track_name}")
                    pygame.mixer.music.fadeout(fade_ms)
                    pygame.mixer.music.load(self.music[track_name])
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(loops, fade_ms=fade_ms)
                    self.current_music = track_name
        except Exception as e:
            print(f"Error playing music track '{track_name}': {e}")
            
    def stop_music(self, fade_ms=500):
        """Stop the currently playing music with optional fading"""
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None
        
    def pause_music(self):
        """Pause the currently playing music"""
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        """Unpause the currently playing music"""
        pygame.mixer.music.unpause()
        
    def set_sound_volume(self, volume):
        """Set the volume for sound effects"""
        # Clamp volume between 0.0 and 1.0
        self.sound_volume = max(0.0, min(1.0, volume))
        
        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sound_volume)
                
    def set_music_volume(self, volume):
        """Set the volume for music"""
        # Clamp volume between 0.0 and 1.0
        self.music_volume = max(0.0, min(1.0, volume))
        
        # Update current music volume
        pygame.mixer.music.set_volume(self.music_volume)
        
    def toggle_sound(self, enabled):
        """Enable or disable sound effects"""
        self.sound_enabled = enabled
        if enabled:
            self.set_sound_volume(0.7)  # Default volume
        else:
            self.set_sound_volume(0.0)  # Mute
            
    def toggle_music(self, enabled):
        """Enable or disable music"""
        self.music_enabled = enabled
        if enabled:
            self.set_music_volume(0.5)  # Default volume
            if self.current_music:
                self.unpause_music()
        else:
            self.set_music_volume(0.0)  # Mute
            self.pause_music()
            
    def is_music_playing(self):
        """Check if music is currently playing"""
        return pygame.mixer.music.get_busy() 