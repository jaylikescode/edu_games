# Latin Dictionary - English to Latin word mappings
import random

class LatinDictionary:
    def __init__(self):
        # Comprehensive English-to-Latin word database
        # Organized by difficulty level
        
        self.easy_words = {
            # Basic nouns and common words
            "water": "aqua",
            "fire": "ignis", 
            "earth": "terra",
            "air": "aer",
            "sun": "sol",
            }
        
        self.medium_words = {
            # More complex vocabulary
            "wisdom": "sapientia",
            "knowledge": "scientia",
            "truth": "veritas",
            "justice": "iustitia",
            "courage": "fortitudo",
            "honor": "honor",
            "glory": "gloria",
            "victory": "victoria",
            "defeat": "clades",
            "battle": "proelium",
            "soldier": "miles",
            "weapon": "telum",
            "shield": "scutum",
            "sword": "gladius",
            "arrow": "sagitta",
            "city": "urbs",
            "country": "patria",
            "citizen": "civis",
            "people": "populus",
            "nation": "gens",
            "law": "lex",
            "right": "ius",
            "duty": "officium",
            "work": "opus",
            "art": "ars",
            "skill": "peritia",
            "master": "magister",
            "student": "discipulus",
            "school": "schola",
            "letter": "epistula",
            "language": "lingua",
            "speech": "oratio",
            "silence": "silentium",
            "sound": "sonus",
            "music": "musica",
            "song": "cantus",
            "dance": "saltus",
            "game": "ludus",
            "sport": "certamen",
            "prize": "praemium",
            "gift": "donum",
            "money": "pecunia",
            "wealth": "divitiae",
            "poverty": "paupertas",
            "health": "salus",
            "sickness": "morbus",
            "medicine": "medicina",
            "doctor": "medicus",
            "temple": "templum",
            "altar": "ara",
            "prayer": "oratio",
            "sacrifice": "sacrificium"
        }
        
        self.hard_words = {
            # Advanced vocabulary and concepts
            "philosophy": "philosophia",
            "mathematics": "mathematica",
            "geometry": "geometria",
            "astronomy": "astronomia",
            "rhetoric": "rhetorica",
            "eloquence": "eloquentia",
            "literature": "litterae",
            "poetry": "poesis",
            "history": "historia",
            "memory": "memoria",
            "imagination": "imaginatio",
            "intellect": "intellectus",
            "reason": "ratio",
            "argument": "argumentum",
            "proof": "probatio",
            "evidence": "testimonium",
            "witness": "testis",
            "judgment": "iudicium",
            "decision": "consilium",
            "opinion": "sententia",
            "belief": "fides",
            "doubt": "dubitatio",
            "certainty": "certitudo",
            "possibility": "possibilitas",
            "necessity": "necessitas",
            "freedom": "libertas",
            "slavery": "servitus",
            "authority": "auctoritas",
            "power": "potestas",
            "strength": "vis",
            "weakness": "infirmitas",
            "virtue": "virtus",
            "vice": "vitium",
            "character": "ingenium",
            "nature": "natura",
            "custom": "consuetudo",
            "tradition": "traditio",
            "innovation": "novitas",
            "change": "mutatio",
            "permanence": "stabilitas",
            "eternity": "aeternitas",
            "infinity": "infinitas",
            "universe": "universum",
            "creation": "creatio",
            "destruction": "destructio",
            "beginning": "initium",
            "end": "finis",
            "purpose": "propositum",
            "destiny": "fatum",
            "fortune": "fortuna",
            "chance": "casus",
            "miracle": "miraculum",
            "mystery": "mysterium"
        }
        
        # Combine all dictionaries for easy access
        self.all_words = {**self.easy_words, **self.medium_words, **self.hard_words}
        
        # Track used words to avoid repetition
        self.used_words = set()
    
    def get_word_by_difficulty(self, difficulty="easy"):
        """Get a random word of specified difficulty"""
        if difficulty == "easy":
            word_dict = self.easy_words
        elif difficulty == "medium":
            word_dict = self.medium_words
        elif difficulty == "hard":
            word_dict = self.hard_words
        else:
            word_dict = self.easy_words
        
        # Filter out used words
        available_words = {k: v for k, v in word_dict.items() 
                          if k not in self.used_words}
        
        # If all words used, reset the used words set
        if not available_words:
            self.used_words.clear()
            available_words = word_dict
        
        # Select random word
        english_word = random.choice(list(available_words.keys()))
        latin_word = available_words[english_word]
        
        # Mark as used
        self.used_words.add(english_word)
        
        return english_word, latin_word
    
    def get_random_word(self):
        """Get a completely random word from any difficulty"""
        english_word = random.choice(list(self.all_words.keys()))
        latin_word = self.all_words[english_word]
        return english_word, latin_word
    
    def check_translation(self, english_word, user_input):
        """Check if the user's Latin translation is correct"""
        if english_word not in self.all_words:
            return False, "Word not found in dictionary"
        
        correct_latin = self.all_words[english_word].lower()
        user_latin = user_input.lower().strip()
        
        # Exact match
        if user_latin == correct_latin:
            return True, "Perfect!"
        
        # Close match (for typos)
        if self._is_close_match(user_latin, correct_latin):
            return True, "Close enough!"
        
        return False, f"Correct answer: {correct_latin}"
    
    def _is_close_match(self, user_input, correct_answer):
        """Check if user input is close to correct answer (handles typos)"""
        # Simple Levenshtein distance calculation
        if len(user_input) == 0:
            return len(correct_answer) <= 2
        if len(correct_answer) == 0:
            return len(user_input) <= 2
        
        # Allow 1-2 character differences for words
        max_differences = 1 if len(correct_answer) <= 5 else 2
        
        # Calculate differences
        differences = 0
        min_len = min(len(user_input), len(correct_answer))
        
        for i in range(min_len):
            if user_input[i] != correct_answer[i]:
                differences += 1
        
        # Add length difference
        differences += abs(len(user_input) - len(correct_answer))
        
        return differences <= max_differences
    
    def get_difficulty_for_word(self, english_word):
        """Get the difficulty level of a word"""
        if english_word in self.easy_words:
            return "easy"
        elif english_word in self.medium_words:
            return "medium"
        elif english_word in self.hard_words:
            return "hard"
        else:
            return "unknown"
    
    def get_hint(self, english_word):
        """Get a hint for the Latin translation"""
        if english_word not in self.all_words:
            return "No hint available"
        
        latin_word = self.all_words[english_word]
        
        # Provide first letter and length
        hint = f"Starts with '{latin_word[0].upper()}' and has {len(latin_word)} letters"
        
        # For longer words, give more hints
        if len(latin_word) > 6:
            hint += f", second letter is '{latin_word[1]}'"
        
        return hint
    
    def reset_used_words(self):
        """Reset the used words tracker"""
        self.used_words.clear()
    
    def get_stats(self):
        """Get statistics about the dictionary"""
        return {
            "easy_words": len(self.easy_words),
            "medium_words": len(self.medium_words), 
            "hard_words": len(self.hard_words),
            "total_words": len(self.all_words),
            "used_words": len(self.used_words)
        }
