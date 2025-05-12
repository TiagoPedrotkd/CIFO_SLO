class Player:

    def __init__(self, player_id, name, position, skill, cost):

        self.id = player_id
        self.name = name
        self.position = position
        self.skill = skill
        self.cost = cost

    def __repr__(self):
        return f"{self.name} ({self.position}) - Skill: {self.skill} | €M{self.cost}"
    
    def get_attribute(self, attribute):

        if attribute == "Name":
            return self.name
        elif attribute == "Position":
            return self.position
        elif attribute == "Skill":
            return self.skill
        elif attribute == "Salary (€M)":
            return self.cost
        else :
            return self.id

class Team:

    def __init__(self, players = None):

        self.players = players if players else []

    
    def add_player(self, player):

        self.players.append(player)

    def total_cost(self):

        return sum(p.cost for p in self.players)
    
    def average_skill(self):

        return sum(p.skill for p in self.players) / len(self.players)
    
    def is_valid(self):
        if len(self.players) != 7:
            return False
        
        pos_count = {"GK" : 0, "DEF" : 0, "MID" : 0, "FWD": 0}

        for p in self.players:
            pos_count[p.position] += 1
        
        return (pos_count["GK"] == 1 and pos_count["DEF"] == 2 and pos_count["MID"] == 2 and pos_count["FWD"] == 2 and self.total_cost() <= 750)
    

class Individual:

    def __init__(self, teams = None):
        
        self.teams = teams if teams else []

    def is_valid(self):
        ids = []

        for team in self.teams:
            if not team.is_valid():
                return False
            
            for p in team.players:
                if p.id in ids:
                    return False
                
                ids.append(p.id)
            
            return True

    def fitness(self):
        if not self.is_valid():
            return -1000

        skills = [team.average_skill() for team in self.teams]
        mean = sum(skills) / len(skills)
        variance = sum((s - mean) ** 2 for s in skills) / len(skills)
        std_dev = variance ** 0.5

        return 1000 - (std_dev * 100)