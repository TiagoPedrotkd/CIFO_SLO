import random
import os
from utils import generate_initial_population
from fitness import evaluate_fitness
from selection import select_parents, elitism
from crossover import team_swap_crossover
from mutation import random_player_mutation

def main(players, pop_size=10, generations=20, elite_count=2,
         selection_method="tournament", crossover_op=None, mutation_op=None,
         verbose=True, crossover_rate=1.0, mutation_rate=1.0,):

    if crossover_op is None:
        crossover_op = team_swap_crossover
    if mutation_op is None:
        mutation_op = random_player_mutation

    population = generate_initial_population(pop_size, players)
    best_fitness_over_time = []

    for gen in range(generations):
        fitnesses = [evaluate_fitness(ind) for ind in population]
        best_fitness = max(fitnesses)
        best_fitness_over_time.append(best_fitness)

        if verbose:
            print(f"Geração {gen} - Melhor fitness: {best_fitness:.4f}")

        new_population = elitism(population, fitnesses, num_elites=elite_count)

        while len(new_population) < pop_size:
            p1, p2 = select_parents(population, fitnesses, method=selection_method)
            if random.random() < crossover_rate:
                c1, c2 = crossover_op(p1, p2)
            else:
                c1, c2 = p1, p2

            if random.random() < mutation_rate:
                c1 = mutation_op(c1, players)
            if random.random() < mutation_rate and len(new_population) + 1 < pop_size:
                c2 = mutation_op(c2, players)

            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)

        population = new_population

    final_fitnesses = [evaluate_fitness(ind) for ind in population]
    best_individual = population[final_fitnesses.index(max(final_fitnesses))]

    output_path = "../results/logs"
    os.makedirs(output_path, exist_ok=True)

    with open(os.path.join(output_path, "melhor_individuo.txt"), "w", encoding="utf-8") as f:
        f.write("Modelo Utilizados:\n")
        f.write(f"Crossover: {crossover_op.__name__}   Mutação: {mutation_op.__name__}   Selection: {selection_method}\n")
        f.write("Parâmetros Utilizados:\n")
        f.write(f"Crossover Rate: {crossover_rate}   Mutação Rate: {mutation_rate}\n")
        f.write("Melhor indivíduo final:\n")
        f.write(f"Fitness: {evaluate_fitness(best_individual):.2f}\n")
        
        for i, team in enumerate(best_individual.teams):
            f.write(f"\nEquipa {i+1} - Média: {team.average_skill():.2f} | Custo total: €{team.total_cost():.2f}\n")
            for p in team.players:
                f.write(f"{p.name} ({p.position}) - Skill: {p.skill}, Custo: {p.cost}\n")

    print("✅ Resultado final escrito em 'results/logs/melhor_individuo.txt'")

    return best_individual, best_fitness_over_time