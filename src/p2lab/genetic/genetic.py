from __future__ import annotations

__all__ = ("genetic_algorithm",)

from typing import TYPE_CHECKING, Callable

from poke_env import PlayerConfiguration
from poke_env.player import SimpleHeuristicsPlayer

from p2lab.genetic.fitness import win_percentages
from p2lab.genetic.matching import dense
from p2lab.genetic.operations import fitness_mutate, mutate, selection
from p2lab.pokemon.battles import run_battles

if TYPE_CHECKING:
    from p2lab.pokemon.teams import Team


# TODO: account for team size of 1
async def genetic_algorithm(
    pokemon_pool: list[str],  # list of all valid pokemon names
    seed_teams: list[Team],  # list of teams to seed the algorithm with
    num_teams: int,
    fitness_fn: Callable = win_percentages,
    match_fn: Callable = dense,
    battles_per_match: int = 3,
    team_size: int = 6,
    battle_format: str = "gen7anythinggoes",
    crossover_fn: Callable | None = None,
    crossover_prob: float = 0.95,
    mutate_prob: float = 0.01,
    mutate_with_fitness: bool = False,
    mutate_k: int | None = None,
    allow_all: bool = False,
    num_generations: int = 500,
    fitness_kwargs: dict | None = None,
    progress_bars: bool = True,
) -> Team:
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
        pokemon_pool: A list of strings containing all valid pokemon names for the population
        team_size: Number of pokmeon in each team
        num_teams: Number of pokemon teams to generate
        match_fn: A function that generates an array of matches. See p2lab.genetic.matching for
                  choices
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
        num_generations: Number of generations to run the model for. The more the better.
    """
    # Some quick checks
    assert (
        mutate_with_fitness is True or crossover_fn is not None
    ), "Either crossover_fn must be defined or mutate_with_fitness must be True."
    assert mutate_prob > 0
    assert mutate_prob < 1
    assert crossover_prob > 0
    assert crossover_prob <= 1

    # Generate initial group of matchups
    matches = match_fn(seed_teams)

    player_1 = SimpleHeuristicsPlayer(
        PlayerConfiguration("Player 1", None), battle_format=battle_format
    )
    player_2 = SimpleHeuristicsPlayer(
        PlayerConfiguration("Player 2", None), battle_format=battle_format
    )

    print("Generation 0:")

    # Run initial simulations
    results = await run_battles(
        matches,
        seed_teams,
        player_1,
        player_2,
        battles_per_match=battles_per_match,
        progress_bar=progress_bars,
    )
    # Compute fitness
    if fitness_kwargs is None:
        fitness_kwargs = {}

    fitness = fitness_fn(seed_teams, matches, results, **fitness_kwargs)

    teams = seed_teams

    # Genetic Loop
    for i in range(num_generations):
        # Step 1: selection
        # An odd number of teams is an edge case for crossover, as it uses 2 teams
        # at a time. This adds an extra team to selection if we are using crossover.
        # the extra team will be removed by the crossover function.
        extra = num_teams % 2 - mutate_with_fitness

        # Returns new fitnesses in case we are doing fitness-mutate
        new_teams, new_fitness = selection(
            teams=teams,
            fitness=fitness,
            num_teams=num_teams + extra,
        )

        # Step 2: crossover
        # Only do this step if not mutating with fitness, as fitness scores become
        # invalid after crossover if doing so
        if not mutate_with_fitness:
            new_teams = crossover_fn(
                teams=new_teams,
                num_teams=num_teams,
                num_pokemon=team_size,
                crossover_prob=crossover_prob,
                allow_all=allow_all,
            )

        # Step 3: mutate
        # If mutating with fitness, skip the crossover step. Otherwise, crossover +
        # mutate.
        if mutate_with_fitness:
            teams = fitness_mutate(
                teams=new_teams,
                num_pokemon=team_size,
                fitness=new_fitness,
                pokemon_population=pokemon_pool,
                allow_all=allow_all,
                k=mutate_k,
            )

        else:
            # Mutate the new teams
            teams = mutate(
                teams=new_teams,
                num_pokemon=team_size,
                mutate_prob=mutate_prob,
                pokemon_population=pokemon_pool,
                allow_all=allow_all,
                k=mutate_k,
            )

        # Generate matches from list of teams
        matches = match_fn(teams)

        print(f"Generation {i + 1}:")

        # Run simulations
        results = await run_battles(
            matches,
            teams,
            player_1,
            player_2,
            battles_per_match=battles_per_match,
            progress_bar=progress_bars,
        )

        # Compute fitness
        fitness = fitness_fn(teams, matches, results, **fitness_kwargs)

    # return all teams and fitness scores
    return teams, fitness
