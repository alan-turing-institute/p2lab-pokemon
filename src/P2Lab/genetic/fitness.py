from __future__ import annotations

import numpy as np

from p2lab.pokemon.team import Team


def BTmodel(
    teams: list[Team],
    matches: np.ndarray,
    results: list[int],
) -> list[float]:
    """
    Bradley-Terry Models

    Args:
        teams: A list of unique team names
        matches: A numpy.ndarray with the following format:

        team 1 | team 2
        -------+-------
          A    |   B
          B    |   C
          B    |   D
          A    |   D
          B    |   A

        'team 1' and 'team 2' are columns containing the IDs of the teams
        that played in the role of team 1 and team 2 respectively

        results: A list of 1s and 0s, where each entry corresponds to a row
        in matches denoting whether or not team 1 won the match
    """

    # Organise teams into X1 and X2 matrices
    print(teams)

    # Generate vector of team abilities
    print(matches)

    # Estimate logit model
    print(results)

    # Return parameters as a measure of fitness
    return [0.1, 0.2, 0.3]
