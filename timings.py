from __future__ import annotations

import random
import time
from itertools import permutations

import numpy as np

from p2lab.genetic.fitness import BTmodel, win_percentages
from p2lab.genetic.matching import dense
from p2lab.genetic.operations import build_crossover_fn, mutate, slot_swap
from p2lab.team import Team

# Constants
N_TEAM = 3
N_POKEMON = 3
POP_SIZE = 151
BATTLES_PER_PAIR = 10
NUM_ROUND = 1000


# Function to check timings
def main():
    # Simulate teams
    poke_pop = list(range(POP_SIZE))
    teams = []
    for _iter in range(N_TEAM):
        teams.append(Team(random.choices(poke_pop, k=N_POKEMON)))

    # Run for many rounds
    for round in range(NUM_ROUND):
        # Log
        print(f"Round: {round}")

        # All vs all matches
        matches = dense(teams)
        n_match = matches.shape[0]

        # Simulate Results
        perms = np.array(list(permutations(range(BATTLES_PER_PAIR + 1), 2)))
        outcomes = perms[np.sum(perms, axis=1) == 3, :]
        num_outcome = outcomes.shape[1]
        results = outcomes[random.choices(range(num_outcome), k=n_match), :]

        # Logging step 1
        print(f"Number of matches: {n_match}")
        print(f"Number of battles per match: {BATTLES_PER_PAIR}")

        # Timings: Win Percent Fitness
        t0_wp = time.perf_counter()
        fitness_wp = win_percentages(
            teams=teams,
            matches=matches,
            results=results,
        )
        t1_wp = time.perf_counter()
        print(f"Ran win_percentages fitness in {t1_wp - t0_wp:0.4f} seconds")

        # Timings: BT
        t0_bt = time.perf_counter()
        _fitness_bt = BTmodel(
            teams=teams,
            matches=matches,
            results=results,
            max_iter=50,
            tol=0.01,
        )
        t1_bt = time.perf_counter()
        print(f"Ran BTmodel fitness in {t1_bt - t0_bt:0.4f} seconds")

        # Timings: Crossover
        t0_slot = time.perf_counter()
        crossover_fn = build_crossover_fn(slot_swap, k=1)
        _teams_new = crossover_fn(
            teams=teams,
            fitness=fitness_wp,
            num_teams=N_TEAM,
            num_pokemon=N_POKEMON,
            crossover_prob=0.5,
            allow_all=False,
        )
        t1_slot = time.perf_counter()
        print(f"Ran slot crossover in {t1_slot - t0_slot:0.4f} seconds")

        # Timings: Mutation
        t0_mut = time.perf_counter()
        mutate(
            teams=teams,
            num_pokemon=N_POKEMON,
            mutate_prob=0.1,
            pokemon_population=poke_pop,
            allow_all=False,
            k=1,
        )
        t1_mut = time.perf_counter()
        print(f"Ran mutate in {t1_mut - t0_mut:0.4f} seconds")


if __name__ == "__main__":
    main()
