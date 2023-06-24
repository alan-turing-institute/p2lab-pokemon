from __future__ import annotations

import math
import random
from typing import Callable

import numpy as np

from p2lab.pokemon.teams import Team


### Selection Operation
def selection(
    teams: list[Team],
    fitness: np.ndarray,
    num_teams: int,
) -> tuple[list[Team], np.ndarray]:
    """
    This function performs the selection genetic operation. Its purpose is to
    pass on good chromosomes/genes to the next population as a function of
    fitness.

    Args:
        teams: A list containing all team objects
        fitness: A numpy array of shape (N_team,) containing team fitness
                    scores
        num_teams: The number of teams
    """

    # Sample indices with replacement to produce new teams + fitnesses
    old_indices = list(range(num_teams))
    new_indices = random.choices(old_indices, k=num_teams)

    # New teams and fitness
    new_teams = [teams[i] for i in new_indices]
    new_fitness = fitness[new_indices]

    # Return
    return new_teams, new_fitness


### Crossover Operations
def build_crossover_fn(
    crossover_method: Callable,
    **kwargs,
) -> Callable:
    """
    This function constructs a crossover function based on its inputs.

    Arguments:
        crossover_method: Function that defines the method of crossover
                          used. See below
        **kwargs: Arguments passed to the crossover method
    """

    def crossover_fn(
        teams: list[Team],
        num_teams: int,
        num_pokemon: int,
        crossover_prob: float,
        allow_all: bool = False,
    ) -> list[Team]:
        """
        A crossover function.

        Args:
            teams: A list containing all team objects
            fitness: A numpy array of shape (N_team,) containing team fitness
                     scores
            num_teams: The number of teams
            num_pokemon: The number of Pokemon in each team
            crossover_prob: The crossover probability. Defines the chance at
                            which two teams are crossed over instead of simply
                            being kept. Should be reasonably high
            allow_all: Allows all members of a team to be crossed over when randomly
                       choosing the number. Should be True if num_pokemon is < 3.
        """

        # Output vector
        new_teams = []

        # Each loop produces 2 new teams, so needs half this number to produce
        # enough teams.
        for i in range(math.ceil(num_teams / 2)):
            # Loop over two teams at a time
            team1_old = teams[i * 2]
            team2_old = teams[i * 2 + 1]

            # Extract list of pokemon to crossover
            team1_pokemon = team1_old.pokemon
            team2_pokemon = team2_old.pokemon

            # Crossover occurs with parameterised probability
            crossover = np.random.choice(
                a=[True, False], p=[crossover_prob, 1 - crossover_prob]
            )

            # Perform crossover
            if crossover:
                team1_pokemon, team2_pokemon = crossover_method(
                    team1=team1_pokemon,
                    team2=team2_pokemon,
                    num_pokemon=num_pokemon,
                    allow_all=allow_all,
                    **kwargs,
                )

            # Build new teams
            team1_new = Team(pokemon=team1_pokemon)
            team2_new = Team(pokemon=team2_pokemon)

            # Append to output
            new_teams = [*new_teams, team1_new, team2_new]

        # Check output is correct length. One team will need
        # removing if N_teams is an odd number. Probably just
        # best to run an even number of teams lol
        if num_teams % 2 != 0:
            new_teams.pop()

        return new_teams

    return crossover_fn


def locus_swap(
    team1: list[str],
    team2: list[str],
    num_pokemon: int,
    allow_all: bool,
    locus: int = None,
) -> tuple(list[str], list[str]):
    """
    A method of performing the crossover. Pick a 'locus' point: this
    becomes the point at which two input lists are sliced.

    Two new lists are then produced from the sliced lists.

    If no locus point is supplied, this will be chosen randomly.

    Args:
        team1: List of pokemon in team 1
        team2: List of pokemon in team 2
        num_pokemon: Number of pokemon in each team
        allow_all: Whether to allow all pokemon to be swapped when ranomly
                   choosing the locus point.
        locus: Locus point at which to perform swaps
    """

    # If locus has not been chosen, randomly choose
    if locus is None:
        # If allow_all is true, the teams may just completely swap members
        # or not swap at all. This changes the higher level crossover probs!
        n = 0 if allow_all else 1
        locus = random.sample(range(n, num_pokemon - n), k=1)[0]

    # Check validity of locus
    assert locus > 0
    assert locus < (num_pokemon - 1)

    # Split teams into halves
    team1_p1 = team1[0:locus]
    team1_p2 = team1[locus:num_pokemon]
    team2_p1 = team2[0:locus]
    team2_p2 = team2[locus:num_pokemon]

    # Recombine
    team1_new = [*team1_p1, *team2_p2]
    team2_new = [*team2_p1, *team1_p2]

    return team1_new, team2_new


def slot_swap(
    team1: list[str],
    team2: list[str],
    num_pokemon: int,
    allow_all: bool,
    k: int = None,
) -> tuple(list[str], list[str]):
    """
    A method of performing the crossover. This method randomly
    chooses k points in the lists, then swaps them over.

    Two new lists are then produced from the sliced lists.

    If a value for k is not chosen, it will be chosen randomly.

    Args:
        team1: List of pokemon in team 1
        team2: List of pokemon in team 2
        num_pokemon: Number of pokemon in each team
        allow_all: Whether to allow all pokemon to be swapped when ranomly
                   choosing the value of k.
        k: Number of slots in which to switch pokemon
    """

    # If locus has not been chosen, choose
    if k is None:
        # If allow_all is true, the teams may just completely swap members
        # or not swap at all. This changes the higher level crossover probs!
        n = 0 if allow_all else 1
        k = random.sample(range(n, num_pokemon - n), k=1)[0]

    # Check validity of locus
    assert k > 0
    assert k < (num_pokemon - 1)

    # Select swap indices
    indices = list(range(num_pokemon))
    swap_indices = random.sample(indices, k=k)

    # Temporarily convert teams to np.arrays because list indexing in Python
    # still hasn't caught up to R
    team1 = np.array(team1)
    team2 = np.array(team2)

    # Get pokemon to swap out
    team1_swaps = team1[swap_indices]
    team2_swaps = team2[swap_indices]

    # Swap the new pokemon in
    team1[swap_indices] = team2_swaps
    team2[swap_indices] = team1_swaps

    return list(team1), list(team2)


def sample_swap(
    team1: list[str],
    team2: list[str],
    num_pokemon: int,
    with_replacement: bool = False,
    **kwargs,
) -> tuple(list[str], list[str]):
    """
    A method of performing the crossover. This method treats the pokemon
    in the two teams as a population and samples from them to create two new
    teams.

    Can be done with or without replacement.

    Args:
        team1: List of pokemon in team 1
        team2: List of pokemon in team 2
        num_pokemon: Number of pokemon in each team
        with_replacement: Whether to sample with or without replacement.
    """

    # Population to sample from and indices
    population = np.array([*team1, *team2])
    indices = list(range(num_pokemon * 2))

    # Sample indices (since teams may have overlapping members)
    team1_indices = np.random.choice(
        indices,
        size=num_pokemon,
        replace=with_replacement,
    )

    # For team 2, change behaviour conditional on replacement
    if with_replacement:
        team2_indices = list(
            np.random.choice(
                indices,
                size=num_pokemon,
                replace=with_replacement,
            )
        )
    else:
        team2_indices = list(set(indices) - set(team1_indices))

    # Return teams
    return list(population[team1_indices]), list(population(team2_indices))


### Mutation Operations
def mutate(
    teams: list[Team],
    num_pokemon: int,
    mutate_prob: float,
    pokemon_population: list[str],
    allow_all: bool,
    k: int = None,
):
    """
    A mutation operation. At random, k members of a team are swapped with k
    pokemeon in the wider population of pokemon.

    Args:
        teams: A list of teams
        num_pokemon: The number of pokemon in each team
        mutate_prob: Probability of mutation to occur
        pokemon_population: The population of all possible pokemon
        allow_all: Whether to allow all pokemon to be swapped when ranomly
                   choosing the locus point.
        k: Number of team members to mutate. If set to None, this number will
           be random.
    """
    for team in teams:
        # Each team faces a random chance of mutation
        if np.random.choice([True, False], size=None, p=[mutate_prob, 1 - mutate_prob]):
            # If k has not been chosen, choose randomly how many team members to mutate
            if k is None:
                # If allow_all is true, the teams may just completely swap members
                # or not swap at all. This changes the higher level crossover probs!
                n = 0 if allow_all else 1
                k = random.sample(range(n, num_pokemon - n), k=1)[0]

            # Randomly swap k members of the team out with pokemon from the general pop
            mutate_indices = np.random.choice(range(num_pokemon), size=k, replace=False)

            new_pokemon = np.random.choice(
                pokemon_population, size=k, replace=False
            )  # open to parameterising the replace
            team.pokemon[mutate_indices] = new_pokemon

    return teams


def fitness_mutate(
    teams: list[Team],
    num_pokemon: int,
    fitness: np.array,
    pokemon_population: list[str],
    allow_all: bool,
    k: int = None,
):
    """
    A mutation operation. Does the same as regular mutation, except that
    mutate probabilites are now inverse to fitness scores.

    Should either be used prior to crossover, or without using any kind of
    crossover.

    Args:
        teams: A list of teams
        num_pokemon: The number of pokemon in each team
        fitness: Team fitnesses
        pokemon_population: The population of all possible pokemon
        allow_all: Whether to allow all pokemon to be swapped when ranomly
                   choosing the locus point.
        k: Number of team members to mutate. If set to None, this number will
           be random.
    """
    new_teams = []

    for index, team in enumerate(teams):
        # Each team faces a random chance of mutation
        if np.random.choice(
            [True, False], size=None, p=[1 - fitness[index], fitness[index]]
        ):
            # If k has not been chosen, choose randomly how many team members to mutate
            if k is None:
                # If allow_all is true, the teams may just completely swap members
                # or not swap at all. This changes the higher level crossover probs!
                n = 0 if allow_all else 1
                k = random.sample(range(n, num_pokemon - n), k=1)[0]

            # Randomly swap k members of the team out with pokemon from the general pop
            # IMPORTANT: ensure that no team has the same pokemon in it
            mutate_indices = np.random.choice(range(num_pokemon), size=k, replace=False)
            new_pokemon = np.random.choice(
                pokemon_population,
                size=k,
                replace=False,  # replace would create duplicates
            )  # open to parameterising the replace
            # check that these new pokemon are not already in the team
            names = [p.formatted.split("|")[0] for p in new_pokemon]
            while any(name in team.names for name in names):
                print("Found duplicate pokemon, resampling...")
                new_pokemon = np.random.choice(
                    pokemon_population,
                    size=k,
                    replace=False,  # replace would create duplicates
                )
                names = [p.formatted.split("|")[0] for p in new_pokemon]
            # Create new team with the mutated pokemon and the rest of the team
            old_pokemon = np.array(team.pokemon)[
                [i for i in range(num_pokemon) if i not in mutate_indices]
            ]
            new_team = [*new_pokemon, *old_pokemon]
            new_teams.append(Team(new_team))
        else:
            new_teams.append(team)

    return new_teams
