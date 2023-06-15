from __future__ import annotations

import random

import networkx as nx
import numpy as np


def dense(teams: list[object]) -> np.ndarray:
    r"""
    Generates a fully connected set of edges. Each team is
    connected to every other one.

    Inputs:
            :teams: set of teams.

    Outputs:

            np.ndarray shape (N_edges, 2)

    """
    g = nx.complete_graph(len(teams))

    # Select only the node index pairs, exclude the feature dict.
    return np.stack(g.edges(data=False))


def random_connected(teams: list[object], min_n_matches: int) -> np.ndarray:
    r"""
    Returns a spanning tree graph generated from the fully
    connected graph over the teams, and adds some additional
    edges on top. The edges are added in such a way that
    every team is connected to a minimum number of other teams.

    Args:

        :teams: list of team objects

        :min_n_matches: int, ensure that every team will play
            at least this number of matches.

    Outputs:

            np.ndarray shape (N_edges, 2)

    """
    g = nx.complete_graph(len(teams))

    mst = nx.algorithms.tree.random_spanning_tree(g)

    for node in mst.nodes:
        if mst.degree[node] < min_n_matches:
            # Get the nodes which will potentially be connected to
            # the current node.
            candidate_nodes = [
                n for n in mst.nodes if n not in mst.neighbors(node) and n != node
            ]
            # print(node, list(mst.neighbors(node)), candidate_nodes)
            selected_nodes = random.sample(
                candidate_nodes, min_n_matches - mst.degree[node]
            )

            mst.add_edges_from([(node, sel_node) for sel_node in selected_nodes])

    return np.stack(mst.edges)
