import random
from copy import deepcopy

def team_swap_crossover(parent1, parent2):
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)
    idx = random.randint(0, len(parent1.teams) - 1)
    child1.teams[idx], child2.teams[idx] = deepcopy(parent2.teams[idx]), deepcopy(parent1.teams[idx])
    return child1, child2

def player_swap_crossover(parent1, parent2):
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)
    team_idx = random.randint(0, len(parent1.teams) - 1)
    team1 = child1.teams[team_idx]
    team2 = child2.teams[team_idx]

    common_positions = list(set(p.position for p in team1.players).intersection(p.position for p in team2.players))
    if not common_positions:
        return deepcopy(parent1), deepcopy(parent2)

    pos = random.choice(common_positions)
    p1_candidates = [i for i, p in enumerate(team1.players) if p.position == pos]
    p2_candidates = [i for i, p in enumerate(team2.players) if p.position == pos]
    if not p1_candidates or not p2_candidates:
        return deepcopy(parent1), deepcopy(parent2)

    p1_idx = random.choice(p1_candidates)
    p2_idx = random.choice(p2_candidates)
    team1.players[p1_idx], team2.players[p2_idx] = team2.players[p2_idx], team1.players[p1_idx]
    return child1, child2


def uniform_team_crossover(parent1, parent2):
    child = deepcopy(parent1)
    for i in range(len(parent1.teams)):
        if random.random() < 0.5:
            child.teams[i] = deepcopy(parent2.teams[i])
    return child


def position_based_crossover(parent1, parent2):
    child = deepcopy(parent1)
    pos = random.choice(['GK', 'DEF', 'MID', 'FWD'])
    for i in range(len(parent1.teams)):
        team1 = child.teams[i]
        team2 = parent2.teams[i]
        for j, p1 in enumerate(team1.players):
            if p1.position == pos:
                for k, p2 in enumerate(team2.players):
                    if p2.position == pos:
                        team1.players[j] = deepcopy(p2)
                        break
    return child

def gene_level_crossover(parent1, parent2):
    from models import Individual, Team
    all_players = [p for team in parent1.teams for p in team.players] + \
                  [p for team in parent2.teams for p in team.players]
    random.shuffle(all_players)
    
    used_ids = set()
    teams = []
    for _ in range(5):
        team = []
        pos_requirements = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
        for p in all_players:
            if p.id in used_ids or pos_requirements.get(p.position, 0) == 0:
                continue
            team.append(p)
            used_ids.add(p.id)
            pos_requirements[p.position] -= 1
            if sum(pos_requirements.values()) == 0:
                break
        if len(team) == 7:
            from models import Team
            teams.append(Team(team))
    if len(teams) == 5:
        return Individual(teams)
    else:
        return deepcopy(parent1)