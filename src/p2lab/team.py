from __future__ import annotations

import numpy as np


class Team:
    def __init__(self, pokemon) -> None:
        self.pokemon = np.array(pokemon)

    def to_packed_str(self):
        return "]".join([mon.formatted for mon in self.pokemon])
