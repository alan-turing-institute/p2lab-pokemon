from __future__ import annotations

import pytest
from poke_env import PlayerConfiguration
from poke_env.player import SimpleHeuristicsPlayer

from p2lab.battling.battles import run_battles
from p2lab.pokemon import pokefactory
from p2lab.pokemon.teams import Team

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio()
async def test_battle_eevee_pikachu_pokes():
    p = pokefactory.PokeFactory()
    eevee = p.make_pokemon(133, moves=["tackle", "growl"], level=5)
    pikachu = p.make_pokemon(25, moves=["thundershock", "growl"], level=5)
    team1 = Team([eevee])
    team2 = Team([pikachu])
    teams = [team1, team2]
    matches = [[0, 1]]

    player_1 = SimpleHeuristicsPlayer(
        PlayerConfiguration("Player 1", None), battle_format="gen7anythinggoes"
    )
    player_2 = SimpleHeuristicsPlayer(
        PlayerConfiguration("Player 2", None), battle_format="gen7anythinggoes"
    )
    res = await run_battles(matches, teams, player_1, player_2, battles_per_match=1)
    assert res is not None


@pytest.mark.asyncio()
async def test_battle_mewtwo_obliterates_eevee():
    p = pokefactory.PokeFactory()
    eevee = p.make_pokemon(133, moves=["tackle", "growl"], level=5)
    mewtwo = p.make_pokemon(150, moves=["psychic"], level=100)
    team1 = Team([eevee])
    team2 = Team([mewtwo])
    teams = [team1, team2]
    matches = [[0, 1]]
    player_1 = SimpleHeuristicsPlayer(
        PlayerConfiguration("Player 3", None), battle_format="gen7anythinggoes"
    )
    player_2 = SimpleHeuristicsPlayer(
        PlayerConfiguration("Player 4", None), battle_format="gen7anythinggoes"
    )
    res = await run_battles(matches, teams, player_1, player_2, battles_per_match=10)
    mewtwo_wins = res[0][1]
    eevee_wins = res[0][0]
    assert mewtwo_wins > eevee_wins


@pytest.mark.asyncio()
async def test_battle_eevee_pikachu_formats():
    p = pokefactory.PokeFactory()
    eevee = p.make_pokemon(133, moves=["tackle", "growl"], level=5)
    pikachu = p.make_pokemon(25, moves=["thundershock", "growl"], level=5)
    team1 = Team([eevee])
    team2 = Team([pikachu])
    teams = [team1, team2]
    matches = [[0, 1]]
    counter = iter(range(10, 20))
    battle_formats = [
        "gen4anythinggoes",
        "gen6anythinggoes",
        "gen7anythinggoes",
        "gen8anythinggoes",
    ]
    for battle_format in battle_formats:
        player_1 = SimpleHeuristicsPlayer(
            PlayerConfiguration(f"Player {next(counter)}", None),
            battle_format=battle_format,
        )
        player_2 = SimpleHeuristicsPlayer(
            PlayerConfiguration(f"Player {next(counter)}", None),
            battle_format=battle_format,
        )
        res = await run_battles(matches, teams, player_1, player_2, battles_per_match=1)
        assert res is not None
