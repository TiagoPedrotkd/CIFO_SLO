def evaluate_fitness(individual):
    if not individual.is_valid():
        return -1000

    skills = [team.average_skill() for team in individual.teams]
    mean = sum(skills) / len(skills)
    variance = sum((s - mean) ** 2 for s in skills) / len(skills)
    std_dev = variance ** 0.5

    return 1000 - (std_dev * 100)