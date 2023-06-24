from __future__ import annotations

import pytest

from p2lab.pokemon.teams import Team


def test_basic_team_creation(gen_1_pool):
    team = Team([gen_1_pool[0], gen_1_pool[1], gen_1_pool[2]])
    assert len(team) == 3
    assert team[0] == gen_1_pool[0]
    assert team[1] == gen_1_pool[1]
    assert team[2] == gen_1_pool[2]
    assert list(team.names) == ["Bulbasaur", "Ivysaur", "Venusaur"]


def test_team_creation_with_duplicates(gen_1_pool):
    with pytest.raises(ValueError, match="Team cannot have duplicate pokemon"):
        Team([gen_1_pool[0], gen_1_pool[1], gen_1_pool[2], gen_1_pool[0]])


def test_team_creation_with_too_many_pokemon(gen_1_pool):
    with pytest.raises(ValueError, match="Team cannot have more than 6 pokemon"):
        Team(gen_1_pool)


def test_modifying_pokemon_in_team(gen_1_pool):
    team = Team([gen_1_pool[0], gen_1_pool[1], gen_1_pool[2]])
    with pytest.raises(
        TypeError, match="'Team' object does not support item assignment"
    ):
        team[0] = gen_1_pool[7]
