from __future__ import annotations

import numpy as np

from p2lab.pokemon import pokefactory


def test_pokedex():
    p = pokefactory.PokeFactory()
    assert p is not None


def test_eevee_fetch():
    p = pokefactory.PokeFactory()
    eevee = p.get_pokemon_by_dexnum(133)
    assert eevee["baseSpecies"].lower() == "eevee"


def test_bulbasaur_fetch():
    p = pokefactory.PokeFactory()
    bulb = p.get_pokemon_by_dexnum(1)
    assert bulb["baseSpecies"].lower() == "bulbasaur"


def test_eevee_moves():
    p = pokefactory.PokeFactory()
    eevee_moves = p.get_allowed_moves(133)
    assert len(eevee_moves) > 0


def test_bulbasaur_moves():
    p = pokefactory.PokeFactory()
    bulb_moves = p.get_allowed_moves(1)
    assert len(bulb_moves) > 0


def test_eevee_is_created():
    p = pokefactory.PokeFactory()
    eevee = p.make_pokemon(133)
    assert eevee is not None


def test_eevee_is_created_with_moves():
    p = pokefactory.PokeFactory()
    eevee = p.make_pokemon(133, moves=["tackle", "growl"])
    assert eevee is not None


def test_random_pokemon_is_created_with_moves():
    p = pokefactory.PokeFactory()
    dexnum = np.random.randint(1, 151)
    while dexnum == 132:
        dexnum = np.random.randint(1, 151)
    poke = p.make_pokemon(dexnum=dexnum, generate_moveset=True)
    assert len(poke.moves) == 4


def test_ditto_is_created_with_moves():
    p = pokefactory.PokeFactory()
    ditto = p.make_pokemon(132)
    assert len(ditto.moves) == 1


def test_all_gen1_pokemon_can_be_created():
    p = pokefactory.PokeFactory()
    for dexnum in range(1, 152):
        poke = p.make_pokemon(dexnum=dexnum, generate_moveset=True)
        assert len(poke.moves) > 0


def test_invalid_dex_raised():
    p = pokefactory.PokeFactory()
    try:
        p.make_pokemon(dexnum=0)
    except ValueError:
        assert True
    else:
        raise AssertionError()


def test_adding_item_to_pokemon():
    p = pokefactory.PokeFactory()
    ditto = p.make_pokemon(132, item="choice scarf")
    assert ditto.item == "choice scarf"