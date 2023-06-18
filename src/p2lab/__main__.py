from __future__ import annotations

import asyncio

from p2lab.genetic.genetic import genetic_algorithm
from p2lab.genetic.operations import locus_swap
from p2lab.pokemon.premade import gen_1_pokemon
from p2lab.pokemon.teams import import_pool


async def main_loop(num_teams: int = 10, team_size: int = 6, num_generations: int = 10):
    # generate the pool
    pool = import_pool(gen_1_pokemon())
    # run the genetic algorithm
    best_team = await genetic_algorithm(
        pokemon_pool=pool,
        num_teams=num_teams,
        team_size=team_size,
        num_generations=num_generations,
        progress_bars=True,
        crossover_fn=locus_swap,
    )

    # print the best team
    print(best_team)


def main():
    asyncio.get_event_loop().run_until_complete(main_loop())


if __name__ == "__main__":
    main()
