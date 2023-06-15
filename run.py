from __future__ import annotations

import sys
from subprocess import check_output

import numpy as np
from poke_env.teambuilder import Teambuilder
from tqdm import tqdm

from p2lab.team import Team


class Builder(Teambuilder):
    def yield_team(self):
        pass


def generate_pool(num_pokemon, format="gen7anythinggoes"):
    teams = []
    print("Generating pokemon in batches of 6 to form pool...")
    # teams are produced in batches of 6, so we need to generate
    # a multiple of 6 teams that's greater than the number of pokemon
    N_seed_teams = num_pokemon // 6 + 1
    for _ in tqdm(range(N_seed_teams)):
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
        n_team = Builder().parse_showdown_team(
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
    return pool[:num_pokemon]


def generate_teams(pool, num_teams, team_size=6):
    return [
        Team(np.random.choice(pool, size=team_size, replace=False))
        for _ in range(num_teams)
    ]


# test the pool generation
if __name__ == "__main__":
    pool = generate_pool(100)
    print(pool)
    print(len(pool))
