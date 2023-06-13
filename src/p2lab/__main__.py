"""
TODO: Write some docs here.
"""

from .teams.builder import Builder
from .evaluator.poke_env import PokeEnv

def main():

    # Main expected loop
    N_generations = 100 # Number of generations to run
    curr_gen = 0 # Current generation
    poke_pool = [] # List of Pokemon 
    teams = [] # list of teams (of Pokemon)

    while curr_gen < N_generations:
        team_fitness = [] # list of scores (of teams)
        poke_pool = [] # List of Pokemon 
        teams = [] # list of teams (of Pokemon)
        curr_gen += 1

if __name__ == "__main__":
    main()