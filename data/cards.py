# Database kartu untuk Deck Building Optimizer
import random

CARDS = [
    # === WARRIOR (10 kartu) ===
    {"id": 1,  "name": "Knight",        "type": "Warrior", "attack": 7,  "defense": 6, "mana_cost": 4, "ability": "shield"},
    {"id": 2,  "name": "Berserker",     "type": "Warrior", "attack": 9,  "defense": 3, "mana_cost": 4, "ability": "rage"},
    {"id": 3,  "name": "Paladin",       "type": "Warrior", "attack": 6,  "defense": 7, "mana_cost": 5, "ability": "heal"},
    {"id": 4,  "name": "Gladiator",     "type": "Warrior", "attack": 8,  "defense": 4, "mana_cost": 4, "ability": "combo"},
    {"id": 5,  "name": "Warlord",       "type": "Warrior", "attack": 10, "defense": 5, "mana_cost": 6, "ability": "rally"},
    {"id": 6,  "name": "Swordsman",     "type": "Warrior", "attack": 6,  "defense": 5, "mana_cost": 3, "ability": "slash"},
    {"id": 7,  "name": "Guardian",      "type": "Warrior", "attack": 4,  "defense": 9, "mana_cost": 4, "ability": "shield"},
    {"id": 8,  "name": "Crusader",      "type": "Warrior", "attack": 7,  "defense": 7, "mana_cost": 5, "ability": "holy"},
    {"id": 9,  "name": "Barbarian",     "type": "Warrior", "attack": 9,  "defense": 2, "mana_cost": 3, "ability": "rage"},
    {"id": 10, "name": "Champion",      "type": "Warrior", "attack": 8,  "defense": 6, "mana_cost": 5, "ability": "rally"},

    # === MAGE (10 kartu) ===
    {"id": 11, "name": "Wizard",        "type": "Mage", "attack": 8,  "defense": 3, "mana_cost": 5, "ability": "fireball"},
    {"id": 12, "name": "Sorcerer",      "type": "Mage", "attack": 7,  "defense": 4, "mana_cost": 4, "ability": "freeze"},
    {"id": 13, "name": "Archmage",      "type": "Mage", "attack": 10, "defense": 3, "mana_cost": 7, "ability": "meteor"},
    {"id": 14, "name": "Illusionist",   "type": "Mage", "attack": 5,  "defense": 5, "mana_cost": 4, "ability": "mirror"},
    {"id": 15, "name": "Necromancer",   "type": "Mage", "attack": 8,  "defense": 4, "mana_cost": 6, "ability": "revive"},
    {"id": 16, "name": "Elementalist",  "type": "Mage", "attack": 9,  "defense": 3, "mana_cost": 6, "ability": "storm"},
    {"id": 17, "name": "Enchanter",     "type": "Mage", "attack": 6,  "defense": 5, "mana_cost": 5, "ability": "buff"},
    {"id": 18, "name": "Warlock",       "type": "Mage", "attack": 9,  "defense": 2, "mana_cost": 5, "ability": "curse"},
    {"id": 19, "name": "Diviner",       "type": "Mage", "attack": 5,  "defense": 6, "mana_cost": 4, "ability": "predict"},
    {"id": 20, "name": "Runemaster",    "type": "Mage", "attack": 7,  "defense": 5, "mana_cost": 5, "ability": "rune"},

    # === DRAGON (10 kartu) ===
    {"id": 21, "name": "Fire Dragon",   "type": "Dragon", "attack": 10, "defense": 7, "mana_cost": 8, "ability": "burn"},
    {"id": 22, "name": "Ice Dragon",    "type": "Dragon", "attack": 8,  "defense": 9, "mana_cost": 8, "ability": "freeze"},
    {"id": 23, "name": "Thunder Dragon","type": "Dragon", "attack": 11, "defense": 6, "mana_cost": 9, "ability": "lightning"},
    {"id": 24, "name": "Shadow Dragon", "type": "Dragon", "attack": 9,  "defense": 8, "mana_cost": 8, "ability": "stealth"},
    {"id": 25, "name": "Earth Dragon",  "type": "Dragon", "attack": 7,  "defense": 11,"mana_cost": 8, "ability": "quake"},
    {"id": 26, "name": "Wind Dragon",   "type": "Dragon", "attack": 9,  "defense": 7, "mana_cost": 7, "ability": "gust"},
    {"id": 27, "name": "Light Dragon",  "type": "Dragon", "attack": 10, "defense": 8, "mana_cost": 9, "ability": "holy"},
    {"id": 28, "name": "Void Dragon",   "type": "Dragon", "attack": 12, "defense": 5, "mana_cost": 9, "ability": "void"},
    {"id": 29, "name": "Sea Dragon",    "type": "Dragon", "attack": 8,  "defense": 10,"mana_cost": 8, "ability": "tide"},
    {"id": 30, "name": "Baby Dragon",   "type": "Dragon", "attack": 5,  "defense": 5, "mana_cost": 4, "ability": "burn"},

    # === SUPPORT (10 kartu) ===
    {"id": 31, "name": "Healer",        "type": "Support", "attack": 2,  "defense": 6, "mana_cost": 3, "ability": "heal"},
    {"id": 32, "name": "Shield Bearer", "type": "Support", "attack": 3,  "defense": 8, "mana_cost": 3, "ability": "shield"},
    {"id": 33, "name": "Bard",          "type": "Support", "attack": 3,  "defense": 5, "mana_cost": 3, "ability": "buff"},
    {"id": 34, "name": "Priest",        "type": "Support", "attack": 2,  "defense": 7, "mana_cost": 4, "ability": "holy"},
    {"id": 35, "name": "Alchemist",     "type": "Support", "attack": 4,  "defense": 5, "mana_cost": 4, "ability": "potion"},
    {"id": 36, "name": "Scout",         "type": "Support", "attack": 5,  "defense": 4, "mana_cost": 3, "ability": "predict"},
    {"id": 37, "name": "Summoner",      "type": "Support", "attack": 4,  "defense": 4, "mana_cost": 5, "ability": "summon"},
    {"id": 38, "name": "Merchant",      "type": "Support", "attack": 2,  "defense": 4, "mana_cost": 2, "ability": "trade"},
    {"id": 39, "name": "Tactician",     "type": "Support", "attack": 3,  "defense": 6, "mana_cost": 4, "ability": "rally"},
    {"id": 40, "name": "Oracle",        "type": "Support", "attack": 2,  "defense": 5, "mana_cost": 3, "ability": "predict"},

    # === TRAP (10 kartu) ===
    {"id": 41, "name": "Poison Trap",   "type": "Trap", "attack": 6,  "defense": 2, "mana_cost": 3, "ability": "poison"},
    {"id": 42, "name": "Mirror Trap",   "type": "Trap", "attack": 5,  "defense": 3, "mana_cost": 3, "ability": "mirror"},
    {"id": 43, "name": "Spike Trap",    "type": "Trap", "attack": 7,  "defense": 2, "mana_cost": 3, "ability": "bleed"},
    {"id": 44, "name": "Freeze Trap",   "type": "Trap", "attack": 4,  "defense": 4, "mana_cost": 3, "ability": "freeze"},
    {"id": 45, "name": "Thunder Trap",  "type": "Trap", "attack": 8,  "defense": 2, "mana_cost": 4, "ability": "lightning"},
    {"id": 46, "name": "Decoy Trap",    "type": "Trap", "attack": 3,  "defense": 5, "mana_cost": 2, "ability": "stealth"},
    {"id": 47, "name": "Bomb Trap",     "type": "Trap", "attack": 9,  "defense": 1, "mana_cost": 4, "ability": "burn"},
    {"id": 48, "name": "Web Trap",      "type": "Trap", "attack": 3,  "defense": 6, "mana_cost": 2, "ability": "slow"},
    {"id": 49, "name": "Curse Trap",    "type": "Trap", "attack": 6,  "defense": 3, "mana_cost": 3, "ability": "curse"},
    {"id": 50, "name": "Void Trap",     "type": "Trap", "attack": 7,  "defense": 3, "mana_cost": 4, "ability": "void"},
]

def get_all_cards():
    return CARDS

def get_random_deck(deck_size=20):
    """Ambil deck random dari card pool"""
    return random.sample(CARDS, deck_size)

def get_card_by_id(card_id):
    """Cari kartu berdasarkan ID"""
    return next((c for c in CARDS if c["id"] == card_id), None)