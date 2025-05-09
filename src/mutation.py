import random
from copy import deepcopy
from utils import create_valid_team


def random_player_mutation(individual, player_pool=None):
    child = deepcopy(individual)
    team_idx = random.randint(0, len(child.teams) - 1)
    team = child.teams[team_idx]

    replace_idx = random.randint(0, len(team.players) - 1)
    old_player = team.players[replace_idx]
    pos = old_player.position

    used_ids = {p.id for t in child.teams for p in t.players}
    used_ids.discard(old_player.id)
    candidates = [p for p in player_pool if p.position == pos and p.id not in used_ids]

    if candidates:
        new_player = random.choice(candidates)
        if new_player.id != old_player.id:
            team.players[replace_idx] = new_player

    return child

def swap_players_between_teams(individual, player_pool=None):
    child = deepcopy(individual)
    t1, t2 = random.sample(range(len(child.teams)), 2)
    team1, team2 = child.teams[t1], child.teams[t2]
    
    pos = random.choice(['GK', 'DEF', 'MID', 'FWD'])
    p1 = next((i for i, p in enumerate(team1.players) if p.position == pos), None)
    p2 = next((j for j, q in enumerate(team2.players) if q.position == pos), None)

    if p1 is not None and p2 is not None:
        team1.players[p1], team2.players[p2] = team2.players[p2], team1.players[p1]
    return child

def replace_team_mutation(individual, player_pool=None, max_attempts=10):
    original_fitness = individual.fitness()
    child = deepcopy(individual)
    idx = random.randint(0, len(child.teams) - 1)
    used_ids = {p.id for i, t in enumerate(child.teams) if i != idx for p in t.players}

    attempt = 0
    while attempt < max_attempts:
        valid_team_found = False
        team_attempts = 0
        while not valid_team_found and team_attempts < 5:
            new_team = create_valid_team(player_pool, used_ids)
            if new_team:
                valid_team_found = True
            else:
                team_attempts += 1

        if valid_team_found:
            test_child = deepcopy(child)
            test_child.teams[idx] = new_team
            if test_child.fitness() != original_fitness:
                return test_child

        attempt += 1

    return child

def expensive_player_mutation(individual, player_pool=None):
    child = deepcopy(individual)
    all_players = [(ti, pi, p) for ti, team in enumerate(child.teams) for pi, p in enumerate(team.players)]
    most_expensive = max(all_players, key=lambda x: x[2].cost)
    ti, pi, p = most_expensive

    used_ids = {p.id for team in child.teams for p in team.players}
    candidates = [q for q in player_pool if q.position == p.position and q.cost < p.cost and q.id not in used_ids]

    if candidates:
        child.teams[ti].players[pi] = random.choice(candidates)
    return child

def cross_position_mutation(individual, player_pool=None):
    child = deepcopy(individual)
    t1, t2 = random.sample(range(len(child.teams)), 2)
    team1, team2 = child.teams[t1], child.teams[t2]
    pos = random.choice(['GK', 'DEF', 'MID', 'FWD'])

    p1 = next((i for i, p in enumerate(team1.players) if p.position == pos), None)
    p2 = next((j for j, p in enumerate(team2.players) if p.position == pos), None)

    if p1 is not None and p2 is not None:
        team1.players[p1], team2.players[p2] = team2.players[p2], team1.players[p1]
    return child

def forward_reset_mutation(individual, player_pool=None):
    child = deepcopy(individual)
    team_idx = random.randint(0, len(child.teams) - 1)
    team = child.teams[team_idx]
    used_ids = {p.id for t in child.teams for p in t.players}
    new_fwds = [p for p in player_pool if p.position == 'FWD' and p.id not in used_ids]
    current_fwds = [i for i, p in enumerate(team.players) if p.position == 'FWD']

    if len(new_fwds) >= len(current_fwds):
        replacements = random.sample(new_fwds, len(current_fwds))
        for i, new_p in zip(current_fwds, replacements):
            team.players[i] = new_p
    return child

def rotate_teams_mutation(individual, player_pool=None):
    child = deepcopy(individual)
    child.teams = child.teams[-1:] + child.teams[:-1]
    return child