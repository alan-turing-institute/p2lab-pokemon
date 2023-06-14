from __future__ import annotations
from poke_env.player import Player, RandomPlayer
import numpy as np


def run_battles(matches: np.ndarray) -> list[int]:
    """
    Runs several matches.

    We may want to change code so that we recording wins/losses as a side effect
    of run_battle

    Probably want to parallelise here?

    Args:
        matches (_type_): _description_

    Returns:
        _type_: _description_
    """
    results = []
    for match in matches:
        results.append(run_battle(match))
    return results


def run_battle(match: np.ndarray) -> int:
    print(match)  # delete this line, it's here to pass pre-commit
    return 0  # this function should always run 0 or 1
