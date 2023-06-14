"""
"""
import socket
import numpy as np 
from itertools import combinations
from poke_env.player import Player, RandomPlayer
from poke_env import PlayerConfiguration
from tqdm import tqdm
class PokeEnv:
    def __init__(self, n_battles=100):
        self.p1 = RandomPlayer(PlayerConfiguration("Player 1", None), battle_format="gen8doublescustomgame")
        self.p2 = RandomPlayer(PlayerConfiguration("Player 2", None),battle_format="gen8doublescustomgame")
        self.n_battles = n_battles
        pass

    async def evaluate_teams(self, teams):
        match_ups = [c for c in combinations(np.arange(len(teams)), 2)]

        for t1, t2 in match_ups:
            res1, res2 = await self.battle(teams[t1], teams[t2])
            teams[t1].set_fitness(res1)
            teams[t2].set_fitness(res2)


    async def battle(self, team1, team2):
        self.p1.update_team("]".join([mon.formatted for mon in team1.get_teamlist()]))
        self.p2.update_team("]".join([mon.formatted for mon in team2.get_teamlist()]))
        await self.p1.battle_against(self.p2, n_battles=self.n_battles)
        return self.p1.n_won_battles, self.p2.n_won_battles
