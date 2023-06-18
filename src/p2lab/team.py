from __future__ import annotations

import numpy as np


class Team:
    def __init__(self, pokemon) -> None:
        self.pokemon = np.array(pokemon)
        self.first_name = self.pokemon[0].formatted.split("|")[0]

    def to_packed_str(self):
        return "]".join([mon.formatted for mon in self.pokemon])
