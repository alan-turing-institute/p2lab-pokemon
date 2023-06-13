from __future__ import annotations

import pytest

from p2lab.genetic.matching import dense, mst


@pytest.fixture()
def data():
    return [0] * 5


def test_dense(data):
    print(dense(data))


def test_mst(data):
    print(mst(data))
