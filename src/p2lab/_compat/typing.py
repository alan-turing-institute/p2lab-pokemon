"""
Copyright (c) 2023 Scientists of the P2 Laboratory. All rights reserved.

P2-Lab: a secret package for genetic optimisation of pokemon teams
"""


from __future__ import annotations

import sys

if sys.version_info < (3, 8):
    from typing_extensions import Literal, Protocol, runtime_checkable
else:
    from typing import Literal, Protocol, runtime_checkable

__all__ = ["Protocol", "runtime_checkable", "Literal"]


def __dir__() -> list[str]:
    return __all__
