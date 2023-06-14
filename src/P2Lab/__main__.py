"""
TODO: Write some docs here.
"""

import asyncio
from .teams.builder import Builder
from .evaluator.poke_env import PokeEnv
from .teams.team import Team 
from .stats.team_recorder import TeamRecorder
from tqdm import tqdm

N_generations = 10 # Number of generations to run
N_teams = 10 # Number of teams to generate per generation
N_battles = 10 # Number of battles to run per team
RECORD=True

async def main_loop():
    builder = Builder(N_seed_teams=N_teams)
    builder.build_N_teams_from_poke_pool(N_teams)
    teams = builder.get_teams()
    curr_gen = 0 # Current generation
    evaluator = PokeEnv(n_battles=N_battles)
    recorder = TeamRecorder()

    # Main expected loop
    print("Starting main loop and running on Generation: ")
    for _ in tqdm(range(N_generations)):
        if RECORD:
            recorder.record_teams(teams, curr_gen) 
        await evaluator.evaluate_teams(teams)
        builder.generate_new_teams()
        teams = builder.get_teams()
        curr_gen += 1

def main():
    asyncio.get_event_loop().run_until_complete(main_loop())

if __name__ == "__main__":
    main()
