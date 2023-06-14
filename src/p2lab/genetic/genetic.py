from __future__ import annotations

import random
from typing import Callable

import numpy as np

from p2lab.genetic.matching import dense
from p2lab.genetic.operations import fitness_mutate, mutate
from p2lab.pokemon.battle import run_battles
from p2lab.pokemon.team import Team


# Psuedocode for the genetic algorithm, some placeholder functions below to
# be deleted
def genetic_team(
    pokemon_population: list[str],  # list of all valid pokemon names
    num_pokemon: int,
    num_teams: int,
    fitness_fn: Callable,
    crossover_fn: Callable = None,
    crossover_prob: float = 0.95,
    mutate_prob: float = 0.01,
    mutate_with_fitness: bool = False,
    mutate_k=None,
    allow_all=False,
    num_evolutions: int = 500,
    fitness_kwargs: dict | None = None,
) -> None:
    """
    A genetic evolution algorithm for optimising pokemon team selection.

    Users specify the population of pokemon to optimise over, the number of pokemon per
    team, the number of teams, and the number of evolutions to run.

    Users also need to define a fitness function, a crossover function, crossover and mutation
    probabilities, and if allowing a random number of pokemon to be crossed/mutated, whether to
    allow this to be random.

    Users can choose to allow mutation probability to occur inversely to fitness instead of
    performing a crossover + mutation step if desired.

    Args:
        pokemon_population: A list of strings containing all valid pokemon names for the population
        num_pokemon: Number of pokmeon in each team
        num_teams: Number of pokemon teams to generate
        fitness_fn: A function to define fitness scores after each round
        crossover_fn: A function that defines the crossover step in each round. Set to
                      None if this step should be ignored.
        crossover_prob: Crossover probability. Chance two teams will be crossed over
                        in the crossover step, as opposed to simply moving to the next
                        generation. Defaults to 0.95 as should be high.
        mutate_prob: Probability each team has of randomly mutating. Defaults to 0.01 as
                     should be low to avoid sub-optimal solutions.
        mutate_with_fitness: Instead of optimising by crossover followed by mutation,
                             instead uses a mutation function defined by fitness scores.
                             Crossover will not be used as fitness scores are invalid
                             post-crossover. Defaults to False.
        mutate_k: Number of genes to randomly mutate. Will be randomly chosen if set to
                  None.
        allow_all: When randomly choosing the number of pokemon to crossover and mutate,
                   determines whether the whole team can be crossed/mutated. Should be set
                   to true when num_pokemon < 3. Redundant if the number of swaps/
                   mutations is is not random.
        num_evolutions: Number of evolutions to run the model for. The more the better.
    """
    # Some quick checks
    assert mutate_with_fitness is True or crossover_fn is not None  # you need one!
    assert mutate_prob > 0
    assert mutate_prob < 1
    assert crossover_prob > 0
    assert crossover_prob <= 1

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
    if fitness_kwargs is None:
        fitness_kwargs = {}
    fitness = fitness_fn(teams, matches, results, **fitness_kwargs)

    # Genetic Loop
    for _iter in range(num_evolutions):
        # If mutating with fitness, skip the crossover step. Otherwise, crossover +
        # mutate.
        if mutate_with_fitness:
            teams = fitness_mutate(
                teams=teams,
                num_pokemon=num_pokemon,
                fitness=fitness,
                pokemon_population=pokemon_population,
                allow_all=allow_all,
                k=mutate_k,
            )

        else:
            # Crossover based on fitness func
            new_teams = crossover_fn(
                teams=teams,
                fitness=fitness,
                num_teams=num_teams,
                num_pokemon=num_pokemon,
                crossover_prob=crossover_prob,
                allow_all=allow_all,
            )

            # Mutate the new teams
            teams = mutate(
                teams=new_teams,
                num_pokemon=num_pokemon,
                mutate_prob=mutate_prob,
                pokemon_population=pokemon_population,
                allow_all=allow_all,
                k=mutate_k,
            )

        # Generate matches from list of teams
        matches = generate_matches(teams)

        # Run simulations
        results = run_battles(matches)

        # Compute fitness
        fitness = fitness_fn(teams, matches, results, **fitness_kwargs)


# Consider seeding this?
def generate_teams(
    pokemon_population: list[str],
    num_pokemon: int,
    num_teams: int,
) -> list[Team]:
    # TODO Use pre-made teambuilder
    teams = []
    for _i in range(num_teams):
        pokemon = random.sample(population=pokemon_population, k=num_pokemon)
        teams.append(Team(pokemon=pokemon))

    return teams


def generate_matches(teams: list[Team]) -> np.ndarray:
    """

    First column should be team IDs for player 1
    Second column should be team IDs for player 2

    Team IDs can be generated fresh each round, but we'll need to
    track them each round

    Actually, team IDs can just index the current team list?

        Outputs:

                np.ndarray shape (N_matches, 2) The columns are team ids.

    """
    return dense(teams)
