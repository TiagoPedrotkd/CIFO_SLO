from models import Team, Individual
import random

def create_valid_team(players, used_ids):
    team = []
    try:
        for pos, count in [('GK',1), ('DEF',2), ('MID',2), ('FWD',2)]:
            options = [p for p in players if p.position == pos and p.id not in used_ids]
            selected = random.sample(options, count)
            team.extend(selected)
            used_ids.update(p.id for p in selected)
        new_team = Team(team)
        if new_team.total_cost() <= 750:
            return new_team
        else:
            return create_valid_team(players) 
    except:
        return None

def create_valid_individual(players, max_attempts=10):
    for attempt in range(max_attempts):
        all_ids = set()
        teams = []

        for _ in range(5):
            team = None
            tries = 0
            while not team and tries < 10:
                team = create_valid_team(players, all_ids)
                tries += 1
            if team:
                teams.append(team)
                all_ids.update(p.id for p in team.players)

        if len(teams) == 5:
            return Individual(teams)

    print("[INFO] Não foi possível gerar um indivíduo válido após várias tentativas.")
    return None

def generate_initial_population(n, players):
    population = []
    attempts = 0
    max_attempts = n * 10

    while len(population) < n and attempts < max_attempts:
        ind = create_valid_individual(players)
        if ind is not None and ind.is_valid():
            population.append(ind)
        attempts += 1

    return population