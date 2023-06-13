"""
The team builder
"""
from __future__ import annotations

import sys
from subprocess import check_output

import numpy as np
from poke_env.teambuilder import Teambuilder


class Builder(Teambuilder):
    """
    The team builder
    """
    def __init__(self, N_seed_teams=2, teams=None, format="gen2randombattle"):
        if teams:
            self.teams = [
                self.join_team(self.parse_showdown_team(team)) for team in teams
            ]
        else:
            self.teams = []
            for _ in range(N_seed_teams):
                self.teams.append(self.parse_showdown_team(check_output(f"pokemon-showdown generate-team {format}| pokemon-showdown export-team", shell=True).decode(sys.stdout.encoding)))
        self.poke_pool = np.array(self.teams).flatten()
        
    def build_N_teams_from_poke_pool(self, N_teams):
        self.teams = [np.random.choice(self.poke_pool, size=6, replace=False) for _ in range(N_teams)]
        

    def yield_team(self):
        return self.teams[np.random.choice(len(self.teams))]

    def generate_new_teams(self):
        self.breed_teams()
        self.mutate_teams()


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