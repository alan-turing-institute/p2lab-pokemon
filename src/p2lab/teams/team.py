from __future__ import annotations

import re

import pandas as pd


class Team:
    def __init__(self, pokemon) -> None:
        self.pokemon = pokemon
        self.fitness = 0

    def get_teamlist(self):
        return self.pokemon

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, x):
        self.fitness = x

    def to_packed_str(self):
        return "]".join([mon.formatted for mon in self.pokemon])

    def to_df(self):
        # TODO Put in the columns or something
        df = pd.DataFrame(
            [re.split("\\||,", s) for s in re.split("\\]", self.to_packed_str())]
        )
        return df
