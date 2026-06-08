# Fitness function untuk mengevaluasi kualitas deck

# Bonus sinergi antar kartu
SYNERGY_RULES = {
    "Warrior": {"min_count": 3, "bonus": 10},
    "Mage":    {"min_count": 3, "bonus": 12},
    "Dragon":  {"min_count": 2, "bonus": 15},
    "Support": {"min_count": 2, "bonus": 8},
    "Trap":    {"min_count": 3, "bonus": 10},
}

# Bonus kombinasi tipe berbeda
COMBO_RULES = [
    ({"Warrior", "Support"}, 8),   # Warrior + Support = tanky combo
    ({"Mage", "Trap"}, 10),        # Mage + Trap = control combo
    ({"Dragon", "Mage"}, 12),      # Dragon + Mage = power combo
    ({"Warrior", "Dragon"}, 10),   # Warrior + Dragon = brute combo
]

def calculate_fitness(deck):
    """
    Hitung fitness score sebuah deck
    fitness = (total_attack x 0.35) + (total_defense x 0.25) 
            + (sinergi_bonus x 0.25) + (mana_efficiency x 0.15)
    """
    if not deck:
        return 0

    # 1. Hitung total attack & defense
    total_attack  = sum(c["attack"]  for c in deck)
    total_defense = sum(c["defense"] for c in deck)

    # 2. Hitung sinergi bonus
    type_count = {}
    for card in deck:
        t = card["type"]
        type_count[t] = type_count.get(t, 0) + 1

    synergy_bonus = 0

    # Bonus per tipe
    for tipe, rule in SYNERGY_RULES.items():
        if type_count.get(tipe, 0) >= rule["min_count"]:
            synergy_bonus += rule["bonus"]

    # Bonus kombinasi tipe
    types_in_deck = set(type_count.keys())
    for combo_types, bonus in COMBO_RULES:
        if combo_types.issubset(types_in_deck):
            synergy_bonus += bonus

    # 3. Hitung mana efficiency
    total_mana = sum(c["mana_cost"] for c in deck)
    avg_mana   = total_mana / len(deck)
    # Makin rendah rata-rata mana = makin efisien
    mana_efficiency = max(0, (10 - avg_mana) * len(deck))

    # 4. Gabungkan semua komponen
    fitness = (
        (total_attack     * 0.35) +
        (total_defense    * 0.25) +
        (synergy_bonus    * 0.25) +
        (mana_efficiency  * 0.15)
    )

    return round(fitness, 4)


def get_fitness_breakdown(deck):
    """Return detail komponen fitness untuk ditampilkan di UI"""
    total_attack  = sum(c["attack"]  for c in deck)
    total_defense = sum(c["defense"] for c in deck)

    type_count = {}
    for card in deck:
        t = card["type"]
        type_count[t] = type_count.get(t, 0) + 1

    synergy_bonus = 0
    for tipe, rule in SYNERGY_RULES.items():
        if type_count.get(tipe, 0) >= rule["min_count"]:
            synergy_bonus += rule["bonus"]

    types_in_deck = set(type_count.keys())
    for combo_types, bonus in COMBO_RULES:
        if combo_types.issubset(types_in_deck):
            synergy_bonus += bonus

    total_mana      = sum(c["mana_cost"] for c in deck)
    avg_mana        = total_mana / len(deck)
    mana_efficiency = max(0, (10 - avg_mana) * len(deck))

    return {
        "total_attack":     total_attack,
        "total_defense":    total_defense,
        "synergy_bonus":    synergy_bonus,
        "mana_efficiency":  round(mana_efficiency, 2),
        "fitness_score":    calculate_fitness(deck)
    }