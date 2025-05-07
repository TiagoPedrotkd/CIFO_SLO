import random
from utils import generate_initial_population
from fitness import evaluate_fitness
from selection import select_parents, elitism
from crossover import team_swap_crossover
from mutation import random_player_mutation

def main(players, pop_size=10, generations=20, elite_count=2,
         selection_method="tournament", crossover_op=None, mutation_op=None,
         verbose=True, crossover_rate=1.0, mutation_rate=1.0):

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

    if verbose:
        print("\nMelhor indivíduo final:")
        print("Fitness:", evaluate_fitness(best_individual))
        for i, team in enumerate(best_individual.teams):
            print(f"\nEquipa {i+1} - Média: {team.average_skill():.2f} | Custo total: €{team.total_cost():.2f}")
            for p in team.players:
                print(f"{p.name} ({p.position}) - Skill: {p.skill}, Custo: {p.cost}")

    return best_individual, best_fitness_over_time