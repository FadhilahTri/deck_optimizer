# Implementasi Simulated Annealing untuk Deck Building Optimizer
import random
import copy
import math
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

    new_deck      = copy.deepcopy(deck)
    idx           = random.randint(0, len(new_deck) - 1)
    new_card      = random.choice(outside_pool)
    new_deck[idx] = new_card

    return new_deck


def simulated_annealing(
    initial_deck,
    initial_temp=1000,
    cooling_rate=0.95,
    min_temp=0.1,
    max_iterations=200
):
    """
    Simulated Annealing:
    - Mulai dengan suhu tinggi (banyak eksplorasi)
    - Suhu turun perlahan (cooling_rate)
    - Makin dingin = makin selektif dalam menerima solusi buruk
    - Probabilitas terima solusi buruk: e^(delta/T)
    """
    current_deck    = copy.deepcopy(initial_deck)
    current_fitness = calculate_fitness(current_deck)

    best_deck       = copy.deepcopy(current_deck)
    best_fitness    = current_fitness

    temperature     = initial_temp
    history         = [current_fitness]
    temp_history    = [temperature]
    accept_history  = []  # Riwayat penerimaan solusi buruk

    iteration = 0

    while temperature > min_temp and iteration < max_iterations:
        neighbor         = get_neighbor(current_deck)
        neighbor_fitness = calculate_fitness(neighbor)

        delta = neighbor_fitness - current_fitness

        if delta > 0:
            # Solusi lebih baik, langsung terima
            current_deck    = neighbor
            current_fitness = neighbor_fitness
            accept_history.append({
                "iteration": iteration,
                "type":      "better",
                "delta":     round(delta, 4),
                "prob":      1.0
            })
        else:
            # Solusi lebih buruk, terima dengan probabilitas Boltzmann
            probability = math.exp(delta / temperature)
            if random.random() < probability:
                current_deck    = neighbor
                current_fitness = neighbor_fitness
                accept_history.append({
                    "iteration": iteration,
                    "type":      "worse_accepted",
                    "delta":     round(delta, 4),
                    "prob":      round(probability, 4)
                })
            else:
                accept_history.append({
                    "iteration": iteration,
                    "type":      "worse_rejected",
                    "delta":     round(delta, 4),
                    "prob":      round(probability, 4)
                })

        # Update solusi terbaik
        if current_fitness > best_fitness:
            best_deck    = copy.deepcopy(current_deck)
            best_fitness = current_fitness

        # Turunkan suhu
        temperature *= cooling_rate

        history.append(current_fitness)
        temp_history.append(round(temperature, 4))
        iteration += 1

    return {
        "algorithm":      "Simulated Annealing",
        "final_deck":     best_deck,
        "final_fitness":  best_fitness,
        "history":        history,
        "temp_history":   temp_history,
        "accept_history": accept_history,
        "iterations":     iteration,
        "initial_temp":   initial_temp,
        "cooling_rate":   cooling_rate,
        "min_temp":       min_temp
    }