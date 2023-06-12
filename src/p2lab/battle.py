from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# make the path to the bot submodule (showdown/ in the root of the repo) available
# work it out at runtime so we don't have to hardcode it
sys.path.append(str(Path(__file__).parent.parent))
# this line is equivalent to:
# sys.path.append(str(Path(__file__).parent.parent / "showdown"))
# since __file__ is the path to this file, and Path.parent is the parent directory

from showdown.run import showdown


def run_battle(bot_1, bot_2):
    """
    Run a battle between two bots.
    """

    # make bots aware they are in a battle

    results = asyncio.gather(
        showdown(env=False, **bot_1.config), showdown(env=False, **bot_2.config)
    )

    # make bots aware they are no longer in a battle

    # make new bot objects with updated win counts for their teams

    return results  # probably return the new bot objects or teams instead of this
