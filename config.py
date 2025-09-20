# Planet Latin - Game Configuration

class GameConfig:
    # Screen settings
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    FPS = 60
    
    # Player settings
    PLAYER_SPEED = 4
    PLAYER_SIZE = (30, 40)
    PLAYER_START_X = 100
    PLAYER_START_Y = 300
    
    # Monster settings
    MONSTER_SIZE = (40, 50)
    MONSTER_SPEED = 1.5
    MONSTER_SPAWN_DISTANCE = 200  # Distance from player to spawn
    MAX_MONSTERS = 5
    
    # Word challenge settings
    TYPING_TIME_LIMIT = 15  # seconds to type the answer
    EASY_WORDS_PER_LEVEL = 5
    MEDIUM_WORDS_PER_LEVEL = 7
    HARD_WORDS_PER_LEVEL = 10
    
    # UI settings
    FONT_SIZE_LARGE = 36
    FONT_SIZE_MEDIUM = 24
    FONT_SIZE_SMALL = 18
    INPUT_BOX_WIDTH = 300
    INPUT_BOX_HEIGHT = 40

class Colors:
    # Basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)
    GOLD = (255, 215, 0)
    YELLOW = (255, 255, 0)
    
    # Game colors
    BACKGROUND = (50, 80, 120)  # Deep blue sky
    GROUND = (139, 69, 19)      # Brown earth
    GRASS = (34, 139, 34)       # Forest green
    
    # UI colors
    UI_BACKGROUND = (40, 40, 40)  # Dark gray background
    INPUT_BOX = (255, 255, 255)
    INPUT_BOX_ACTIVE = (255, 255, 200)
    INPUT_TEXT = (0, 0, 0)
    
    # Player colors
    PLAYER_BODY = (0, 100, 200)  # Blue tunic
    PLAYER_OUTLINE = (0, 50, 150)
    
    # Monster colors
    MONSTER_EASY = (100, 200, 100)    # Green - easy
    MONSTER_MEDIUM = (200, 200, 100)  # Yellow - medium  
    MONSTER_HARD = (200, 100, 100)    # Red - hard
    MONSTER_EYES = (255, 0, 0)        # Red eyes
    
    # Text colors
    TEXT_WHITE = (255, 255, 255)
    TEXT_BLACK = (0, 0, 0)
    TEXT_SUCCESS = (0, 255, 0)
    TEXT_ERROR = (255, 0, 0)
    TEXT_WARNING = (255, 165, 0)
    
    # Level colors
    EASY_LEVEL = (144, 238, 144)    # Light green
    MEDIUM_LEVEL = (255, 255, 144)  # Light yellow
    HARD_LEVEL = (255, 182, 193)    # Light pink

class GameState:
    MENU = "menu"
    BOOK_SELECTION = "book_selection"
    LESSON_SELECTION = "lesson_selection"
    PLAYING = "playing"
    WORD_CHALLENGE = "word_challenge"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"
    INSTRUCTIONS = "instructions"
