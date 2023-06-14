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

    # # Check for convergence
    # if np.sum(np.abs(old_abilities - abilities)) < tol:
    #     break

    return abilities


def BT_iter_func(
    id: int,
    team_ids: np.ndarray,
    win_matrix: np.ndarray,
    abilities: np.ndarray,
):
    """
    Function to compute this part of the BT iterative estimation:
    sum_(j!=1) {(w_ij + w_ji)/(p_i + p_j)}

    Args:
        id: Team to compute the relevant sum for
        team_ids: Array of all team ids
        win_matrix: Matrix of wins
        abilities: Array of abilities
    """
    other_ids = team_ids[team_ids != id]
    return np.sum(
        (win_matrix[id, other_ids] + win_matrix[other_ids, id])
        / (abilities[0] + abilities[other_ids])
    )


def win_percentages(
    teams: list[Team],
    matches: np.ndarray,
    results: np.ndarray,
) -> np.ndarray:
    """
    This function calculates the ratio of games won to games played for each
    team. This serves as a candidate measure for fitness in the genetic algo

    Args:
        teams: A list of teams. Used mainly for generating team IDs
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
        results: An array of 1s and 0s, where each entry corresponds to a row
                 in matches denoting whether or not team 1 won the match
    """
    team_ids = np.array(range(len(teams)))
    total_wins = count_team_wins(
        team_ids=team_ids,
        matches=matches,
        results=results,
    )
    total_matches = count_team_matches(
        team_ids=team_ids,
        matches=matches,
    )
    win_percentages = total_wins / total_matches
    return win_percentages / np.sum(win_percentages)  # standardise to sum to 1


# Some helper functions for use across different candidate fitness functions:
def count_team_wins(
    team_ids: np.ndarray,
    matches: np.ndarray,
    results: np.ndarray,
) -> np.ndarray:
    """
    Given some matches and results, computes total wins for each team

    Args:
        team_ids:
        matches (_type_): _description_
        results:
    """
    total_wins = np.array([], dtype=np.int32)
    for id in team_ids:
        total_wins = np.append(
            total_wins,
            np.sum(results[matches[:, 0] == id])
            + np.sum(1 - results[matches[:, 1] == id]),
        )
    return total_wins


def count_team_matches(
    team_ids: np.ndarray,
    matches: np.ndarray,
) -> np.ndarray:
    """
    Count the number of matches each team has played

    Args:
        team_ids:
        matches (_type_): _description_
    """
    return np.array([np.sum(matches == x) for x in team_ids])


def make_win_matrix(
    N_team: int,
    matches: np.ndarray,
    results: np.ndarray,
) -> np.ndarray:
    """
    Produces an N_team x N_team matrix, where row (i,j) counts
    the number of times team i has beaten team j.

    Args:
        matches (_type_): _description_
        results (_type_): _description_
    """

    win_matrix = np.zeros(shape=(N_team, N_team), dtype=np.int32)
    for index, match in enumerate(matches):
        if results[index] == 0:
            win_matrix[match[1], match[0]] += 1
        else:
            win_matrix[match[0], match[1]] += 1
    return win_matrix
