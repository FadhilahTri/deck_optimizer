# Implementasi Hill Climbing Algorithm untuk Deck Building Optimizer
import random
import copy
from data.cards import CARDS
from utils.fitness import calculate_fitness

def get_neighbor(deck):
    """
    Hasilkan tetangga dengan swap 1 kartu di deck
    dengan kartu lain dari card pool yang belum ada di deck
    """
    deck_ids     = {c["id"] for c in deck}
    outside_pool = [c for c in CARDS if c["id"] not in deck_ids]

    if not outside_pool:
        return deck

    new_deck  = copy.deepcopy(deck)
    idx       = random.randint(0, len(new_deck) - 1)
    new_card  = random.choice(outside_pool)
    new_deck[idx] = new_card

    return new_deck


# ============================================================
# 1. SIMPLE HILL CLIMBING
# ============================================================
def simple_hill_climbing(initial_deck, max_iterations=100):
    """
    Simple Hill Climbing:
    - Cek 1 tetangga per iterasi
    - Pindah jika tetangga lebih baik
    """
    current_deck    = copy.deepcopy(initial_deck)
    current_fitness = calculate_fitness(current_deck)

    history = [current_fitness]  # Riwayat fitness per iterasi

    for i in range(max_iterations):
        neighbor         = get_neighbor(current_deck)
        neighbor_fitness = calculate_fitness(neighbor)

        if neighbor_fitness > current_fitness:
            current_deck    = neighbor
            current_fitness = neighbor_fitness

        history.append(current_fitness)

    return {
        "algorithm":     "Simple Hill Climbing",
        "final_deck":    current_deck,
        "final_fitness": current_fitness,
        "history":       history,
        "iterations":    max_iterations
    }


# ============================================================
# 2. STEEPEST ASCENT HILL CLIMBING
# ============================================================
def steepest_ascent_hill_climbing(initial_deck, max_iterations=100, num_neighbors=10):
    """
    Steepest Ascent Hill Climbing:
    - Cek BANYAK tetangga per iterasi (num_neighbors)
    - Pilih tetangga TERBAIK
    - Pindah hanya jika tetangga terbaik lebih baik dari current
    """
    current_deck    = copy.deepcopy(initial_deck)
    current_fitness = calculate_fitness(current_deck)

    history = [current_fitness]

    for i in range(max_iterations):
        # Generate banyak tetangga
        neighbors = [get_neighbor(current_deck) for _ in range(num_neighbors)]

        # Cari tetangga terbaik
        best_neighbor         = max(neighbors, key=calculate_fitness)
        best_neighbor_fitness = calculate_fitness(best_neighbor)

        if best_neighbor_fitness > current_fitness:
            current_deck    = best_neighbor
            current_fitness = best_neighbor_fitness

        history.append(current_fitness)

    return {
        "algorithm":     "Steepest Ascent Hill Climbing",
        "final_deck":    current_deck,
        "final_fitness": current_fitness,
        "history":       history,
        "iterations":    max_iterations
    }


# ============================================================
# 3. STOCHASTIC HILL CLIMBING
# ============================================================
def stochastic_hill_climbing(initial_deck, max_iterations=100):
    """
    Stochastic Hill Climbing:
    - Cek 1 tetangga per iterasi
    - Pindah dengan PROBABILITAS berdasarkan selisih fitness
    - Bisa menerima solusi yang sedikit lebih buruk (menghindari local optima)
    """
    current_deck    = copy.deepcopy(initial_deck)
    current_fitness = calculate_fitness(current_deck)

    history = [current_fitness]

    for i in range(max_iterations):
        neighbor         = get_neighbor(current_deck)
        neighbor_fitness = calculate_fitness(neighbor)

        delta = neighbor_fitness - current_fitness

        # Selalu terima jika lebih baik
        # Terima dengan probabilitas kecil jika lebih buruk
        if delta > 0:
            current_deck    = neighbor
            current_fitness = neighbor_fitness
        else:
            probability = 1 / (1 + abs(delta))
            if random.random() < probability:
                current_deck    = neighbor
                current_fitness = neighbor_fitness

        history.append(current_fitness)

    return {
        "algorithm":     "Stochastic Hill Climbing",
        "final_deck":    current_deck,
        "final_fitness": current_fitness,
        "history":       history,
        "iterations":    max_iterations
    }


# ============================================================
# 4. HILL CLIMBING WITH RANDOM RESTART
# ============================================================
def hill_climbing_random_restart(num_restarts=5, max_iterations=100):
    """
    Hill Climbing dengan Random Restart:
    - Jalankan Simple HC beberapa kali dari titik awal berbeda
    - Ambil hasil terbaik dari semua restart
    - Mengatasi masalah local optima
    """
    best_result  = None
    all_restarts = []

    for r in range(num_restarts):
        # Random deck awal yang berbeda tiap restart
        initial_deck = random.sample(CARDS, 20)
        result       = simple_hill_climbing(initial_deck, max_iterations)

        all_restarts.append({
            "restart":  r + 1,
            "fitness":  result["final_fitness"],
            "history":  result["history"]
        })

        if best_result is None or result["final_fitness"] > best_result["final_fitness"]:
            best_result = result

    return {
        "algorithm":    "Hill Climbing + Random Restart",
        "final_deck":   best_result["final_deck"],
        "final_fitness":best_result["final_fitness"],
        "history":      best_result["history"],
        "all_restarts": all_restarts,
        "num_restarts": num_restarts
    }