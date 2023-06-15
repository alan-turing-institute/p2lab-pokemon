from __future__ import annotations

import numpy as np

from p2lab.teams.team import Team


def BTmodel(
    teams: list[Team],
    matches: np.ndarray,
    results: np.ndarray,
    max_iter: int,
    tol: float,
) -> list[float]:
    """
    Bradley-Terry Models are used to estimate latent team 'abilities'
    in sports contests.

    They do this by assuming that the probability of team 1 beating team 1
    has the following form:

    Pr(team1>team2) = exp(a_1) / (exp(a_1) + exp(a_2))

    Where a_1 is team 1's latent ability.

    The abilities are estimated via an iterative algorithm.

    Which means we only need access to win/loss data and match data in order
    to produce estimates

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
        results: An array of shape (num_matches, 2), where each row corresponds to
                 an element of matches and each column corresponds to a team. The
                 items in each column counts the number of times that team won that
                 matchup. 
        max_iter: Maximum number of iterations for Bradley-Terry model to run
        tol: Tolerence to check for convergence at the end of each iteration
    """
    
    # Organise teams into X1 and X2 matrices
    N_team = len(teams)
    N_match = matches.shape[0]
    team_ids = np.array(range(N_team))
    X1 = np.zeros(shape=(N_match, N_team), dtype=np.int32)
    X2 = np.zeros(shape=(N_match, N_team), dtype=np.int32)
    for index, pair in enumerate(matches):
        X1[index, pair[0]] = 1
        X2[index, pair[1]] = 1

    # Prepare win data
    total_wins = count_team_wins(
        team_ids=team_ids,
        matches=matches,
        results=results,
    )
    win_matrix = make_win_matrix(
        N_team=N_team,
        matches=matches,
        results=results,
    )

    # Generate vector of team abilities
    abilities = np.ones(shape=(N_team), dtype=np.float64)

    # Iteratively update abilities as: p_i = W_i / sum_(j!=1) {(w_ij + w_ji)/(p_i + p_j)}
    for _iter in range(max_iter):
        old_abilities = abilities
        abilities = total_wins / np.array(
            [BT_iter_func(x, team_ids, win_matrix, abilities) for x in team_ids]
        )
        abilities = abilities / np.sum(abilities)

        # Check for convergence
        if np.sum(np.abs(old_abilities - abilities)) < tol:
            break
    
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
        results: An array of shape (num_matches, 2), where each row corresponds to
                 an element of matches and each column corresponds to a team. The
                 items in each column counts the number of times that team won that
                 matchup. 
    """
    team_ids = np.array(range(len(teams)))
    total_wins = count_team_wins(
        team_ids=team_ids,
        matches=matches,
        results=results,
    )
    matches_per_pairing = np.sum(results[0,])
    total_pairings = count_team_pairings(
        team_ids=team_ids,
        matches=matches,
    )
    total_matches = total_pairings * matches_per_pairing
    win_percentages = total_wins / total_matches
    fitness = win_percentages / np.sum(win_percentages)
    return fitness


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
        results: An array of shape (num_matches, 2), where each row corresponds to
                 an element of matches and each column corresponds to a team. The
                 items in each column counts the number of times that team won that
                 matchup. 
    """
    total_wins = np.array([], dtype=np.int32)
    for id in team_ids:
        total_wins = np.append(
            total_wins,
            np.sum(results[matches == id]),
        )
    return total_wins


def count_team_pairings(
    team_ids: np.ndarray,
    matches: np.ndarray,
) -> np.ndarray:
    """
    Count the number of pairings each team is in within the match
    data (i.e. does not count the actual number of games)

    Args:
        team_ids:
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
    """
    return np.array([np.sum(matches == id) for id in team_ids])


def make_win_matrix(
    N_team: int,
    matches: np.ndarray,
    results: np.ndarray,
) -> np.ndarray:
    """
    Produces an N_team x N_team matrix, where row (i,j) counts
    the number of times team i has beaten team j.

    Args:
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
        results: An array of shape (num_matches, 2), where each row corresponds to
                 an element of matches and each column corresponds to a team. The
                 items in each column counts the number of times that team won that
                 matchup. 
    """
    
    win_matrix = np.zeros(shape=(N_team, N_team), dtype=np.int32)
    for index, match in enumerate(matches):
        win_matrix[match[0], match[1]] = results[index, 0]
        win_matrix[match[1], match[0]] = results[index, 1]
    return win_matrix
