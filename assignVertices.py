def assignCycles(vertices, outgoingEdgesMap, childOrParent):

	#
	assigned = set()
	cyclesCache = {}
	assignCycles = []
	for vertex in vertices:
		if vertex in cyclesCache:
			cycles = cyclesCache[vertex]
		else:
			cycles = findTwentyCycles(outgoingEdgesMap, vertex)

		cycles.append()
		best_cycle = []
		best_score = 0
		for cycle in cycles:
			overlap = False
			for vertexIndex in cycle:
				if vertexIndex in assigned:
					overlap = True

			if overlap:

			else:

