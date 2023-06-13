"""
"""
import numpy as np 
from itertools import combinations
from poke_env.player import Player, RandomPlayer

class PokeEnv:
    def __init__(self, n_battles=100):
        self.n_battles = n_battles
        pass

    async def evaluate_teams(self, teams):
        match_ups = combinations(np.arange(len(teams)), 2)
        for t1, t2 in match_ups:
            res1, res2 = await self.battle(teams[t1], teams[t2])
            teams[t1].set_fitness(res1)
            teams[t2].set_fitness(res2)

    async def battle(self, team1, team2):
        p1, p2 = RandomPlayer(team=team1), RandomPlayer(team=team2)
        await p1.battle_against(p2, n_battles=self.n_battles)
        return p1.n_won_battles, p2.n_won_battles
