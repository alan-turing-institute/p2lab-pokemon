from __future__ import annotations


class Team:
    def __init__(self, pokemon) -> None:
        self.pokemon = pokemon
        self.fitness = 0
    
    def get_teamlist(self):
        return self.pokemon
    def get_fitness(self):
        return self.fitness
    def random_mutate(self, p: float, pokemon_population: list[str]):
        print(p)
        print(pokemon_population)
        # randomly replace one team member with probability p
        self.pokemon = self.pokemon

    def set_fitness(self, x):
        self.fitness = x