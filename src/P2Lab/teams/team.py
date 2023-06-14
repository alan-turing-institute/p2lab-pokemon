from __future__ import annotations


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
