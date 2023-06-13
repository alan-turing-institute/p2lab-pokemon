from __future__ import annotations


class Team:
    def __init__(self, pokemon) -> None:
        self.pokemon = pokemon

    def random_mutate(self, p: float, pokemon_population: list[str]):
        print(p)
        print(pokemon_population)
        # randomly replace one team member with probability p
        self.pokemon = self.pokemon
