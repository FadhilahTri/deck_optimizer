# Implementasi Genetic Algorithm untuk Deck Building Optimizer
import random
import copy
from data.cards import CARDS
from utils.fitness import calculate_fitness

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_individual():
    """Buat 1 individu (deck random) dari card pool"""
    return random.sample(CARDS, 20)

def create_population(pop_size=50):
    """Buat populasi awal"""
    return [create_individual() for _ in range(pop_size)]

def selection_tournament(population, k=3):
    """
    Tournament Selection:
    - Pilih k individu random dari populasi
    - Kembalikan yang fitness-nya tertinggi
    """
    tournament = random.sample(population, k)
    return max(tournament, key=calculate_fitness)

def crossover(parent1, parent2):
    """
    Single-point Crossover:
    - Potong di titik random
    - Gabungkan bagian parent1 + parent2
    - Hindari duplikat kartu
    """
    point = random.randint(1, 19)
    
    child_cards = parent1[:point]
    child_ids   = {c["id"] for c in child_cards}
    
    for card in parent2:
        if card["id"] not in child_ids and len(child_cards) < 20:
            child_cards.append(card)
            child_ids.add(card["id"])
    
    # Kalau masih kurang dari 20, isi dari pool
    if len(child_cards) < 20:
        remaining = [c for c in CARDS if c["id"] not in child_ids]
        random.shuffle(remaining)
        child_cards += remaining[:20 - len(child_cards)]
    
    return child_cards

def mutate(deck, mutation_rate=0.1):
    """
    Mutasi:
    - Tiap kartu punya peluang mutation_rate untuk diganti
    - Kartu diganti dengan kartu random dari pool yang belum ada di deck
    """
    new_deck  = copy.deepcopy(deck)
    deck_ids  = {c["id"] for c in new_deck}
    
    for i in range(len(new_deck)):
        if random.random() < mutation_rate:
            outside_pool = [c for c in CARDS if c["id"] not in deck_ids]
            if outside_pool:
                new_card       = random.choice(outside_pool)
                deck_ids.discard(new_deck[i]["id"])
                new_deck[i]    = new_card
                deck_ids.add(new_card["id"])
    
    return new_deck


# ============================================================
# GENETIC ALGORITHM MAIN
# ============================================================

def genetic_algorithm(
    pop_size=50,
    generations=100,
    mutation_rate=0.1,
    crossover_rate=0.8,
    elitism=2
):
    """
    Genetic Algorithm:
    1. Buat populasi awal
    2. Evaluasi fitness semua individu
    3. Seleksi, crossover, mutasi → generasi baru
    4. Ulangi sampai max generasi
    """
    # 1. Inisialisasi populasi
    population = create_population(pop_size)
    
    best_deck    = None
    best_fitness = 0
    history      = []  # Fitness terbaik per generasi
    avg_history  = []  # Rata-rata fitness per generasi
    
    for gen in range(generations):
        # 2. Evaluasi fitness
        fitness_scores = [(deck, calculate_fitness(deck)) for deck in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Update best
        if fitness_scores[0][1] > best_fitness:
            best_deck    = copy.deepcopy(fitness_scores[0][0])
            best_fitness = fitness_scores[0][1]
        
        gen_best = fitness_scores[0][1]
        gen_avg  = sum(f for _, f in fitness_scores) / len(fitness_scores)
        
        history.append(round(gen_best, 4))
        avg_history.append(round(gen_avg, 4))
        
        # 3. Buat generasi baru
        new_population = []
        
        # Elitism: langsung masukkan individu terbaik
        for i in range(elitism):
            new_population.append(copy.deepcopy(fitness_scores[i][0]))
        
        # Isi sisa populasi dengan crossover + mutasi
        while len(new_population) < pop_size:
            parent1 = selection_tournament([d for d, _ in fitness_scores])
            parent2 = selection_tournament([d for d, _ in fitness_scores])
            
            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = copy.deepcopy(parent1)
            
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    return {
        "algorithm":      "Genetic Algorithm",
        "final_deck":     best_deck,
        "final_fitness":  best_fitness,
        "history":        history,
        "avg_history":    avg_history,
        "generations":    generations,
        "pop_size":       pop_size,
        "mutation_rate":  mutation_rate,
        "crossover_rate": crossover_rate
    }