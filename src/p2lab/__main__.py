from __future__ import annotations

import asyncio

import numpy as np

from p2lab.genetic.genetic import genetic_algorithm
from p2lab.pokemon.premade import gen_1_pokemon
from p2lab.pokemon.teams import import_pool


async def main_loop(num_teams, team_size, num_generations, unique):
    # generate the pool
    pool = import_pool(gen_1_pokemon())
    # crossover_fn = build_crossover_fn(locus_swap, locus=0)
    # run the genetic algorithm
    teams, fitnesses = await genetic_algorithm(
        pokemon_pool=pool,
        num_teams=num_teams,
        team_size=team_size,
        num_generations=num_generations,
        progress_bars=True,
        unique_teams=unique,
        mutate_with_fitness=True,
        mutate_k=1,
    )

    print("Best team:")
    best_team = teams[np.argmax(fitnesses)]
    fitness = fitnesses[np.argmax(fitnesses)]
    for mon in best_team.pokemon:
        print(mon.formatted)

    print(f"Fitness: {fitness}")

    print("Worst team:")

    worst_team = teams[np.argmin(fitnesses)]
    fitness = fitnesses[np.argmin(fitnesses)]
    for mon in worst_team.pokemon:
        print(mon.formatted)

    print(f"Fitness: {fitness}")


def main():
    num_teams = 30
    team_size = 2
    num_generations = 10
    unique = True
    asyncio.get_event_loop().run_until_complete(
        main_loop(num_teams, team_size, num_generations, unique)
    )


if __name__ == "__main__":
    main()
