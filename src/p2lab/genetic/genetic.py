from __future__ import annotations

from typing import Callable

import numpy as np

from p2lab.genetic.fitness import BTmodel
from p2lab.pokemon.team import Team


# Psuedocode for the genetic algorithm, some placeholder functions below to
# be deleted
def genetic_team(
    pokemon_population: list[str],  # list of all valid pokemon names
    generate_teams: Callable,
    generate_matches: Callable,
    run_battles: Callable,
    crossover: Callable,
    mutate: Callable,
    fitness_func: Callable[[list[Team], np.ndarray, list[int]], list[float]] = BTmodel,
    num_pokemon: int = 6,
    num_teams: int = 100,
    max_evolutions: int = 500,
    **kwargs,
) -> None:
    # Generate initial group of teams and matchups
    teams = generate_teams(
        pokemon_population,
        num_pokemon,
        num_teams,
    )
    matches = generate_matches(teams)

    # Run initial simulations
    results = run_battles(matches)

    # Compute fitness
    fitness = fitness_func(teams, matches, results, **kwargs)

    # Genetic Loop
    for _iter in range(max_evolutions):
        # Crossover based on fitness func
        new_teams = crossover(teams, fitness, num_teams, num_pokemon)

        # Mutate the new teams
        teams = mutate(
            new_teams, p=0.1, pokemon_population=pokemon_population
        )  # need to parameterise mutation prob

        # Generate matches from list of teams
        matches = generate_matches(teams)

        # Run simulations
        results = run_battles(matches)

        # Compute fitness
        fitness = fitness_func(teams, matches, results, **kwargs)
