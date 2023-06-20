from __future__ import annotations

from p2lab.pokemon import poke_factory


def test_pokedex():
    p = poke_factory.PokeFactory()
    assert p is not None


def test_eevee_fetch():
    p = poke_factory.PokeFactory()
    eevee = p.get_pokemon_by_dexnum(133)
    assert eevee["species"].lower() == "eevee"


def test_eevee_moves():
    assert 1 == 0


def test_eevee_stats():
    assert 1 == 0


def test_impossible_pokemon():
    assert 1 == 0
