"""
The team builder
"""
from __future__ import annotations

import sys
from subprocess import check_output
import copy
from tqdm import tqdm
import numpy as np
from poke_env.teambuilder import Teambuilder
from .team import Team

class Builder(Teambuilder):
    """
    The team builder
    """
    def __init__(self, N_seed_teams=2, teams=None, format="gen3randombattle"):
        if teams:
            self.teams = [
                self.join_team(self.parse_showdown_team(team)) for team in teams
            ]
        else:
            self.teams = []
            print("Generating seed teams")
            for _ in tqdm(range(N_seed_teams)):

                try:
                    n_team = self.parse_showdown_team(check_output(f"pokemon-showdown generate-team {format}| pokemon-showdown export-team", shell=True).decode(sys.stdout.encoding))
                    self.teams.append(n_team)
                except TypeError as e:
                    print("Error generating team... skipping to next")

                
        self.poke_pool = np.array(self.teams).flatten()
        
    def build_N_teams_from_poke_pool(self, N_teams):
        self.teams = [Team(np.random.choice(self.poke_pool, size=6, replace=False)) for _ in range(N_teams)]
        
    def get_teams(self):
        return self.teams

    def yield_team(self):
        return self.teams[np.random.choice(len(self.teams))]

    def generate_new_teams(self):
        self.last_generation =  copy.deepcopy(self.teams)
        self.breed_teams()
        # TODO: Make this fancier
        #self.mutate_teams()


    def breed_teams(self):
        teams = []
        for i in range(len(self.teams)):
            probs = np.array([t.get_fitness() for t in self.teams])
            probs = probs/np.sum(probs)
            t1, t2 = np.random.choice(self.teams, 2, p=probs, replace=False)
            t1 = t1.get_teamlist()
            t2 = t2.get_teamlist()
            teams.append(self.breed_team(t1,t2))
        self.teams = teams
        self.duplicate_detect() # Prob should take out or move this somewhere else 
            
    def breed_team(self, t1,t2):
        # REALLY BAD DUPLICATION PREVENTION
        # TODO: FIX ASAP      
        poss_pokes = np.concatenate((t1,t2))
        names = [str(p).split("|")[0] for p in poss_pokes]
        new_team_names = np.random.choice(list(set(names)), size=6, replace=False)
        n2p = {n:p for n,p in zip(names,poss_pokes)}
        new_team =[n2p[n] for n in new_team_names]
        return Team(new_team)

    def duplicate_detect(self):
        for t in self.teams:
            pokes = []
            for p in t.get_teamlist():
                pokes.append(str(p).split("|")[0])
            if len(set(pokes)) != 6:
                print("WARNING DUPLICATION DETECTED")
                print(pokes)

    def mutate_team(self, team, mutation_rate=0.1):
        # Each pokemon in a team has a given probability of being replaced by a random pokemon from the pool
        for pokemon in team:
            if np.random.random() < mutation_rate:
                new_pokemon = np.random.choice(self.poke_pool)
                # If the pokemon is already in the team, replace it with a random pokemon from the pool
                while new_pokemon in team:
                    new_pokemon = np.random.choice(self.poke_pool)
                # Replace the pokemon
                team[np.where(team == pokemon)[0][0]] = new_pokemon