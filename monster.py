import pygame
import random
import math
from config import GameConfig, Colors
from latin_dictionary import LatinDictionary

class Monster:
    def __init__(self, x, y, difficulty="easy"):
        self.x = x
        self.y = y
        self.width, self.height = GameConfig.MONSTER_SIZE
        self.difficulty = difficulty
        self.speed = GameConfig.MONSTER_SPEED
        
        # Word challenge - will be set by monster manager
        self.dictionary = LatinDictionary()
        self.english_word = None
        self.latin_word = None
        self.difficulty = difficulty
        
        # Visual properties
        self.color = self._get_color_by_difficulty()
        self.eye_color = Colors.MONSTER_EYES
        
        # Animation
        self.animation_time = 0
        self.bob_offset = 0  # Floating/bobbing animation
        
        # State
        self.is_active = True
        self.is_defeated = False
        self.death_animation = 0
        
        # Movement AI
        self.target_x = x
        self.target_y = y
        self.wander_timer = 0
        self.wander_interval = random.uniform(2, 5)  # seconds
        
        # Challenge state
        self.is_challenging = False
        self.challenge_distance = 80  # Distance to trigger challenge
        
    def _get_color_by_difficulty(self):
        """Get monster color based on difficulty"""
        if self.difficulty == "easy":
            return Colors.MONSTER_EASY
        elif self.difficulty == "medium":
            return Colors.MONSTER_MEDIUM
        elif self.difficulty == "hard":
            return Colors.MONSTER_HARD
        else:
            return Colors.MONSTER_EASY
    
    def update(self, player, dt):
        """Update monster behavior"""
        if self.is_defeated:
            self.death_animation += dt * 3  # Speed up death animation
            return
        
        self.animation_time += dt
        self.bob_offset = math.sin(self.animation_time * 3) * 2  # Gentle bobbing
        
        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Check if should challenge player
        if distance < self.challenge_distance and not self.is_challenging:
            self.is_challenging = True
            return "challenge"  # Signal to start word challenge
        
        # Wander behavior when not challenging
        if not self.is_challenging:
            self._update_wandering(dt)
        
        return None
    
    def _update_wandering(self, dt):
        """Update wandering AI behavior"""
        self.wander_timer -= dt
        
        # Set new wander target
        if self.wander_timer <= 0:
            self.target_x = self.x + random.uniform(-100, 100)
            self.target_y = self.y + random.uniform(-50, 50)
            
            # Keep within screen bounds
            self.target_x = max(50, min(GameConfig.SCREEN_WIDTH - 50, self.target_x))
            self.target_y = max(100, min(GameConfig.SCREEN_HEIGHT - 150, self.target_y))
            
            self.wander_timer = random.uniform(3, 6)
        
        # Move towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:  # Don't jitter when very close
            # Normalize direction and apply speed
            self.x += (dx / distance) * self.speed * dt * 60
            self.y += (dy / distance) * self.speed * dt * 60
    
    def defeat(self):
        """Mark monster as defeated"""
        self.is_defeated = True
        self.is_challenging = False
        self.death_animation = 0
    
    def get_challenge_word(self):
        """Get the English word for the challenge"""
        return self.english_word
    
    def check_answer(self, user_input):
        """Check if the user's answer is correct"""
        return self.dictionary.check_translation(self.english_word, user_input)
    
    def get_hint(self):
        """Get a hint for the current word"""
        if self.english_word:
            return self.dictionary.get_hint(self.english_word)
        return "No hint available"
    
    def set_word(self, english_word, latin_word):
        """Set the word challenge for this monster"""
        self.english_word = english_word
        self.latin_word = latin_word
    
    def draw(self, screen):
        """Draw the monster"""
        if self.death_animation > 1:  # Completely faded out
            return
        
        # Calculate position with bobbing
        draw_x = int(self.x)
        draw_y = int(self.y + self.bob_offset)
        
        # Death fade effect
        if self.is_defeated:
            alpha = max(0, 255 - int(self.death_animation * 255))
            # Create surface with alpha for fading
            monster_surface = pygame.Surface((self.width + 20, self.height + 40), pygame.SRCALPHA)
            
            # Draw on the surface instead of directly on screen
            self._draw_monster_body(monster_surface, 10, 20, alpha)
            self._draw_word_bubble(monster_surface, 10, 0, alpha)
            
            screen.blit(monster_surface, (draw_x - 10, draw_y - 20))
        else:
            # Normal drawing
            self._draw_monster_body(screen, draw_x, draw_y, 255)
            self._draw_word_bubble(screen, draw_x, draw_y - 20, 255)
    
    def _draw_monster_body(self, surface, x, y, alpha):
        """Draw the monster body"""
        # Body color with alpha
        body_color = (*self.color, alpha) if alpha < 255 else self.color
        
        # Main body (oval shape)
        body_rect = pygame.Rect(x, y, self.width, self.height)
        
        if alpha < 255:
            # For alpha blending, we need to draw on a surface
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.ellipse(temp_surface, body_color, (0, 0, self.width, self.height))
            pygame.draw.ellipse(temp_surface, Colors.BLACK, (0, 0, self.width, self.height), 2)
            surface.blit(temp_surface, (x, y))
        else:
            pygame.draw.ellipse(surface, body_color, body_rect)
            pygame.draw.ellipse(surface, Colors.BLACK, body_rect, 2)
        
        # Eyes
        eye_size = 4
        left_eye_x = x + self.width // 3
        right_eye_x = x + 2 * self.width // 3
        eye_y = y + self.height // 3
        
        eye_color = (*self.eye_color, alpha) if alpha < 255 else self.eye_color
        
        if alpha < 255:
            temp_surface = pygame.Surface((eye_size * 2, eye_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, eye_color, (eye_size, eye_size), eye_size)
            surface.blit(temp_surface, (left_eye_x - eye_size, eye_y - eye_size))
            surface.blit(temp_surface, (right_eye_x - eye_size, eye_y - eye_size))
        else:
            pygame.draw.circle(surface, eye_color, (left_eye_x, eye_y), eye_size)
            pygame.draw.circle(surface, eye_color, (right_eye_x, eye_y), eye_size)
        
        # Mouth (simple line)
        mouth_y = y + 2 * self.height // 3
        mouth_start = (x + self.width // 4, mouth_y)
        mouth_end = (x + 3 * self.width // 4, mouth_y)
        
        if alpha < 255:
            temp_surface = pygame.Surface((self.width // 2 + 4, 8), pygame.SRCALPHA)
            pygame.draw.line(temp_surface, (*Colors.BLACK, alpha), (2, 4), (self.width // 2 + 2, 4), 2)
            surface.blit(temp_surface, (x + self.width // 4 - 2, mouth_y - 4))
        else:
            pygame.draw.line(surface, Colors.BLACK, mouth_start, mouth_end, 2)
    
    def _draw_word_bubble(self, surface, x, y, alpha):
        """Draw the English word above the monster"""
        if not self.english_word:
            return
        
        font = pygame.font.Font(None, 24)
        text_color = (*Colors.TEXT_BLACK, alpha) if alpha < 255 else Colors.TEXT_BLACK
        
        # Create text surface
        if alpha < 255:
            text_surface = font.render(self.english_word.upper(), True, Colors.TEXT_BLACK)
            text_surface.set_alpha(alpha)
        else:
            text_surface = font.render(self.english_word.upper(), True, text_color)
        
        text_rect = text_surface.get_rect()
        
        # Speech bubble background
        bubble_padding = 8
        bubble_width = text_rect.width + bubble_padding * 2
        bubble_height = text_rect.height + bubble_padding * 2
        bubble_x = x + self.width // 2 - bubble_width // 2
        bubble_y = y - bubble_height - 10
        
        # Draw bubble background
        if alpha < 255:
            bubble_surface = pygame.Surface((bubble_width + 4, bubble_height + 4), pygame.SRCALPHA)
            pygame.draw.rect(bubble_surface, (*Colors.WHITE, alpha), (2, 2, bubble_width, bubble_height), border_radius=5)
            pygame.draw.rect(bubble_surface, (*Colors.BLACK, alpha), (2, 2, bubble_width, bubble_height), 2, border_radius=5)
            surface.blit(bubble_surface, (bubble_x - 2, bubble_y - 2))
        else:
            pygame.draw.rect(surface, Colors.WHITE, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=5)
            pygame.draw.rect(surface, Colors.BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=5)
        
        # Draw text
        text_x = bubble_x + bubble_padding
        text_y = bubble_y + bubble_padding
        surface.blit(text_surface, (text_x, text_y))
        
        # Draw bubble pointer (small triangle)
        pointer_tip = (x + self.width // 2, y - 5)
        pointer_left = (bubble_x + bubble_width // 2 - 5, bubble_y + bubble_height)
        pointer_right = (bubble_x + bubble_width // 2 + 5, bubble_y + bubble_height)
        
        if alpha < 255:
            pointer_surface = pygame.Surface((15, 10), pygame.SRCALPHA)
            pygame.draw.polygon(pointer_surface, (*Colors.WHITE, alpha), [(7, 0), (2, 9), (12, 9)])
            pygame.draw.polygon(pointer_surface, (*Colors.BLACK, alpha), [(7, 0), (2, 9), (12, 9)], 2)
            surface.blit(pointer_surface, (x + self.width // 2 - 7, y - 10))
        else:
            pygame.draw.polygon(surface, Colors.WHITE, [pointer_tip, pointer_left, pointer_right])
            pygame.draw.polygon(surface, Colors.BLACK, [pointer_tip, pointer_left, pointer_right], 2)


class MonsterManager:
    def __init__(self):
        self.monsters = []
        self.spawn_timer = 0
        self.spawn_interval = 8.0  # seconds between spawns
        self.max_monsters = GameConfig.MAX_MONSTERS
        self.level = 1
        self.monsters_defeated = 0
        self.textbook_manager = None
        self.vocabulary_list = []
        self.used_words = set()
        
    def update(self, player, dt):
        """Update all monsters"""
        challenge_request = None
        
        # Update spawn timer
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and len(self.monsters) < self.max_monsters:
            self.spawn_monster(player)
            self.spawn_timer = self.spawn_interval
        
        # Update existing monsters
        monsters_to_remove = []
        for monster in self.monsters:
            result = monster.update(player, dt)
            
            if result == "challenge":
                challenge_request = monster
            
            # Remove fully faded monsters
            if monster.is_defeated and monster.death_animation > 1:
                monsters_to_remove.append(monster)
                self.monsters_defeated += 1
        
        # Remove defeated monsters
        for monster in monsters_to_remove:
            self.monsters.remove(monster)
        
        # Level progression
        if self.monsters_defeated > 0 and self.monsters_defeated % 10 == 0:
            self.level += 1
            self.spawn_interval = max(3.0, self.spawn_interval * 0.9)  # Spawn faster
        
        return challenge_request
    
    def set_textbook_mode(self, textbook_manager):
        """Set the monster manager to use textbook vocabulary"""
        self.textbook_manager = textbook_manager
        vocabulary = textbook_manager.get_current_vocabulary()
        self.vocabulary_list = list(vocabulary.items())  # List of (english, latin) tuples
        self.used_words.clear()
    
    def get_next_word(self):
        """Get the next word from the lesson vocabulary"""
        if not self.vocabulary_list:
            return "word", "verbum"  # Fallback
        
        # Filter unused words
        available_words = [(eng, lat) for eng, lat in self.vocabulary_list 
                          if eng not in self.used_words]
        
        # If all words used, reset
        if not available_words:
            self.used_words.clear()
            available_words = self.vocabulary_list
        
        # Select random word
        import random
        english_word, latin_word = random.choice(available_words)
        self.used_words.add(english_word)
        
        return english_word, latin_word
    
    def spawn_monster(self, player):
        """Spawn a new monster away from the player"""
        # Choose difficulty based on level
        if self.level <= 3:
            difficulty = "easy"
        elif self.level <= 6:
            difficulty = random.choice(["easy", "medium"])
        else:
            difficulty = random.choice(["easy", "medium", "hard"])
        
        # Find spawn position away from player
        attempts = 0
        while attempts < 10:
            x = random.randint(50, GameConfig.SCREEN_WIDTH - 50)
            y = random.randint(100, GameConfig.SCREEN_HEIGHT - 150)
            
            # Check distance from player
            dx = x - player.x
            dy = y - player.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > GameConfig.MONSTER_SPAWN_DISTANCE:
                monster = Monster(x, y, difficulty)
                
                # Set word from textbook if available
                if self.textbook_manager:
                    english_word, latin_word = self.get_next_word()
                    monster.set_word(english_word, latin_word)
                else:
                    # Fallback to dictionary
                    english_word, latin_word = monster.dictionary.get_word_by_difficulty(difficulty)
                    monster.set_word(english_word, latin_word)
                
                self.monsters.append(monster)
                break
            
            attempts += 1
    
    def get_active_monsters(self):
        """Get all active (non-defeated) monsters"""
        return [m for m in self.monsters if not m.is_defeated]
    
    def draw(self, screen):
        """Draw all monsters"""
        for monster in self.monsters:
            monster.draw(screen)
    
    def clear_all(self):
        """Clear all monsters"""
        self.monsters.clear()
        self.spawn_timer = self.spawn_interval
