from __future__ import annotations

import random
from typing import Callable

import numpy as np

from p2lab.genetic.fitness import BTmodel
from p2lab.pokemon.battle import run_battles
from p2lab.pokemon.team import Team


# Psuedocode for the genetic algorithm, some placeholder functions below to
# be deleted
def genetic_team(
    pokemon_population: list[str],  # list of all valid pokemon names
    num_pokemon: int = 6,
    num_teams: int = 100,
    fitness_func: Callable[[list[Team], np.ndarary, list[int]], list[float]] = BTmodel,
    max_iter: int = 500,
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
    fitness = fitness_func(teams, matches, results)

    # Genetic Loop
    for _iter in range(max_iter):
        # Crossover based on fitness func
        new_teams = crossover(teams, fitness, num_teams, num_pokemon)

        # Mutate the new teams
        teams = mutate(new_teams, p=0.1, pokemon_population=pokemon_population)  # need to parameterise mutation prob

        # Generate matches from list of teams
        matches = generate_matches(teams)

        # Run simulations
        results = run_battles(matches)

        # Compute fitness
        fitness = fitness_func(teams, matches, results)


# Placeholders:


# Consider seeding this?
def generate_teams(
    pokemon_population: list[str],
    num_pokemon: int,
    num_teams: int,
) -> list[Team]:
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
    """
    return np.zeros(shape=(len(teams), 2))


def crossover(
    teams: list[Team], fitness: list[float], num_teams: int, num_pokemon: int
) -> list[Team]:
    """
    Given a list of teams and a fitness score for each team, generate
    new teams.

    The fitness score determines the likelihood of selection when
    generating 2 teams from 2 old ones.


    """
    print(fitness)  # delete this line - it's here to avoid pre-commit checks
    new_teams: list[Team] = []

    # Assume num_teams is even, sample w/ replacement
    for _i in range(int(num_teams / 2)):
        teams_old = random.sample(teams, k=2)
        team1_old = teams_old[0]
        team2_old = teams_old[1]

        team1_pokemon = team1_old.pokemon
        team2_pokemon = team2_old.pokemon

        # Randomly pick locus
        locus = random.sample(range(0, num_pokemon), k=1)[0]

        # Check that the sliciing here works but you get the idea
        team1_new_pokemeon = team1_pokemon[0:locus] + team2_pokemon[locus:num_pokemon]
        team2_new_pokemeon = team2_pokemon[0:locus] + team1_pokemon[locus:num_pokemon]

        team1_new = Team(pokemon=team1_new_pokemeon)
        team2_new = Team(pokemon=team2_new_pokemeon)

        new_teams = [*new_teams, team1_new, team2_new]

    return new_teams


def mutate(teams: list[Team], p: float, pokemon_population: list[str]) -> list[Team]:
    for team in teams:
        team.random_mutate(
            p=p, pokemon_population=pokemon_population
        )  # will need to be parameterised with a prob
    return teams
