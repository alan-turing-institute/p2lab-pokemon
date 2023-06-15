"""
The team builder
"""
from __future__ import annotations

import copy
import sys
from subprocess import check_output
import multiprocessing

import numpy as np
from poke_env.teambuilder import Teambuilder
from tqdm import tqdm

from .team import Team
from . import gen_filter

class Builder(Teambuilder):
    """
    The team builder
    """

    def __init__(self, N_seed_teams=2, teams=None, play_format="gen7anythinggoes", team_selection_format=None, team_size=3, filter=True):
        self.play_format = play_format
        self.team_selection_format = team_selection_format
        self.team_size = team_size
        if team_selection_format is None:
            team_selection_format = format
        if teams:
            self.teams = [
                self.join_team(self.parse_showdown_team(team)) for team in teams
            ]
        else:
            self.teams = []
            print("Generating seed teams")
            with multiprocessing.Pool(processes=8) as pool:
                teams = list(tqdm(pool.imap(self.generate_teams_via_showdown, [self.team_size for _ in range(N_seed_teams)]), total=N_seed_teams))
            self.teams = [t for t in teams if t is not None]
        self.poke_pool = np.array(self.teams).flatten()
        if filter:
            self.poke_pool = [p for p in self.poke_pool if gen_filter.is_in(p, gen_filter.pokemon_gen1)]

    def build_N_teams_from_poke_pool(self, N_teams):
        self.teams = [
            Team(np.random.choice(self.poke_pool, size=self.team_size, replace=False))
            for _ in range(N_teams)
        ]


    def generate_teams_via_showdown(self, _):

        try:
            poss_team = check_output(
                f"pokemon-showdown generate-team {self.team_selection_format}", shell=True
            )
            check_output(
                f"pokemon-showdown validate-team {self.play_format} ",
                shell=True,
                input=poss_team,
            )

            n_team = self.parse_showdown_team(
                check_output(
                    "pokemon-showdown export-team ", input=poss_team, shell=True
                ).decode(sys.stdout.encoding)
            )
            if len(n_team) != 6:
                msg = "Team not of length 6"
                raise Exception(msg)
        except Exception as e:
            print("Error validating team... skipping to next")
            return None
        return n_team

    def get_teams(self):
        return self.teams

    def yield_team(self):
        return self.teams[np.random.choice(len(self.teams))]

    def generate_new_teams(self):
        self.last_generation = copy.deepcopy(self.teams)
        self.breed_teams()
        # TODO: Make this fancier
        # self.mutate_teams()

    def breed_teams(self):
        teams = []
        for _ in range(len(self.teams)):
            probs = np.array([t.get_fitness() for t in self.teams])
            probs = probs / np.sum(probs)
            t1, t2 = np.random.choice(self.teams, 2, p=probs, replace=False)
            t1 = t1.get_teamlist()
            t2 = t2.get_teamlist()
            teams.append(self.breed_team(t1, t2))
        self.teams = teams


    def breed_team(self, t1, t2):
        # REALLY BAD DUPLICATION PREVENTION
        # TODO: FIX ASAP
        poss_pokes = np.concatenate((t1, t2))
        names = [str(p).split("|")[0] for p in poss_pokes]
        new_team_names = np.random.choice(list(set(names)), size=self.team_size, replace=False)
        n2p = dict(zip(names, poss_pokes))
        new_team = [n2p[n] for n in new_team_names]
        return Team(new_team)

    def mutate_team(self, team, mutation_rate=0.1):
        # Each pokemon in a team has a given probability of being replaced by a random pokemon from the pool
        for pokemon in team:
            if np.random.random() < mutation_rate:
                new_pokemon = np.random.choice(self.poke_pool)
                # If the pokemon is already in the team, replace it with a random pokemon from the pool
                while new_pokemon in team:
                    new_pokemon = np.random.choice(self.poke_pool)
                # Replace the pokemon
                team[np.where(team == pokemon)[0][0]] = new_pokemon
