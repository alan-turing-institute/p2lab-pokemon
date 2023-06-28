from __future__ import annotations

import pytest

from p2lab.__main__ import main_loop


@pytest.mark.parametrize(
    ("team_size", "crossover_string"),
    [
        (1, None),
        (2, None),
        (6, "locus"),
        (6, "slot"),
        (6, "sample"),
    ],
)
def test_main_loop(event_loop, team_size, crossover_string):
    num_teams = 10
    num_generations = 3
    crossover_name = crossover_string if crossover_string is not None else "none"
    player_name = "main-" + str(team_size) + "-" + crossover_name
    event_loop.run_until_complete(
        main_loop(
            num_teams=num_teams,
            team_size=team_size,
            num_generations=num_generations,
            unique=True,
            crossover=crossover_string,
            p1=player_name[:15] + " P1",
            p2=player_name[:15] + " P2",
            battles_per_match=3,
            write_every=None,
            write_path=None,
        )
    )
