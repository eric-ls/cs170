import copy
from findCycles import findTwentyCycles

def assignCycles(graph):

	# maps vertices to their assigned cycle
	assignedCycles = {}

	for vertex in graph.vertices:
		cycles = findTwentyCycles(graph, vertex)

		best_cycle = []
		best_score = 0
		
		bestdisjointCyclesToAdd = []

		for cycle in cycles:

			# vertices that overlap
			overlappingVertices = set()
			cycle_add_score = 0

			for vertexIndex in cycle:
				if vertexIndex in assignedCycles:
					overlappingVertices.add(vertexIndex)
				if vertexIndex in graph.children_indices:
					cycle_add_score += 2
				else:
					cycle_add_score += 1


			if len(overlappingVertices) > 0:
				# temporary backtrack
				removedVertices = set()
				for overlappingVertex in overlappingVertices:
					removedVertices = removedVertices.union(assignedCycles[overlappingVertex])

				assignedCopy = copy.deepcopy(assignedCycles)
				cycle_remove_score = len(removedVertices)
				for toRemoveVertex in removedVertices:
					assignedCopy.pop(toRemoveVertex)

				for current_cycle_vertex in cycle:
					assignedCopy[current_cycle_vertex] = cycle

				disjointCyclesToAdd = []
				disjoint_cycle_add_score = 0
				for toRemoveVertex in removedVertices:
					disjointCycles = findTwentyCycles(graph, toRemoveVertex, set(assignedCopy.keys()))
					best_disjoint_cycle = None
					best_disjoint_cycle_score = 0
					for disjointCycle in disjointCycles:
						if len(disjointCycle) > best_disjoint_cycle_score:
							best_disjoint_cycle_score = disjointCycle
							best_disjoint_cycle = disjointCycle
					if best_disjoint_cycle != None:
						disjointCyclesToAdd.append(best_disjoint_cycle)
						disjoint_cycle_add_score += len(best_disjoint_cycle)

					if best_disjoint_cycle is not None:
						for local_disjoint_cycle_vertex in best_disjoint_cycle:
							assignedCopy[local_disjoint_cycle_vertex] = best_disjoint_cycle


				total_score = disjoint_cycle_add_score + cycle_add_score - cycle_remove_score
				if total_score > best_score:
					best_score = total_score
					best_cycle = cycle
					bestdisjointCyclesToAdd = disjointCyclesToAdd

			else:
				if cycle_add_score > best_score:
					best_cycle = cycle
					best_score = cycle_add_score

		for best_cycle_vertex in best_cycle:
			assignedCycles[best_cycle_vertex] = best_cycle

		for disjointCycle in bestdisjointCyclesToAdd:
			for disjoint_cycle_vertex in disjointCycle:
				assignedCycles[disjoint_cycle_vertex] = disjointCycle

	final_cycles_set = set()
	for key, value in assignedCycles.iteritems():
		final_cycles_set.add(tuple(value))
	final_cycles_list = list(final_cycles_set)
	return final_cycles_list

