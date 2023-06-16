# 1v1 fights for the pokemon for stats.
# Author: Edmund Dable-Heath
"""
    Setting each of the 150 pokemon to fight each other pokemon until either a cutoff is
    reached or the variation of the win ratio over a history of s fights falls below a
    threshold.
"""

# Imports include reference to potential scripts
# import pop_gen
# import fight_sim
from __future__ import annotations

import asyncio
import pickle
import sys
from itertools import combinations_with_replacement as cwr

import numpy as np

from run.py import run_battles

sys.path.insert(1, "/Users/edable-heath/Documents/HackWeek/P2-Lab")


# Actual code ==========================================================================


def gen_pop() -> list(poke_objects):
    """Generate the population of 151 pokemon objects ready to fight.

    NB: This can be done more explicity here, i.e. implement the rejection sampling
        in this script, but I will simplify away from that for now.
    """
    return pop_gen.gen_pop


async def duel(poke_1, poke_2, player_1, player_2) -> bool:
    """Simulate a fight between a pair of pokemon, with a result of True if poke_1
        wins.

    Args:
        poke_1 (poke_object): pokemon_1     (IN THE RED CORNER)
        poke_2 (poke_object): pokemon_2     (IN THE BLUE CORNER)

    Returns:
        bool: True if pokemon 1 is victorious.
    """
    return bool(run_battles([[0, 1]], [poke_1, poke_2], player_1, player_2, 1)[0])


def duel_to_convergence(
    poke_1,
    poke_2,
    cutoff: int,
) -> tuple(float, float):
    """DUEL TO THE DEATH! (or at least a converged win ratio.....)

        For two pokemon, duel until the win ration converges or cutoff is reached.
        Return ratios scaled by number of fights.

        TODO: make lookback function of number of fights?

    Args:
        poke_1 (poke_object): pokemon_1      (GLADIATOR, READY!)
        poke_2 (poke_object): pokemon_2      (GLADIATOR, READY!)
        var_threshold (float): threshold for convergence of win ratio variance.
        look_back: how man previous ratio values to consider.
        cutoff: max iters to run this.

    Returns:
        (poke_wins_1, poke_wins_2) tuple(float, float):
            poke_wins_i = (no wins of poke_i) / (no of duels)
    """
    count = 0
    poke_win_1 = 0
    poke_win_2 = 0
    while count < cutoff:
        count += 1
        if duel(poke_1, poke_2):
            poke_win_1 += 1
        else:
            poke_win_2 += 1
    return poke_win_1 / count, poke_win_2 / count


async def main(**kwargs):
    # Generate a population
    pokemons = gen_pop()
    poke_num = len(pokemons)

    # Read the poke_dict for results
    with open("poke_base_stats.pkl", "rb") as f:
        poke_dict = pickle.load(f)
    poke_names = list(poke_dict.keys())

    # Instantiate results matrix (we know n = 151)
    res_arr = np.zeros((poke_num, poke_num))

    # Duel to convergence to get stats
    for dueling_partners_id in cwr(list(range(len(pokemons))), 2):
        i, j = dueling_partners_id
        # print(f"IN THE RED CORNER: {poke_names[i]}")
        # print(f"IN THE BLUE CORNER: {poke_names[j]}")
        poke_ratio_1, poke_ratio_2 = duel_to_convergence(
            pokemons[i],
            pokemons[j],
            kwargs["cutoff"],
        )
        if i == j:
            res_arr[i, i] += poke_ratio_1
        res_arr[i, j] += poke_ratio_1
        res_arr[j, i] += poke_ratio_2

    # Average over to get stats
    avg_win_ratio = np.mean(res_arr, axis=0)
    for i in range(len(poke_names)):
        poke_dict[poke_names[i]]["average_win_ratio"] = avg_win_ratio[i]

    # print(poke_dict)
    # print("for Magikarp:")
    # print(poke_dict["magikarp"])

    # Write poke dict to storage
    with open("poke_fight_results.pkl", "wb") as fp:
        pickle.dump(poke_dict, fp)
    return poke_dict


if __name__ == "__main__":
    # Pars hardcoded in for now as should be single run.
    pars = {"cutoff": 100}

    asyncio.get_event_loop().run_until_complete(main(**pars))
