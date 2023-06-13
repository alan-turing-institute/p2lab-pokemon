"""
TODO: Write some docs here.
"""

import asyncio
from .teams.builder import Builder
from .evaluator.poke_env import PokeEnv
from .teams.team import Team 
from tqdm import tqdm

N_generations = 10 # Number of generations to run
N_teams = 3 # Number of teams to generate per generation
N_battles = 3 # Number of battles to run per team

async def main_loop():
    builder = Builder(N_seed_teams=N_teams)
    builder.build_N_teams_from_poke_pool(N_teams)
    curr_gen = 0 # Current generation
    teams = [Team(builder.yield_team()) for n in range(N_teams)]
    evaluator = PokeEnv()

    # Main expected loop
    while curr_gen < N_generations:
        await evaluator.evaluate_teams(teams)
        #poke_pool = [] # List of Pokemon 
        #teams = [] # list of teams (of Pokemon)
        #curr_gen += 1

def main():
    asyncio.get_event_loop().run_until_complete(main_loop())

if __name__ == "__main__":
    main()
