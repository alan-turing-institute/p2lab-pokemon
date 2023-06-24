from __future__ import annotations

import pytest

from p2lab.__main__ import main_loop
from p2lab.genetic.operations import (
    locus_swap,
    sample_swap,
    slot_swap,
)


@pytest.mark.parametrize(
    ("team_size", "crossover_fn"),
    [
        (1, None),
        (2, None),
        (6, locus_swap),
        (6, slot_swap),
        (6, sample_swap),
    ],
)
def test_main_loop(event_loop, team_size, crossover_fn):
    num_teams = 10
    num_generations = 3
    crossover_name = crossover_fn.__name__ if crossover_fn is not None else "none"
    player_name = "main-" + str(team_size) + "-" + crossover_name
    event_loop.run_until_complete(
        main_loop(
            num_teams=num_teams,
            team_size=team_size,
            num_generations=num_generations,
            unique=True,
            crossover=crossover_fn,
            p1=player_name[:15] + " P1",
            p2=player_name[:15] + " P2",
            battles_per_match=3,
        )
    )
