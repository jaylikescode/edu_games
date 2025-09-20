# Latin Textbook Vocabulary Database
import random

class LatinTextbook:
    def __init__(self, name, description, lessons):
        self.name = name
        self.description = description
        self.lessons = lessons  # Dictionary of lesson_number: {vocabulary, grammar_focus}
    
    def get_lesson_vocabulary(self, lesson_number):
        """Get vocabulary for a specific lesson"""
        if lesson_number in self.lessons:
            return self.lessons[lesson_number]["vocabulary"]
        return {}
    
    def get_lesson_info(self, lesson_number):
        """Get complete lesson information"""
        if lesson_number in self.lessons:
            return self.lessons[lesson_number]
        return None
    
    def get_available_lessons(self):
        """Get list of available lesson numbers"""
        return sorted(self.lessons.keys())

class TextbookManager:
    def __init__(self):
        self.textbooks = self._initialize_textbooks()
        self.current_textbook = None
        self.current_lesson = 1
    
    def _initialize_textbooks(self):
        """Initialize all available textbooks"""
        textbooks = {}
        
        # Henle Latin First Year
        henle_lessons = self._create_henle_lessons()
        textbooks["henle1"] = LatinTextbook(
            "Henle Latin First Year",
            "Traditional grammar-based approach with classical readings",
            henle_lessons
        )
        
        # Wheelock's Latin
        wheelock_lessons = self._create_wheelock_lessons()
        textbooks["wheelock"] = LatinTextbook(
            "Wheelock's Latin",
            "Comprehensive introduction to classical Latin",
            wheelock_lessons
        )
        
        # Cambridge Latin Course
        cambridge_lessons = self._create_cambridge_lessons()
        textbooks["cambridge"] = LatinTextbook(
            "Cambridge Latin Course",
            "Story-based approach with cultural context",
            cambridge_lessons
        )
        
        # Lingua Latina (Ørberg)
        lingua_lessons = self._create_lingua_lessons()
        textbooks["lingua"] = LatinTextbook(
            "Lingua Latina (Ørberg)",
            "Natural method - Latin taught in Latin",
            lingua_lessons
        )
        
        return textbooks
    
    def _create_henle_lessons(self):
        """Create Henle Latin First Year lesson vocabulary"""
        return {
            1: {
                "title": "First Declension Nouns",
                "grammar_focus": "First declension nouns (-a endings)",
                "vocabulary": {
                    "girl": "puella",
                    "water": "aqua", 
                    "island": "insula",
                    "table": "mensa",
                    "rose": "rosa",
                    "fortune": "fortuna",
                    "victory": "victoria",
                    "memory": "memoria",
                    "glory": "gloria",
                    "sailor": "nauta"
                }
            },
            2: {
                "title": "Verbs - Present Tense",
                "grammar_focus": "Present tense of first conjugation verbs",
                "vocabulary": {
                    "love": "amo",
                    "call": "voco",
                    "give": "do",
                    "walk": "ambulo",
                    "work": "laboro",
                    "sail": "navigo",
                    "tell": "narro",
                    "carry": "porto",
                    "praise": "laudo",
                    "prepare": "paro"
                }
            },
            3: {
                "title": "Second Declension - Masculine",
                "grammar_focus": "Second declension masculine nouns (-us endings)",
                "vocabulary": {
                    "friend": "amicus",
                    "field": "ager",
                    "boy": "puer",
                    "master": "dominus",
                    "god": "deus",
                    "people": "populus",
                    "number": "numerus",
                    "place": "locus",
                    "wind": "ventus",
                    "horse": "equus"
                }
            },
            4: {
                "title": "Adjectives - First/Second Declension",
                "grammar_focus": "Adjective agreement with nouns",
                "vocabulary": {
                    "good": "bonus",
                    "bad": "malus",
                    "great": "magnus",
                    "small": "parvus",
                    "many": "multi",
                    "few": "pauci",
                    "high": "altus",
                    "wide": "latus",
                    "long": "longus",
                    "new": "novus"
                }
            },
            5: {
                "title": "Second Declension - Neuter",
                "grammar_focus": "Second declension neuter nouns (-um endings)",
                "vocabulary": {
                    "war": "bellum",
                    "gift": "donum",
                    "danger": "periculum",
                    "kingdom": "regnum",
                    "town": "oppidum",
                    "help": "auxilium",
                    "office": "officium",
                    "example": "exemplum",
                    "temple": "templum",
                    "iron": "ferrum"
                }
            },
            6: {
                "title": "Prepositions",
                "grammar_focus": "Prepositions with accusative and ablative",
                "vocabulary": {
                    "in": "in",
                    "with": "cum",
                    "from": "de",
                    "through": "per",
                    "to": "ad",
                    "without": "sine",
                    "by": "a",
                    "before": "ante",
                    "after": "post",
                    "under": "sub"
                }
            },
            7: {
                "title": "Imperfect Tense",
                "grammar_focus": "Imperfect tense of all conjugations",
                "vocabulary": {
                    "was loving": "amabam",
                    "was having": "habebam",
                    "was seeing": "videbam",
                    "was hearing": "audiebam",
                    "was coming": "veniebam",
                    "was saying": "dicebam",
                    "was making": "faciebam",
                    "was going": "ibam",
                    "was being": "eram",
                    "was able": "poteram"
                }
            },
            8: {
                "title": "Third Declension - Consonant Stems",
                "grammar_focus": "Third declension consonant stem nouns",
                "vocabulary": {
                    "king": "rex",
                    "voice": "vox",
                    "peace": "pax",
                    "foot": "pes",
                    "part": "pars",
                    "law": "lex",
                    "leader": "dux",
                    "soldier": "miles",
                    "name": "nomen",
                    "body": "corpus"
                }
            }
        }
    
    def _create_wheelock_lessons(self):
        """Create Wheelock's Latin lesson vocabulary"""
        return {
            1: {
                "title": "The Alphabet and Pronunciation",
                "grammar_focus": "Latin alphabet and pronunciation rules",
                "vocabulary": {
                    "nothing": "nihil",
                    "not": "non",
                    "where": "ubi",
                    "indeed": "quidem",
                    "often": "saepe",
                    "if": "si",
                    "but": "sed",
                    "and": "et",
                    "also": "etiam",
                    "always": "semper"
                }
            },
            2: {
                "title": "Cases and Declensions",
                "grammar_focus": "Introduction to cases and first declension",
                "vocabulary": {
                    "fatherland": "patria",
                    "fortune": "fortuna",
                    "form": "forma",
                    "girl": "puella",
                    "poet": "poeta",
                    "philosophy": "philosophia",
                    "wisdom": "sapientia",
                    "life": "vita",
                    "memory": "memoria",
                    "victory": "victoria"
                }
            },
            3: {
                "title": "Second Declension",
                "grammar_focus": "Second declension masculine and neuter",
                "vocabulary": {
                    "friend": "amicus",
                    "book": "liber",
                    "boy": "puer",
                    "people": "populus",
                    "Roman": "Romanus",
                    "gift": "donum",
                    "duty": "officium",
                    "danger": "periculum",
                    "war": "bellum",
                    "evil": "malum"
                }
            }
        }
    
    def _create_cambridge_lessons(self):
        """Create Cambridge Latin Course lesson vocabulary"""
        return {
            1: {
                "title": "Caecilius",
                "grammar_focus": "Introduction to Latin through stories",
                "vocabulary": {
                    "father": "pater",
                    "son": "filius",
                    "house": "villa",
                    "garden": "hortus",
                    "dog": "canis",
                    "sits": "sedet",
                    "reads": "legit",
                    "writes": "scribit",
                    "sleeps": "dormit",
                    "walks": "ambulat"
                }
            },
            2: {
                "title": "In Villa",
                "grammar_focus": "Nominative and accusative cases",
                "vocabulary": {
                    "merchant": "mercator",
                    "slave": "servus",
                    "cook": "coquus",
                    "food": "cibus",
                    "wine": "vinum",
                    "buys": "emit",
                    "sells": "vendit",
                    "prepares": "parat",
                    "eats": "consumit",
                    "drinks": "bibit"
                }
            }
        }
    
    def _create_lingua_lessons(self):
        """Create Lingua Latina lesson vocabulary"""
        return {
            1: {
                "title": "Imperium Romanum",
                "grammar_focus": "Natural introduction to Latin",
                "vocabulary": {
                    "Rome": "Roma",
                    "Italy": "Italia",
                    "Gaul": "Gallia",
                    "Germania": "Germania",
                    "Britannia": "Britannia",
                    "province": "provincia",
                    "empire": "imperium",
                    "is": "est",
                    "are": "sunt",
                    "in": "in"
                }
            },
            2: {
                "title": "Familia Romana",
                "grammar_focus": "Roman family vocabulary",
                "vocabulary": {
                    "family": "familia",
                    "father": "pater",
                    "mother": "mater",
                    "son": "filius",
                    "daughter": "filia",
                    "brother": "frater",
                    "sister": "soror",
                    "husband": "maritus",
                    "wife": "uxor",
                    "child": "liberi"
                }
            }
        }
    
    def get_textbook(self, textbook_id):
        """Get a specific textbook"""
        return self.textbooks.get(textbook_id)
    
    def get_all_textbooks(self):
        """Get all available textbooks"""
        return self.textbooks
    
    def set_current_textbook(self, textbook_id, lesson_number=1):
        """Set the current textbook and lesson"""
        if textbook_id in self.textbooks:
            self.current_textbook = textbook_id
            self.current_lesson = lesson_number
            return True
        return False
    
    def get_current_vocabulary(self):
        """Get vocabulary for current textbook and lesson"""
        if self.current_textbook:
            textbook = self.textbooks[self.current_textbook]
            return textbook.get_lesson_vocabulary(self.current_lesson)
        return {}
    
    def get_current_lesson_info(self):
        """Get current lesson information"""
        if self.current_textbook:
            textbook = self.textbooks[self.current_textbook]
            return textbook.get_lesson_info(self.current_lesson)
        return None
