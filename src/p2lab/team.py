from __future__ import annotations


class Team:
    def __init__(self, pokemon) -> None:
        self.pokemon = pokemon

    def to_packed_str(self):
        return "]".join([mon.formatted for mon in self.pokemon])
