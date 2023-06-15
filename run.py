from __future__ import annotations

import asyncio
import sys
from subprocess import check_output

import numpy as np
from poke_env import PlayerConfiguration
from poke_env.player import RandomPlayer
from poke_env.teambuilder import Teambuilder
from tqdm import tqdm

from p2lab.genetic.matching import dense
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


async def run_battles(
    matches,
    teams,
    battles_per_match=1,
    bot_strategy="random",
    battle_format="gen7anythinggoes",
    progress_bar=True,
):
    if bot_strategy == "random":
        p1 = RandomPlayer(
            PlayerConfiguration("Player 1", None), battle_format=battle_format
        )
        p2 = RandomPlayer(
            PlayerConfiguration("Player 2", None), battle_format=battle_format
        )
    else:
        msg = f"bot strategy not implemented: should be one of ['random'] but got {bot_strategy}"
        raise Exception(msg)

    results = []
    for t1, t2 in tqdm(matches) if progress_bar else matches:
        p1.update_team(teams[t1].to_packed_str())
        p2.update_team(teams[t2].to_packed_str())
        await p1.battle_against(p2, n_battles=battles_per_match)
        results.append((p1.n_won_battles, p2.n_won_battles))
        p1.reset_battles()
        p2.reset_battles()

    return results


async def main():
    pool = generate_pool(10)
    print(len(pool))
    teams = generate_teams(pool, 3)
    matches = dense(teams)
    print(f"matches: {matches}")
    print(f"matches shape: {matches.shape}")
    results = await run_battles(matches, teams)
    print(f"results: {results}")


# test the pool generation
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
