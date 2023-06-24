from __future__ import annotations

from copy import deepcopy

__all__ = (
    "Team",
    "generate_pool",
    "generate_teams",
    "import_pool",
)

import sys
from dataclasses import dataclass
from pathlib import Path
from subprocess import check_output
from typing import Any

import numpy as np
from poke_env.teambuilder import Teambuilder
from tqdm import tqdm

Pokemon = Any


@dataclass(frozen=True)
class Team:
    pokemon: tuple[Pokemon]
    names: tuple[str]

    def __init__(self, pokemon) -> None:
        if len(pokemon) > 6:
            msg = f"Team cannot have more than 6 pokemon: tried to create team of {pokemon}"
            raise ValueError(msg)
        names = [p.formatted.split("|")[0] for p in pokemon]
        if len(names) != len(set(names)):
            msg = f"Team cannot have duplicate pokemon names: tried to create team of {names}"
            raise ValueError(msg)
        object.__setattr__(self, "pokemon", tuple(deepcopy(pokemon)))
        object.__setattr__(self, "names", tuple(names))

    def to_packed_str(self) -> str:
        return "]".join([mon.formatted for mon in self.pokemon])

    def __len__(self) -> int:
        return len(self.pokemon)

    def __getitem__(self, index: int) -> Pokemon:
        return self.pokemon[index]


class _Builder(Teambuilder):
    def yield_team(self):
        pass


def generate_pool(
    num_pokemon, format="gen7anythinggoes", export=False, filename="pool.txt"
):
    teams = []
    print("Generating pokemon in batches of 6 to form pool...")
    # teams are produced in batches of 6, so we need to generate
    # a multiple of 6 teams that's greater than the number of pokemon
    N_seed_teams = num_pokemon // 6 + 1
    for _ in tqdm(range(N_seed_teams), desc="Generating teams!"):
        poss_team = check_output(f"pokemon-showdown generate-team {format}", shell=True)
        try:
            check_output(
                f"pokemon-showdown validate-team {format} ",
                shell=True,
                input=poss_team,
            )
        except Exception as e:
            print("Error validating team... skipping to next")
            print(f"Error: {e}")
            continue
        n_team = _Builder().parse_showdown_team(
            check_output(
                "pokemon-showdown export-team ", input=poss_team, shell=True
            ).decode(sys.stdout.encoding)
        )
        if len(n_team) != 6:
            msg = "pokemon showdown generated a team not of length 6"
            raise Exception(msg)
        teams.append(n_team)

    pool = np.array(teams).flatten()

    # trim the pool to the desired number of pokemon
    pool = pool[:num_pokemon]

    if export:
        with Path.open(filename, "w") as f:
            packed = "\n".join([mon.formatted for mon in pool])
            # convert using pokemon-showdown export-team
            human_readable = check_output(
                "pokemon-showdown export-team ",
                input=packed,
                shell=True,
                universal_newlines=True,
            )
            f.write(human_readable)

    return pool


def import_pool(pool_source):
    # check if pool is a filename or a list of teams by matching the file extension
    if isinstance(pool_source, str):
        if Path(pool_source).suffix == ".txt":
            with Path.open(pool_source, "r") as f:
                human_readable = f.read()
            teams = []
            # loop over every 6 lines and parse the team
            for _i in range(0, len(human_readable.splitlines()), 6):
                team = _Builder().parse_showdown_team(human_readable)
                teams.append(team)
            pool = np.array(teams).flatten()
        else:
            pool = np.array(_Builder().parse_showdown_team(pool_source))
    else:
        msg = "pool_source must be a filename or a list of teams"
        raise Exception(msg)
    return pool


def generate_teams(pool, num_teams, team_size=6, unique=False):
    if unique:
        if num_teams * team_size > len(pool):
            msg = f"Cannot generate {num_teams} teams of size {team_size} from pool of size {len(pool)}"
            raise Exception(msg)
        indicies = np.random.choice(
            len(pool), size=(num_teams, team_size), replace=False
        )
        teams = np.array(pool)[indicies].reshape(num_teams, team_size)
        return [Team(team) for team in teams]
    return [
        Team(np.random.choice(pool, size=team_size, replace=False))
        for _ in range(num_teams)
    ]
