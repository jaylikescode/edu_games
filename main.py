import pygame
import sys
import time
from config import GameConfig, Colors, GameState
from player import Player
from monster import MonsterManager
from latin_dictionary import LatinDictionary
from textbooks import TextbookManager
from ui_components import Button, ScrollableList, TextDisplay, MenuManager

class WordChallenge:
    def __init__(self, monster):
        self.monster = monster
        self.english_word = monster.get_challenge_word()
        self.user_input = ""
        self.time_left = GameConfig.TYPING_TIME_LIMIT
        self.result = None
        self.feedback_message = ""
        self.show_hint = False
        self.hint_text = ""
        
    def update(self, dt):
        """Update challenge timer"""
        if self.result is None:  # Still active
            self.time_left -= dt
            if self.time_left <= 0:
                self.result = False
                self.feedback_message = f"Time's up! Correct answer: {self.monster.latin_word}"
    
    def handle_input(self, event):
        """Handle keyboard input for the challenge"""
        if self.result is not None:  # Challenge completed
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Submit answer
                correct, message = self.monster.check_answer(self.user_input)
                self.result = correct
                self.feedback_message = message
            elif event.key == pygame.K_BACKSPACE:
                # Delete character
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_TAB:
                # Show hint
                self.show_hint = True
                self.hint_text = self.monster.get_hint()
            elif event.unicode.isprintable() and len(self.user_input) < 20:
                # Add character
                self.user_input += event.unicode.lower()


class PlanetLatinGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Planet Latin - Educational Adventure")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.running = True
        self.dt = 0
        
        # Game objects
        self.player = Player(GameConfig.PLAYER_START_X, GameConfig.PLAYER_START_Y)
        self.monster_manager = MonsterManager()
        self.dictionary = LatinDictionary()
        self.textbook_manager = TextbookManager()
        
        # Fonts (initialize before UI)
        self.font_large = pygame.font.Font(None, GameConfig.FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, GameConfig.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, GameConfig.FONT_SIZE_SMALL)
        
        # UI Management
        self.menu_manager = MenuManager()
        self.setup_main_menu()
        
        # Word challenge
        self.current_challenge = None
        self.challenge_complete_timer = 0
        
        # Background
        self.background_stars = self._generate_stars()
        
        # Selection state
        self.selected_textbook = None
        self.selected_lesson = 1
    
    def _generate_stars(self):
        """Generate background stars for Planet Latin atmosphere"""
        import random
        stars = []
        for _ in range(100):
            x = random.randint(0, GameConfig.SCREEN_WIDTH)
            y = random.randint(0, GameConfig.SCREEN_HEIGHT // 2)  # Upper half only
            brightness = random.randint(100, 255)
            size = random.randint(1, 2)
            stars.append((x, y, brightness, size))
        return stars
    
    def setup_main_menu(self):
        """Setup the main menu UI"""
        self.menu_manager.clear()
        
        # Title and subtitle are drawn separately
        
        # Menu buttons
        button_width = 300
        button_height = 50
        button_x = (GameConfig.SCREEN_WIDTH - button_width) // 2
        start_y = 300
        
        # Start Game button
        start_button = Button(button_x, start_y, button_width, button_height,
                            "Start Adventure", self.font_medium,
                            Colors.EASY_LEVEL, Colors.TEXT_BLACK)
        self.menu_manager.add_component(start_button)
        
        # Instructions button
        instructions_button = Button(button_x, start_y + 60, button_width, button_height,
                                   "Instructions", self.font_medium,
                                   Colors.MEDIUM_LEVEL, Colors.TEXT_BLACK)
        self.menu_manager.add_component(instructions_button)
        
        # Exit button
        exit_button = Button(button_x, start_y + 120, button_width, button_height,
                           "Exit", self.font_medium,
                           Colors.HARD_LEVEL, Colors.TEXT_BLACK)
        self.menu_manager.add_component(exit_button)
    
    def setup_book_selection_menu(self):
        """Setup the book selection UI"""
        self.menu_manager.clear()
        
        # Title is drawn separately
        
        # Book list
        textbooks = self.textbook_manager.get_all_textbooks()
        book_items = []
        for book_id, textbook in textbooks.items():
            book_items.append({
                'id': book_id,
                'name': textbook.name,
                'description': textbook.description
            })
        
        book_list = ScrollableList(100, 150, 400, 300, book_items, self.font_small)
        self.menu_manager.add_component(book_list)
        
        # Description panel
        description_panel = TextDisplay(520, 150, 350, 200, self.font_small,
                                      Colors.TEXT_WHITE, Colors.UI_BACKGROUND, Colors.WHITE)
        description_panel.set_text("Select a textbook to see its description.")
        self.menu_manager.add_component(description_panel)
        
        # Buttons
        button_width = 150
        button_height = 40
        
        # Continue button
        continue_button = Button(520, 370, button_width, button_height,
                               "Continue", self.font_medium,
                               Colors.EASY_LEVEL, Colors.TEXT_BLACK)
        self.menu_manager.add_component(continue_button)
        
        # Back button
        back_button = Button(680, 370, button_width, button_height,
                           "Back", self.font_medium,
                           Colors.HARD_LEVEL, Colors.TEXT_BLACK)
        self.menu_manager.add_component(back_button)
    
    def setup_lesson_selection_menu(self):
        """Setup the lesson selection UI"""
        self.menu_manager.clear()
        
        if not self.selected_textbook:
            return
        
        textbook = self.textbook_manager.get_textbook(self.selected_textbook)
        available_lessons = textbook.get_available_lessons()
        
        # Create lesson items
        lesson_items = []
        for lesson_num in available_lessons:
            lesson_info = textbook.get_lesson_info(lesson_num)
            lesson_items.append({
                'number': lesson_num,
                'name': f"Lesson {lesson_num}: {lesson_info['title']}",
                'grammar': lesson_info['grammar_focus'],
                'vocab_count': len(lesson_info['vocabulary'])
            })
        
        # Lesson list
        lesson_list = ScrollableList(100, 150, 400, 300, lesson_items, self.font_small)
        self.menu_manager.add_component(lesson_list)
        
        # Lesson details panel
        details_panel = TextDisplay(520, 150, 350, 250, self.font_small,
                                  Colors.TEXT_WHITE, Colors.UI_BACKGROUND, Colors.WHITE)
        details_panel.set_text("Select a lesson to see its details.")
        self.menu_manager.add_component(details_panel)
        
        # Buttons
        button_width = 150
        button_height = 40
        
        # Start Lesson button
        start_button = Button(520, 420, button_width, button_height,
                            "Start Lesson", self.font_medium,
                            Colors.EASY_LEVEL, Colors.TEXT_BLACK)
        self.menu_manager.add_component(start_button)
        
        # Back button
        back_button = Button(680, 420, button_width, button_height,
                            "Back", self.font_medium,
                           Colors.HARD_LEVEL, Colors.TEXT_BLACK)
        self.menu_manager.add_component(back_button)
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle UI events first
            if self.state in [GameState.MENU, GameState.BOOK_SELECTION, GameState.LESSON_SELECTION]:
                ui_results = self.menu_manager.handle_event(event)
                self.handle_menu_events(ui_results)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.WORD_CHALLENGE:
                        # Cancel challenge (monster wins)
                        self.current_challenge = None
                        self.state = GameState.PLAYING
                    elif self.state == GameState.BOOK_SELECTION:
                        self.state = GameState.MENU
                        self.setup_main_menu()
                    elif self.state == GameState.LESSON_SELECTION:
                        self.state = GameState.BOOK_SELECTION
                        self.setup_book_selection_menu()
                    else:
                        self.running = False
                
                elif self.state == GameState.INSTRUCTIONS:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.state = GameState.MENU
                        self.setup_main_menu()
                
                elif self.state == GameState.WORD_CHALLENGE:
                    self.current_challenge.handle_input(event)
                
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_r:
                        self.restart_game()
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_m:
                        self.state = GameState.MENU
    
    def update(self):
        """Update game logic"""
        self.dt = self.clock.get_time() / 1000.0
        
        if self.state == GameState.PLAYING:
            self.update_playing()
        elif self.state == GameState.WORD_CHALLENGE:
            self.update_word_challenge()
    
    def update_playing(self):
        """Update main gameplay"""
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys, self.dt)
        
        # Update monsters
        challenge_monster = self.monster_manager.update(self.player, self.dt)
        
        # Start word challenge if monster requests it
        if challenge_monster and self.current_challenge is None:
            self.current_challenge = WordChallenge(challenge_monster)
            self.state = GameState.WORD_CHALLENGE
    
    def update_word_challenge(self):
        """Update word challenge state"""
        if self.current_challenge:
            self.current_challenge.update(self.dt)
            
            # Check if challenge is complete
            if self.current_challenge.result is not None:
                self.challenge_complete_timer += self.dt
                
                # Process result after showing feedback
                if self.challenge_complete_timer > 2.0:
                    if self.current_challenge.result:
                        # Player won - defeat monster
                        self.current_challenge.monster.defeat()
                        self.player.answer_question(True)
                    else:
                        # Player lost - record failure
                        self.player.answer_question(False)
                    
                    # Return to playing
                    self.current_challenge = None
                    self.challenge_complete_timer = 0
                    self.state = GameState.PLAYING
    
    def draw(self):
        """Draw everything"""
        # Clear screen with background
        self.screen.fill(Colors.BACKGROUND)
        
        # Draw stars
        for star in self.background_stars:
            x, y, brightness, size = star
            star_color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, star_color, (x, y), size)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.BOOK_SELECTION:
            self.draw_book_selection()
        elif self.state == GameState.LESSON_SELECTION:
            self.draw_lesson_selection()
        elif self.state == GameState.INSTRUCTIONS:
            self.draw_instructions()
        elif self.state == GameState.PLAYING:
            self.draw_playing()
        elif self.state == GameState.WORD_CHALLENGE:
            self.draw_word_challenge()
        elif self.state == GameState.PAUSED:
            self.draw_playing()  # Draw game underneath
            self.draw_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_book_selection(self):
        """Draw book selection screen"""
        # Title
        title_text = self.font_large.render("SELECT TEXTBOOK", True, Colors.TEXT_WHITE)
        title_rect = title_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Choose your Latin textbook", True, Colors.LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 120))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw UI components
        self.menu_manager.draw(self.screen)
    
    def draw_lesson_selection(self):
        """Draw lesson selection screen"""
        # Title
        if self.selected_textbook:
            textbook = self.textbook_manager.get_textbook(self.selected_textbook)
            title_text = self.font_large.render(textbook.name.upper(), True, Colors.TEXT_WHITE)
        else:
            title_text = self.font_large.render("SELECT LESSON", True, Colors.TEXT_WHITE)
        title_rect = title_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Choose your lesson", True, Colors.LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 120))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw UI components
        self.menu_manager.draw(self.screen)
    
    def draw_menu(self):
        """Draw main menu"""
        # Title
        title_text = self.font_large.render("PLANET LATIN", True, Colors.TEXT_WHITE)
        title_rect = title_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 150))
        
        # Add glow effect to title
        for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            glow_rect = title_rect.copy()
            glow_rect.x += offset[0]
            glow_rect.y += offset[1]
            glow_text = self.font_large.render("PLANET LATIN", True, Colors.GOLD)
            self.screen.blit(glow_text, glow_rect)
        
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Educational Latin Adventure", True, Colors.TEXT_WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw menu buttons
        self.menu_manager.draw(self.screen)
        
        # Game description
        description = [
            "Choose your textbook and lesson to start learning!",
            "Defeat monsters by translating English to Latin",
            "Perfect companion for Latin students"
        ]
        
        desc_y = 500
        for i, line in enumerate(description):
            desc_text = self.font_small.render(line, True, Colors.LIGHT_GRAY)
            desc_rect = desc_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, desc_y + i * 25))
            self.screen.blit(desc_text, desc_rect)
    
    def draw_instructions(self):
        """Draw instructions screen"""
        # Title
        title_text = self.font_large.render("HOW TO PLAY", True, Colors.TEXT_WHITE)
        title_rect = title_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "MOVEMENT:",
            "• WASD or Arrow Keys - Move around Planet Latin",
            "",
            "COMBAT:",
            "• Approach monsters to start word challenges",
            "• Type the Latin translation of the English word",
            "• Press ENTER to submit your answer",
            "• Press TAB for a hint (first letter + length)",
            "",
            "DIFFICULTY LEVELS:",
            "• Green monsters - Easy words (basic vocabulary)",
            "• Yellow monsters - Medium words (intermediate)",
            "• Red monsters - Hard words (advanced concepts)",
            "",
            "PROGRESSION:",
            "• Gain XP for correct answers",
            "• Level up to move faster and face harder challenges",
            "• Track your accuracy and words learned",
            "",
            "Press SPACE to return to menu"
        ]
        
        y_pos = 140
        for instruction in instructions:
            if instruction.startswith("•"):
                color = Colors.LIGHT_GRAY
                font = self.font_small
            elif instruction.isupper() and instruction.endswith(":"):
                color = Colors.GOLD
                font = self.font_medium
            elif instruction == "":
                y_pos += 10
                continue
            else:
                color = Colors.TEXT_WHITE
                font = self.font_small
            
            inst_text = font.render(instruction, True, color)
            self.screen.blit(inst_text, (50, y_pos))
            y_pos += 25
    
    def draw_playing(self):
        """Draw main gameplay"""
        # Draw ground
        ground_y = GameConfig.SCREEN_HEIGHT - 100
        pygame.draw.rect(self.screen, Colors.GROUND, 
                        (0, ground_y, GameConfig.SCREEN_WIDTH, 100))
        pygame.draw.rect(self.screen, Colors.GRASS, 
                        (0, ground_y, GameConfig.SCREEN_WIDTH, 20))
        
        # Draw game objects
        self.monster_manager.draw(self.screen)
        self.player.draw(self.screen)
        
        # Draw UI
        self.player.draw_stats(self.screen)
        
        # Draw monster counter
        active_monsters = len(self.monster_manager.get_active_monsters())
        monster_text = self.font_small.render(f"Monsters: {active_monsters}", True, Colors.TEXT_WHITE)
        self.screen.blit(monster_text, (GameConfig.SCREEN_WIDTH - 150, 10))
        
        # Draw level indicator
        level_text = self.font_small.render(f"Monster Level: {self.monster_manager.level}", True, Colors.TEXT_WHITE)
        self.screen.blit(level_text, (GameConfig.SCREEN_WIDTH - 150, 30))
    
    def draw_word_challenge(self):
        """Draw word challenge interface"""
        # Draw game underneath (dimmed)
        self.draw_playing()
        
        # Dim overlay
        overlay = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if not self.current_challenge:
            return
        
        # Challenge panel
        panel_width = 500
        panel_height = 300
        panel_x = (GameConfig.SCREEN_WIDTH - panel_width) // 2
        panel_y = (GameConfig.SCREEN_HEIGHT - panel_height) // 2
        
        # Panel background
        pygame.draw.rect(self.screen, Colors.UI_BACKGROUND, 
                        (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(self.screen, Colors.WHITE, 
                        (panel_x, panel_y, panel_width, panel_height), 3, border_radius=10)
        
        # Challenge content
        y_offset = panel_y + 20
        
        # Title
        title_text = self.font_large.render("WORD CHALLENGE", True, Colors.TEXT_WHITE)
        title_rect = title_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset + 20))
        self.screen.blit(title_text, title_rect)
        y_offset += 60
        
        # English word
        word_text = self.font_large.render(f'"{self.current_challenge.english_word.upper()}"', True, Colors.GOLD)
        word_rect = word_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset + 20))
        self.screen.blit(word_text, word_rect)
        y_offset += 60
        
        # Instruction
        if self.current_challenge.result is None:
            instruction = "Type the Latin translation:"
            instruction_color = Colors.TEXT_WHITE
        else:
            instruction = self.current_challenge.feedback_message
            instruction_color = Colors.TEXT_SUCCESS if self.current_challenge.result else Colors.TEXT_ERROR
        
        inst_text = self.font_medium.render(instruction, True, instruction_color)
        inst_rect = inst_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset + 15))
        self.screen.blit(inst_text, inst_rect)
        y_offset += 50
        
        # Input box (only if challenge is active)
        if self.current_challenge.result is None:
            input_box_x = (GameConfig.SCREEN_WIDTH - GameConfig.INPUT_BOX_WIDTH) // 2
            input_box_y = y_offset
            
            # Input box background
            box_color = Colors.INPUT_BOX_ACTIVE if len(self.current_challenge.user_input) > 0 else Colors.INPUT_BOX
            pygame.draw.rect(self.screen, box_color, 
                           (input_box_x, input_box_y, GameConfig.INPUT_BOX_WIDTH, GameConfig.INPUT_BOX_HEIGHT))
            pygame.draw.rect(self.screen, Colors.BLACK, 
                           (input_box_x, input_box_y, GameConfig.INPUT_BOX_WIDTH, GameConfig.INPUT_BOX_HEIGHT), 2)
            
            # Input text
            input_text = self.font_medium.render(self.current_challenge.user_input, True, Colors.INPUT_TEXT)
            text_y = input_box_y + (GameConfig.INPUT_BOX_HEIGHT - input_text.get_height()) // 2
            self.screen.blit(input_text, (input_box_x + 10, text_y))
            
            # Cursor
            if int(time.time() * 2) % 2:  # Blinking cursor
                cursor_x = input_box_x + 10 + input_text.get_width()
                pygame.draw.line(self.screen, Colors.INPUT_TEXT, 
                               (cursor_x, text_y), (cursor_x, text_y + input_text.get_height()), 2)
            
            y_offset += 60
            
            # Timer
            time_color = Colors.TEXT_ERROR if self.current_challenge.time_left < 5 else Colors.TEXT_WHITE
            timer_text = self.font_medium.render(f"Time: {self.current_challenge.time_left:.1f}s", True, time_color)
            timer_rect = timer_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset + 15))
            self.screen.blit(timer_text, timer_rect)
            
            # Hint
            if self.current_challenge.show_hint:
                hint_text = self.font_small.render(f"Hint: {self.current_challenge.hint_text}", True, Colors.TEXT_WARNING)
                hint_rect = hint_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset + 40))
                self.screen.blit(hint_text, hint_rect)
            else:
                hint_instruction = self.font_small.render("Press TAB for hint", True, Colors.LIGHT_GRAY)
                hint_rect = hint_instruction.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset + 40))
                self.screen.blit(hint_instruction, hint_rect)
    
    def draw_pause_overlay(self):
        """Draw pause screen overlay"""
        overlay = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, Colors.TEXT_WHITE)
        pause_rect = pause_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instructions = [
            "ESC - Resume",
            "R - Restart",
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_medium.render(instruction, True, Colors.TEXT_WHITE)
            inst_rect = inst_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT // 2 + i * 30))
            self.screen.blit(inst_text, inst_rect)
    
    def start_game(self):
        """Start a new game"""
        self.state = GameState.BOOK_SELECTION
        self.setup_book_selection_menu()
    
    def start_lesson(self):
        """Start the selected lesson"""
        # Set up the textbook manager with selected book and lesson
        self.textbook_manager.set_current_textbook(self.selected_textbook, self.selected_lesson)
        
        # Update the monster manager to use textbook vocabulary
        self.monster_manager = MonsterManager()
        self.monster_manager.set_textbook_mode(self.textbook_manager)
        
        # Start the game
        self.player = Player(GameConfig.PLAYER_START_X, GameConfig.PLAYER_START_Y)
        self.current_challenge = None
        self.state = GameState.PLAYING
    
    def restart_game(self):
        """Restart the current game"""
        self.state = GameState.MENU
        self.setup_main_menu()
    
    def handle_menu_events(self, ui_results):
        """Handle UI component events"""
        for component, result in ui_results:
            if self.state == GameState.MENU:
                self.handle_main_menu_events(component, result)
            elif self.state == GameState.BOOK_SELECTION:
                self.handle_book_selection_events(component, result)
            elif self.state == GameState.LESSON_SELECTION:
                self.handle_lesson_selection_events(component, result)
    
    def handle_main_menu_events(self, component, result):
        """Handle main menu events"""
        if isinstance(component, Button):
            if component.text == "Start Adventure":
                self.state = GameState.BOOK_SELECTION
                self.setup_book_selection_menu()
            elif component.text == "Instructions":
                self.state = GameState.INSTRUCTIONS
            elif component.text == "Exit":
                self.running = False
    
    def handle_book_selection_events(self, component, result):
        """Handle book selection events"""
        if isinstance(component, ScrollableList):
            # Book selected from list
            selected_book = component.get_selected_item()
            if selected_book:
                # Update description panel
                description_panel = self.menu_manager.components[1]  # Second component
                description_panel.set_text(selected_book['description'])
                self.selected_textbook = selected_book['id']
        
        elif isinstance(component, Button):
            if component.text == "Continue" and self.selected_textbook:
                self.state = GameState.LESSON_SELECTION
                self.setup_lesson_selection_menu()
            elif component.text == "Back":
                self.state = GameState.MENU
                self.setup_main_menu()
    
    def handle_lesson_selection_events(self, component, result):
        """Handle lesson selection events"""
        if isinstance(component, ScrollableList):
            # Lesson selected from list
            selected_lesson = component.get_selected_item()
            if selected_lesson:
                # Update details panel
                details_panel = self.menu_manager.components[1]  # Second component
                details_text = f"Grammar Focus: {selected_lesson['grammar']}\n\n"
                details_text += f"Vocabulary Words: {selected_lesson['vocab_count']}\n\n"
                details_text += "This lesson will test your knowledge of the vocabulary from this chapter."
                details_panel.set_text(details_text)
                self.selected_lesson = selected_lesson['number']
        
        elif isinstance(component, Button):
            if component.text == "Start Lesson" and self.selected_textbook and self.selected_lesson:
                self.start_lesson()
            elif component.text == "Back":
                self.state = GameState.BOOK_SELECTION
                self.setup_book_selection_menu()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(GameConfig.FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = PlanetLatinGame()
    game.run()
