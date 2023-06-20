"""
This class is used to generate Pokemon teams using the pokedex provided from
Pokemon Showdown (via poke-env)

This is directly inspired by poke-env's diagostic_tools folder
"""
from __future__ import annotations

from poke_env.data import GenData as POKEDEX
from poke_env.teambuilder import TeambuilderPokemon


class PokeFactory:
    def __init__(self, gen=1, drop_forms=True):
        self.gen = (
            gen if gen > 4 else 3
        )  # because this seems to be the minimum gen for the pokedex
        self.dex = POKEDEX(self.gen)
        if drop_forms:
            self.dex2mon = {
                int(self.dex.pokedex[m]["num"]): m
                for m in self.dex.pokedex
                if "forme" not in self.dex.pokedex[m].keys()
            }
        else:
            self.dex2mon = {
                int(self.dex.pokedex[m]["num"]): m for m in self.dex.pokedex
            }

    def get_pokemon_by_dexnum(self, dexnum):
        return self.dex.pokedex[self.dex2mon[dexnum]]

    def get_allowed_moves(self, dexnum, level=100):
        pot_moves = self.dex.learnset[self.dex2mon[dexnum]]["learnset"]
        allowed_moves = []
        for move, lims in pot_moves.items():
            gens = [int(lim[0]) for lim in lims]
            # TODO: write logic here to check if level is allowed
            if level != 100:
                msg = "Level checking not implemented yet"
                raise NotImplementedError(msg)
            # lvls = [int(l[1:]) for l in lims if l[1:].isdigit()]
            if self.gen in gens:
                allowed_moves.append(move)
        return allowed_moves

    def make_pokemon(self, dexnum, **kwargs):
        return TeambuilderPokemon(species=self.dex2mon[dexnum], **kwargs)
