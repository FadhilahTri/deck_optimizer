from flask import Flask, render_template, jsonify, request
import random
from data.cards import CARDS, get_random_deck
from utils.fitness import calculate_fitness, get_fitness_breakdown
from algorithms.hill_climbing import (
    simple_hill_climbing,
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    hill_climbing_random_restart
)
from algorithms.simulated_annealing import simulated_annealing
from algorithms.genetic_algorithm import genetic_algorithm

app = Flask(__name__)

# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/cards")
def get_cards():
    """Return semua kartu"""
    return jsonify(CARDS)

@app.route("/api/optimize", methods=["POST"])
def optimize():
    """
    Jalankan algoritma optimasi
    Body: { "algorithm": "simple_hc" | "steepest_hc" | "stochastic_hc" | "random_restart" | "sa" | "ga" }
    """
    data      = request.get_json()
    algorithm = data.get("algorithm", "simple_hc")
    
    # Deck awal random
    initial_deck = get_random_deck(20)
    
    if algorithm == "simple_hc":
        result = simple_hill_climbing(initial_deck, max_iterations=100)
    
    elif algorithm == "steepest_hc":
        result = steepest_ascent_hill_climbing(initial_deck, max_iterations=100, num_neighbors=10)
    
    elif algorithm == "stochastic_hc":
        result = stochastic_hill_climbing(initial_deck, max_iterations=100)
    
    elif algorithm == "random_restart":
        result = hill_climbing_random_restart(num_restarts=5, max_iterations=100)
    
    elif algorithm == "sa":
        result = simulated_annealing(
            initial_deck,
            initial_temp=1000,
            cooling_rate=0.95,
            min_temp=0.1,
            max_iterations=200
        )
    
    elif algorithm == "ga":
        result = genetic_algorithm(
            pop_size=50,
            generations=100,
            mutation_rate=0.1,
            crossover_rate=0.8,
            elitism=2
        )
    
    else:
        return jsonify({"error": "Algorithm not found"}), 400
    
    # Tambahkan breakdown fitness ke result
    breakdown = get_fitness_breakdown(result["final_deck"])
    
    return jsonify({
        "algorithm":     result["algorithm"],
        "final_fitness": result["final_fitness"],
        "history":       result["history"],
        "final_deck":    result["final_deck"],
        "breakdown":     breakdown,
        "iterations":    result.get("iterations", result.get("generations", 0))
    })

@app.route("/api/compare", methods=["GET"])
def compare_all():
    """Jalankan semua algoritma dan bandingkan hasilnya"""
    initial_deck = get_random_deck(20)
    initial_fitness = calculate_fitness(initial_deck)
    
    results = {}
    
    results["simple_hc"] = simple_hill_climbing(initial_deck)
    results["steepest_hc"] = steepest_ascent_hill_climbing(initial_deck)
    results["stochastic_hc"] = stochastic_hill_climbing(initial_deck)
    results["sa"] = simulated_annealing(initial_deck)
    results["ga"] = genetic_algorithm()
    
    comparison = []
    for key, res in results.items():
        comparison.append({
            "algorithm":     res["algorithm"],
            "final_fitness": res["final_fitness"],
            "history":       res["history"]
        })
    
    return jsonify({
        "initial_fitness": initial_fitness,
        "comparison":      comparison
    })

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)