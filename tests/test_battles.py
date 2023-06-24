from __future__ import annotations

import inspect

import pytest
from poke_env import PlayerConfiguration
from poke_env.player import SimpleHeuristicsPlayer

from p2lab.pokemon.battles import run_battles
from p2lab.pokemon.teams import Team

pytest_plugins = ("pytest_asyncio",)


def test_battle_eevee_pikachu_pokes(event_loop, default_factory):
    eevee = default_factory.make_pokemon(133, moves=["tackle", "growl"], level=5)
    pikachu = default_factory.make_pokemon(25, moves=["thundershock", "growl"], level=5)
    team1 = Team([eevee])
    team2 = Team([pikachu])
    teams = [team1, team2]
    matches = [[0, 1]]

    player_1 = SimpleHeuristicsPlayer(
        PlayerConfiguration(inspect.stack()[0][3].split("test_")[1][:15] + " P1", None),
        battle_format="gen7anythinggoes",
    )
    player_2 = SimpleHeuristicsPlayer(
        PlayerConfiguration(inspect.stack()[0][3].split("test_")[1][:15] + " P2", None),
        battle_format="gen7anythinggoes",
    )
    res = event_loop.run_until_complete(
        run_battles(matches, teams, player_1, player_2, battles_per_match=1)
    )

    assert res is not None


def test_battle_mewtwo_obliterates_eevee(event_loop, default_factory):
    eevee = default_factory.make_pokemon(133, moves=["tackle", "growl"], level=5)
    mewtwo = default_factory.make_pokemon(150, moves=["psychic"], level=100)
    team1 = Team([eevee])
    team2 = Team([mewtwo])
    teams = [team1, team2]
    matches = [[0, 1]]
    player_1 = SimpleHeuristicsPlayer(
        PlayerConfiguration(inspect.stack()[0][3].split("test_")[1][:15] + " P1", None),
        battle_format="gen7anythinggoes",
    )
    player_2 = SimpleHeuristicsPlayer(
        PlayerConfiguration(inspect.stack()[0][3].split("test_")[1][:15] + " P2", None),
        battle_format="gen7anythinggoes",
    )
    res = event_loop.run_until_complete(
        run_battles(matches, teams, player_1, player_2, battles_per_match=1)
    )
    mewtwo_wins = res[0][1]
    eevee_wins = res[0][0]
    assert mewtwo_wins > eevee_wins


@pytest.mark.parametrize(
    "battle_format",
    [
        ("gen4anythinggoes"),
        ("gen6anythinggoes"),
        ("gen7anythinggoes"),
        ("gen8anythinggoes"),
    ],
)
def test_battle_eevee_pikachu_formats(event_loop, battle_format, default_factory):
    eevee = default_factory.make_pokemon(133, moves=["tackle", "growl"], level=5)
    pikachu = default_factory.make_pokemon(25, moves=["thundershock", "growl"], level=5)
    team1 = Team([eevee])
    team2 = Team([pikachu])
    teams = [team1, team2]
    matches = [[0, 1]]

    player_1 = SimpleHeuristicsPlayer(
        PlayerConfiguration(
            inspect.stack()[0][3].split("test_")[1][:10]
            + "-"
            + battle_format[:4]
            + " P1",
            None,
        ),
        battle_format=battle_format,
    )
    player_2 = SimpleHeuristicsPlayer(
        PlayerConfiguration(
            inspect.stack()[0][3].split("test_")[1][:10]
            + "-"
            + battle_format[:4]
            + " P2",
            None,
        ),
        battle_format=battle_format,
    )
    res = event_loop.run_until_complete(
        run_battles(matches, teams, player_1, player_2, battles_per_match=1)
    )
    assert res is not None
