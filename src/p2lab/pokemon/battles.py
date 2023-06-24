from __future__ import annotations

__all__ = ("run_battles",)

import numpy as np
from tqdm import tqdm


async def run_battles(
    matches,
    teams,
    player_1,
    player_2,
    battles_per_match=10,
    progress_bar=True,
):
    results = []
    for t1, t2 in tqdm(matches, desc="Battling!") if progress_bar else matches:
        player_1.update_team(teams[t1].to_packed_str())
        player_2.update_team(teams[t2].to_packed_str())
        await player_1.battle_against(player_2, n_battles=battles_per_match)
        results.append((player_1.n_won_battles, player_2.n_won_battles))
        player_1.reset_battles()
        player_2.reset_battles()
    return np.array(results)
