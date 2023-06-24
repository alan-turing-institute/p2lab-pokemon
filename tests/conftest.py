from __future__ import annotations

import pytest

from p2lab.pokemon import pokefactory


@pytest.fixture()
def default_factory():
    return pokefactory.PokeFactory()
