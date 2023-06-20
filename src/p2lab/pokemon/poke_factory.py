"""
This class is used to generate Pokemon teams using the pokedex provided from
Pokemon Showdown (via poke-env)

This is directly inspired by poke-env's diagostic_tools folder
"""
from __future__ import annotations

from poke_env.data import GenData as POKEDEX


class PokeFactory:
    def __init__(self, gen=1):
        self.dex = POKEDEX(gen)
        self.dex2mon = {int(self.dex.pokedex[m]["num"]): m for m in self.dex.pokedex}

    def get_pokemon_by_dexnum(self, dexnum):
        return self.dex.pokedex[self.dex2mon[dexnum]]
