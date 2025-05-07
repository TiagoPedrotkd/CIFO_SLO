import random

def tournament_selection(population, fitnesses, k=2):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[0][0]

def roulette_wheel_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(population)
    probs = [f / total_fitness for f in fitnesses]
    return random.choices(population, weights=probs, k=1)[0]

def truncation_selection(population, fitnesses, top_percent=0.3):
    n = max(1, int(len(population) * top_percent))
    sorted_pop = [p for p, _ in sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)]
    top_individuals = sorted_pop[:n]
    return random.choice(top_individuals)

def rank_selection(population, fitnesses):
    sorted_pairs = sorted(zip(population, fitnesses), key=lambda x: x[1])
    ranks = list(range(1, len(population) + 1))
    total = sum(ranks)
    probs = [r / total for r in ranks]
    return random.choices([p for p, _ in sorted_pairs], weights=probs, k=1)[0]

def stochastic_universal_sampling(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(population)
    probs = [f / total_fitness for f in fitnesses]
    pointers = []
    point_distance = 1.0 / len(population)
    start = random.uniform(0, point_distance)
    for i in range(len(population)):
        pointers.append(start + i * point_distance)

    cumulative = 0
    selected = []
    i = 0
    for p, prob in zip(population, probs):
        cumulative += prob
        while i < len(pointers) and cumulative >= pointers[i]:
            selected.append(p)
            i += 1
    return random.choice(selected)

def elitism(population, fitnesses, num_elites=1):
    sorted_pairs = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
    return [ind for ind, _ in sorted_pairs[:num_elites]]

def select_parents(population, fitnesses, method="tournament"):
    if method == "tournament":
        return tournament_selection(population, fitnesses), tournament_selection(population, fitnesses)
    elif method == "roulette":
        return roulette_wheel_selection(population, fitnesses), roulette_wheel_selection(population, fitnesses)
    elif method == "truncation":
        return truncation_selection(population, fitnesses), truncation_selection(population, fitnesses)
    elif method == "rank":
        return rank_selection(population, fitnesses), rank_selection(population, fitnesses)
    elif method == "sus":
        return stochastic_universal_sampling(population, fitnesses), stochastic_universal_sampling(population, fitnesses)
    else:
        raise ValueError("Método de seleção inválido.")