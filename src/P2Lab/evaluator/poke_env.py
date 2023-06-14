"""
"""
from __future__ import annotations

from itertools import combinations

import numpy as np
from poke_env import PlayerConfiguration
from poke_env.player import RandomPlayer
from tqdm import tqdm

SHOW_MATCH_PROGRESS = True


class PokeEnv:
    def __init__(self, n_battles=100, battle_format="gen7anythinggoes"):
        self.p1 = RandomPlayer(
            PlayerConfiguration("Player 1", None), battle_format=battle_format
        )
        self.p2 = RandomPlayer(
            PlayerConfiguration("Player 2", None), battle_format=battle_format
        )
        self.n_battles = n_battles
        pass

    async def evaluate_teams(self, teams):
        match_ups = list(combinations(np.arange(len(teams)), 2))

        for t1, t2 in tqdm(match_ups) if SHOW_MATCH_PROGRESS else match_ups:
            res1, res2 = await self.battle(teams[t1], teams[t2])
            teams[t1].set_fitness(res1)
            teams[t2].set_fitness(res2)

    async def battle(self, team1, team2):
        self.p1.update_team(team1.to_packed_str())
        self.p2.update_team(team2.to_packed_str())
        await self.p1.battle_against(self.p2, n_battles=self.n_battles)
        return self.p1.n_won_battles, self.p2.n_won_battles
