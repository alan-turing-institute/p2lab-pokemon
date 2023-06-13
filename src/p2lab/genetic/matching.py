import networkx as nx
import numpy as np

def dense(teams : list[object]) -> np.ndarray:
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
	return np.stack( g.edges(data=False) )

def mst(teams : list[object]) -> np.ndarray:
	r"""
	Returns a minimum spanning tree graph generated from the
	fully connected graph over the teams.

	Outputs:

		np.ndarray shape (N_edges, 2)

	"""
	g = nx.complete_graph(len(teams))
	mst = nx.algorithms.tree.minimum_spanning_edges(g, data=False)

	return list(mst)

def main():
	
	# Test
	print(mst([0] * 5))
	print(dense([0] * 5))

if __name__ == "__main__":
	main()
