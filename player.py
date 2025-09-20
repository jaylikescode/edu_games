import pygame
import math
from config import GameConfig, Colors

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width, self.height = GameConfig.PLAYER_SIZE
        self.speed = GameConfig.PLAYER_SPEED
        
        # Animation
        self.animation_time = 0
        self.walking = False
        self.facing_right = True
        
        # Stats
        self.level = 1
        self.experience = 0
        self.experience_to_next = 100
        self.words_learned = 0
        self.accuracy = 100.0
        self.total_attempts = 0
        self.correct_attempts = 0
        
        # Visual effects
        self.level_up_effect = 0
        self.word_learned_effect = 0
        
    def update(self, keys, dt):
        """Update player state"""
        self.animation_time += dt
        self.walking = False
        
        # Movement
        old_x = self.x
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * dt * 60
            self.walking = True
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * dt * 60
            self.walking = True
            self.facing_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed * dt * 60
            self.walking = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed * dt * 60
            self.walking = True
        
        # Keep player on screen
        self.x = max(15, min(GameConfig.SCREEN_WIDTH - self.width - 15, self.x))
        self.y = max(50, min(GameConfig.SCREEN_HEIGHT - self.height - 50, self.y))
        
        # Update visual effects
        if self.level_up_effect > 0:
            self.level_up_effect -= dt
        if self.word_learned_effect > 0:
            self.word_learned_effect -= dt
    
    def answer_question(self, correct):
        """Record the result of answering a question"""
        self.total_attempts += 1
        
        if correct:
            self.correct_attempts += 1
            self.words_learned += 1
            self.experience += 10
            self.word_learned_effect = 1.0  # Visual effect duration
            
            # Check for level up
            if self.experience >= self.experience_to_next:
                self.level_up()
        
        # Update accuracy
        self.accuracy = (self.correct_attempts / self.total_attempts) * 100
    
    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.experience -= self.experience_to_next
        self.experience_to_next = int(self.experience_to_next * 1.2)  # Increase requirement
        self.level_up_effect = 2.0  # Visual effect duration
        
        # Increase speed slightly
        self.speed += 0.2
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw the player"""
        # Calculate animation offset for walking
        walk_offset = 0
        if self.walking:
            walk_offset = math.sin(self.animation_time * 8) * 2
        
        draw_x = int(self.x)
        draw_y = int(self.y + walk_offset)
        
        # Player body color with effects
        body_color = Colors.PLAYER_BODY
        if self.level_up_effect > 0:
            # Golden glow for level up
            glow_intensity = int(100 * self.level_up_effect)
            body_color = (min(255, Colors.PLAYER_BODY[0] + glow_intensity),
                         min(255, Colors.PLAYER_BODY[1] + glow_intensity), 
                         min(255, Colors.PLAYER_BODY[2] + glow_intensity))
        elif self.word_learned_effect > 0:
            # Green glow for correct answer
            glow_intensity = int(50 * self.word_learned_effect)
            body_color = (Colors.PLAYER_BODY[0],
                         min(255, Colors.PLAYER_BODY[1] + glow_intensity),
                         Colors.PLAYER_BODY[2])
        
        # Draw player body (simple humanoid figure)
        # Head
        head_radius = 8
        head_x = draw_x + self.width // 2
        head_y = draw_y + head_radius
        pygame.draw.circle(screen, body_color, (head_x, head_y), head_radius)
        pygame.draw.circle(screen, Colors.PLAYER_OUTLINE, (head_x, head_y), head_radius, 2)
        
        # Body
        body_rect = pygame.Rect(draw_x + 5, draw_y + head_radius * 2 - 5, 
                               self.width - 10, self.height - head_radius * 2 - 5)
        pygame.draw.rect(screen, body_color, body_rect)
        pygame.draw.rect(screen, Colors.PLAYER_OUTLINE, body_rect, 2)
        
        # Arms
        arm_y = draw_y + head_radius * 2 + 5
        left_arm_x = draw_x + 2
        right_arm_x = draw_x + self.width - 2
        arm_swing = math.sin(self.animation_time * 6) * 3 if self.walking else 0
        
        pygame.draw.line(screen, body_color, 
                        (left_arm_x, arm_y), 
                        (left_arm_x - 8, arm_y + 15 + arm_swing), 3)
        pygame.draw.line(screen, body_color, 
                        (right_arm_x, arm_y), 
                        (right_arm_x + 8, arm_y + 15 - arm_swing), 3)
        
        # Legs
        leg_y = draw_y + self.height - 5
        left_leg_x = draw_x + 8
        right_leg_x = draw_x + self.width - 8
        leg_swing = math.sin(self.animation_time * 8) * 5 if self.walking else 0
        
        pygame.draw.line(screen, body_color,
                        (left_leg_x, leg_y),
                        (left_leg_x - 3 + leg_swing, leg_y + 15), 4)
        pygame.draw.line(screen, body_color,
                        (right_leg_x, leg_y),
                        (right_leg_x + 3 - leg_swing, leg_y + 15), 4)
        
        # Eyes
        eye_size = 2
        if self.facing_right:
            eye_x = head_x + 2
        else:
            eye_x = head_x - 2
        eye_y = head_y - 2
        pygame.draw.circle(screen, Colors.BLACK, (eye_x, eye_y), eye_size)
        
        # Level up effect
        if self.level_up_effect > 0:
            effect_radius = int(40 * (2.0 - self.level_up_effect))
            effect_alpha = int(100 * self.level_up_effect)
            
            # Create effect surface
            effect_surface = pygame.Surface((effect_radius * 2, effect_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(effect_surface, (*Colors.GOLD, effect_alpha), 
                             (effect_radius, effect_radius), effect_radius, 3)
            
            # Draw centered on player
            effect_x = head_x - effect_radius
            effect_y = head_y - effect_radius
            screen.blit(effect_surface, (effect_x, effect_y))
    
    def draw_stats(self, screen):
        """Draw player statistics"""
        font_large = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 18)
        
        # Stats panel background
        panel_x = 10
        panel_y = 10
        panel_width = 250
        panel_height = 120
        
        # Semi-transparent background
        stats_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(stats_surface, Colors.UI_BACKGROUND, (0, 0, panel_width, panel_height), border_radius=5)
        screen.blit(stats_surface, (panel_x, panel_y))
        
        # Border
        pygame.draw.rect(screen, Colors.WHITE, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=5)
        
        # Stats text
        y_offset = panel_y + 10
        
        # Level
        level_text = font_large.render(f"Level: {self.level}", True, Colors.TEXT_WHITE)
        screen.blit(level_text, (panel_x + 10, y_offset))
        y_offset += 25
        
        # Experience bar
        exp_text = font_small.render(f"XP: {self.experience}/{self.experience_to_next}", True, Colors.TEXT_WHITE)
        screen.blit(exp_text, (panel_x + 10, y_offset))
        
        # Experience bar
        bar_x = panel_x + 10
        bar_y = y_offset + 18
        bar_width = panel_width - 20
        bar_height = 8
        
        # Background bar
        pygame.draw.rect(screen, Colors.DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Experience fill
        exp_ratio = self.experience / self.experience_to_next
        exp_width = int(bar_width * exp_ratio)
        pygame.draw.rect(screen, Colors.EASY_LEVEL, (bar_x, bar_y, exp_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, Colors.WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        y_offset += 30
        
        # Words learned
        words_text = font_small.render(f"Words Learned: {self.words_learned}", True, Colors.TEXT_WHITE)
        screen.blit(words_text, (panel_x + 10, y_offset))
        y_offset += 18
        
        # Accuracy
        accuracy_color = Colors.TEXT_SUCCESS if self.accuracy >= 80 else Colors.TEXT_WARNING if self.accuracy >= 60 else Colors.TEXT_ERROR
        accuracy_text = font_small.render(f"Accuracy: {self.accuracy:.1f}%", True, accuracy_color)
        screen.blit(accuracy_text, (panel_x + 10, y_offset))
        
        # Level up notification
        if self.level_up_effect > 0:
            notification_font = pygame.font.Font(None, 36)
            level_up_text = notification_font.render("LEVEL UP!", True, Colors.GOLD)
            text_rect = level_up_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 100))
            
            # Add glow effect
            for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                glow_rect = text_rect.copy()
                glow_rect.x += offset[0]
                glow_rect.y += offset[1]
                glow_text = notification_font.render("LEVEL UP!", True, Colors.YELLOW)
                screen.blit(glow_text, glow_rect)
            
            screen.blit(level_up_text, text_rect)
