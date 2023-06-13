from __future__ import annotations


class Team:
    def __init__(self, pokemon) -> None:
        self.pokemon = pokemon

    def random_mutate(self, p: float):
        print(p)
        # randomly replace one team member with probability p
        self.pokemon = self.pokemon
