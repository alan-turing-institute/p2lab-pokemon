from __future__ import annotations

from p2lab.pokemon import poke_factory


def test_pokedex():
    p = poke_factory.PokeFactory()
    assert p is not None


def test_eevee_fetch():
    p = poke_factory.PokeFactory()
    eevee = p.get_pokemon_by_dexnum(133)
    assert eevee["baseSpecies"].lower() == "eevee"


def test_bulbasaur_fetch():
    p = poke_factory.PokeFactory()
    eevee = p.get_pokemon_by_dexnum(1)
    assert eevee["baseSpecies"].lower() == "bulbasaur"


def test_eevee_moves():
    p = poke_factory.PokeFactory()
    eevee_moves = p.get_allowed_moves(133)
    assert len(eevee_moves) > 0


def test_bulbasaur_moves():
    p = poke_factory.PokeFactory()
    bulb_moves = p.get_allowed_moves(1)
    assert len(bulb_moves) > 0


def test_eevee_stats():
    assert 1 == 0
