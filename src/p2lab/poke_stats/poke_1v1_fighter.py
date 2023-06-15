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

import pickle
from itertools import combinations_with_replacement as cwr

import numpy as np

# Actual code ==========================================================================

# def gen_pop() -> list(poke_objects):
#     """Generate the population of 151 pokemon objects ready to fight.

#     NB: This can be done more explicity here, i.e. implement the rejection sampling
#         in this script, but I will simplify away from that for now.
#     """
#     return pop_gen.gen_pop

# # def duel_to_convergence(
#     poke_1: poke_object,
#     poke_2: poke_object,
#     var_threshold: float,
#     look_back: int,
#     cutoff: int,
# ) -> tuple(float, float):
#     """DUEL TO THE DEATH! (or at least a converged win ratio.....)

#         For two pokemon, duel until the win ration converges or cutoff is reached.
#         Return ratios scaled by number of fights.

#         TODO: make lookback function of number of fights?

#     Args:
#         poke_1 (poke_object): pokemon_1      (GLADIATOR, READY!)
#         poke_2 (poke_object): pokemon_2      (GLADIATOR, READY!)
#         var_threshold (float): threshold for convergence of win ratio variance.
#         look_back: how man previous ratio values to consider.
#         cutoff: max iters to run this.

#     Returns:
#         (poke_wins_1, poke_wins_2) tuple(float, float):
#             poke_wins_i = (no wins of poke_i) / (no of duels)
#     """
#     count = 0
#     variance = 100
#     poke_win_1 = 1  # Start with one win each to avoid /0 errors....
#     poke_win_2 = 1
#     ratios = []
#     while (count < cutoff) or (variance > var_threshold):
#         count += 1
#         if duel(poke_1, poke_2):
#             poke_win_1 += 1
#         else:
#             poke_win_2 += 1
#         ratios.append(poke_win_1 / poke_win_2)
#         if len(ratios) < look_back:
#             variance = np.var(ratios)
#         else:
#             variance = np.var(ratios[-look_back:])
#     return poke_win_1 / count, poke_win_2 / count

# def duel(poke_1: poke_object, poke_2: poke_object) -> bool:
#     """Simulate a fight between a pair of pokemon, with a result of True if poke_1
#         wins.

#     Args:
#         poke_1 (poke_object): pokemon_1     (IN THE RED CORNER)
#         poke_2 (poke_object): pokemon_2     (IN THE BLUE CORNER)

#     Returns:
#         bool: True if pokemon 1 is victorious.
#     """
#     winner = fight_sim.fight(poke_1, poke_2)
#     return winner == poke_1


# def main(**kwargs):
#     # Generate a population
#     poke_pop = gen_pop

#     # Instantiate results matrix (we know n = 151)
#     res_arr = np.zeros(151, 151)

#     # Duel to convergence to get stats
#     for dueling_partners_id in cwr(list(range(len(poke_pop))), 2):
#         i, j = dueling_partners_id
#         poke_ratio_1, poke_ratio_2 = duel_to_convergence(
#             poke_pop[i],
#             poke_pop[j],
#             kwargs["var_threshold"],
#             kwargs["look_back"],
#             kwargs["cutoff"],
#         )
#         if i == j:
#             res_arr[i, i] += poke_ratio_1
#         res_arr[i, j] += poke_ratio_1
#         res_arr[j, i] += poke_ratio_2

#     # Average over to get stats
#     avg_win_ratio = np.mean(res_arr, axis=0)
#     return avg_win_ratio

# Dummy Code ===========================================================================


def dummy_gen_pop() -> list(str):
    """Create a dummy list of pokemon."""
    with open("poke_base_stats.pkl", "rb") as f:
        p_dict = pickle.load(f)
    return p_dict


def dummy_duel(poke_1: str, poke_2: str) -> bool:
    """Dummy duel method"""
    rng = np.random.default_rng(seed=int("".join(str(ord(c)) for c in poke_1 + poke_2)))
    prob = rng.random(1)[0]
    # print(prob)
    # print(1 - prob)
    return rng.choice(a=[True, False], p=[prob, 1 - prob])


def dummy_duel_to_convergence(
    poke_1: str,
    poke_2: str,
    var_threshold: float,
    look_back: int,
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
    variance = 100
    poke_win_1 = 1  # Start with one win each to avoid /0 errors....
    poke_win_2 = 1
    ratios = []
    # print(cutoff)
    while count < cutoff and variance > var_threshold:  # or variance
        # print(count)
        count += 1
        if dummy_duel(poke_1, poke_2):
            poke_win_1 += 1
        else:
            poke_win_2 += 1
        ratios.append(poke_win_1 / poke_win_2)
        if count > 2:
            if len(ratios) < look_back:
                variance = np.var(ratios)
            else:
                variance = np.var(ratios[-look_back:])
    print(variance)
    return poke_win_1 / count, poke_win_2 / count


def main(**kwargs):
    # Generate a population
    poke_dict = dummy_gen_pop()
    poke_names = list(poke_dict.keys())

    # Instantiate results matrix (we know n = 151)
    res_arr = np.zeros((151, 151))

    # Duel to convergence to get stats
    for dueling_partners_id in cwr(list(range(len(poke_names))), 2):
        i, j = dueling_partners_id
        print(f"IN THE RED CORNER: {poke_names[i]}")
        print(f"IN THE BLUE CORNER: {poke_names[j]}")
        poke_ratio_1, poke_ratio_2 = dummy_duel_to_convergence(
            poke_names[i],
            poke_names[j],
            kwargs["var_threshold"],
            kwargs["look_back"],
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
    print("for Magikarp:")
    print(poke_dict["magikarp"])
    return poke_dict


if __name__ == "__main__":
    # Pars hardcoded in for now as should be single run.
    pars = {"var_threshold": 1e-14, "look_back": 2, "cutoff": 100}

    main(**pars)
