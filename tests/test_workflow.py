from __future__ import annotations

import numpy as np
import pytest

from p2lab.genetic.genetic import genetic_algorithm
from p2lab.genetic.operations import (
    build_crossover_fn,
    locus_swap,
    sample_swap,
    slot_swap,
)
from p2lab.pokemon.premade import gen_1_pokemon
from p2lab.pokemon.teams import generate_teams, import_pool


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("team_size", "crossover_fn"),
    [
        (2, None),
        (6, locus_swap),
        (6, slot_swap),
        (6, sample_swap),
    ],
)
async def test_main_loop(team_size, crossover_fn):
    num_teams = 10
    # generate the pool
    pool = import_pool(gen_1_pokemon())
    seed_teams = generate_teams(pool, num_teams, team_size, unique=True)
    crossover_fn = build_crossover_fn(crossover_fn)
    # run the genetic algorithm
    teams, fitnesses = await genetic_algorithm(
        pokemon_pool=pool,
        seed_teams=seed_teams,
        num_teams=num_teams,
        team_size=team_size,
        num_generations=3,
        progress_bars=False,
        mutate_with_fitness=crossover_fn is None,
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
