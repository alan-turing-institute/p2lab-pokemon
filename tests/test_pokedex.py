from __future__ import annotations

import numpy as np
import pytest


def test_eevee_fetch(default_factory):
    eevee = default_factory.get_pokemon_by_dexnum(133)
    assert eevee["baseSpecies"].lower() == "eevee"


def test_bulbasaur_fetch(default_factory):
    bulb = default_factory.get_pokemon_by_dexnum(1)
    assert bulb["baseSpecies"].lower() == "bulbasaur"


def test_eevee_moves(default_factory):
    eevee_moves = default_factory.get_allowed_moves(133)
    assert len(eevee_moves) > 0


def test_bulbasaur_moves(default_factory):
    bulb_moves = default_factory.get_allowed_moves(1)
    assert len(bulb_moves) > 0


def test_eevee_is_created(default_factory):
    eevee = default_factory.make_pokemon(133)
    assert eevee is not None


def test_eevee_is_created_with_moves(default_factory):
    eevee = default_factory.make_pokemon(133, moves=["tackle", "growl"])
    assert eevee is not None


def test_random_pokemon_is_created_with_moves(default_factory):
    dexnum = np.random.randint(1, 151)
    while dexnum == 132:
        dexnum = np.random.randint(1, 151)
    poke = default_factory.make_pokemon(dexnum=dexnum, generate_moveset=True)
    assert 1 < len(poke.moves) <= 4


def test_ditto_is_created_with_moves(default_factory):
    ditto = default_factory.make_pokemon(132)
    assert len(ditto.moves) == 1


def test_all_gen1_pokemon_can_be_created(default_factory):
    for dexnum in range(1, 152):
        poke = default_factory.make_pokemon(dexnum=dexnum, generate_moveset=True)
        assert 1 < len(poke.moves) <= 4


def test_invalid_dex_raised(default_factory):
    with pytest.raises(ValueError, match="dexnum must be between 1 and 151"):
        default_factory.make_pokemon(dexnum=0)


def test_adding_item_to_pokemon(default_factory):
    ditto = default_factory.make_pokemon(132, item="choice scarf")
    assert ditto.item == "choice scarf"
