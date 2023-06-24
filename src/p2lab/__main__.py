from __future__ import annotations

import argparse
import asyncio

import numpy as np

from p2lab.genetic.genetic import genetic_algorithm
from p2lab.genetic.operations import (
    build_crossover_fn,
    locus_swap,
    sample_swap,
    slot_swap,
)
from p2lab.pokemon.premade import gen_1_pokemon
from p2lab.pokemon.teams import generate_teams, import_pool


async def main_loop(
    num_teams,
    team_size,
    num_generations,
    battles_per_match,
    unique,
    crossover,
    p1,
    p2,
    write_every,
    write_path,
):
    # generate the pool
    pool = import_pool(gen_1_pokemon())
    seed_teams = generate_teams(pool, num_teams, team_size, unique=unique)
    function_map = {
        "sample": sample_swap,
        "slot": slot_swap,
        "locus": locus_swap,
    }
    crossover_fn = (
        build_crossover_fn(function_map[crossover]) if crossover is not None else None
    )

    # log the parameters
    print("Running genetic algorithm with the following parameters:")
    print(f"Number of teams: {num_teams}")
    print(f"Team size: {team_size}")
    print(f"Number of generations: {num_generations}")
    print(f"Unique teams: {unique}")
    print(f"Crossover: {crossover if crossover is not None else 'none'}")
    print(f"Player 1: {p1}")
    print(f"Player 2: {p2}")
    # run the genetic algorithm
    teams, fitnesses = await genetic_algorithm(
        pokemon_pool=pool,
        seed_teams=seed_teams,
        num_teams=num_teams,
        team_size=team_size,
        num_generations=num_generations,
        progress_bars=True,
        mutate_with_fitness=crossover_fn is None,
        crossover_fn=crossover_fn,
        mutate_k=team_size - 1,
        player_1_name=p1,
        player_2_name=p2,
        battles_per_match=battles_per_match,
        write_every=write_every,
        write_path=write_path,
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generations",
        help="Number of generations to iterate over",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--team-size", help="Number of pokemon per team (max 6)", type=int, default=3
    )
    parser.add_argument(
        "--teams",
        help="Number of teams i.e., individuals per generation",
        type=int,
        default=30,
    )
    parser.add_argument("--seed", help="Random seed to use ", type=int, default=None)
    parser.add_argument(
        "--unique",
        help="Determines if a team can have duplicate pokemon species",
        default=True,
    )
    parser.add_argument(
        "--crossover",
        help="Determines which crossover function to use",
        choices=["locus", "slot", "sample"],
        default=None,
    )
    parser.add_argument(
        "--p1",
        help="Name of the first player",
        type=str,
        default="Player 1",
    )
    parser.add_argument(
        "--p2",
        help="Name of the second player",
        type=str,
        default="Player 2",
    )
    parser.add_argument(
        "--battles-per-match",
        help="Number of battles per match",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--write-every",
        help="Write every N generations",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--write-path",
        help="Path to write to",
        type=str,
        default=".",
    )
    return vars(parser.parse_args())


def main():
    args = parse_args()
    if args["seed"] is not None:
        np.random.seed(args["seed"])

    asyncio.get_event_loop().run_until_complete(
        main_loop(
            num_teams=args["teams"],
            team_size=args["team_size"],
            num_generations=args["generations"],
            unique=args["unique"],
            crossover=args["crossover"],
            p1=args["p1"],
            p2=args["p2"],
            battles_per_match=args["battles_per_match"],
            write_every=args["write_every"],
            write_path=args["write_path"],
        )
    )


if __name__ == "__main__":
    main()
