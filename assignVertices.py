import copy
from findCycles import findTwentyCycles

def assignCycles(graph):

	# maps vertices to their assigned cycle
	assignedCycles = {}

	# iterate through all the vertices, considering one at a time
	for vertex in graph.vertices:

		# find cycles for the vertex
		cycles = findTwentyCycles(graph, vertex)

		best_cycle = []
		best_score = 0
		
		bestdisjointCyclesToAdd = []
		bestVerticesToRemoveFromAssigned = []

		for cycle in cycles:

			# find a set of all the vertices in this cycle that are already assigned
			# and compute a score benefit of adding this cycle
			overlappingVertices = set()
			cycle_add_score = 0

			for vertexIndex in cycle:
				if vertexIndex in assignedCycles:
					overlappingVertices.add(vertexIndex)
				if vertexIndex in graph.children_indices:
					cycle_add_score += 2
				else:
					cycle_add_score += 1

			# if some vertices overlap we must backtrack
			if len(overlappingVertices) > 0:
				
				# the set of removed vertices is the union of all cycles
				# of overlapping vertices
				removedVertices = set()
				for overlappingVertex in overlappingVertices:
					removedVertices = removedVertices.union(assignedCycles[overlappingVertex])

				# we want to test out new assignments so we copy assignedCycles
				assignedCopy = copy.deepcopy(assignedCycles)

				# compute the score of removing all vertices of removed vertices
				# remove these vertices from assigned copy (temporary destroy)
				# the cycles
				cycle_remove_score = 0
				for toRemoveVertex in removedVertices:
					assignedCopy.pop(toRemoveVertex)
					if toRemoveVertex in graph.children_indices:
						cycle_remove_score += 2
					else:
						cycle_remove_score += 1

				# temporarily assign the cycle under consideration
				for current_cycle_vertex in cycle:
					assignedCopy[current_cycle_vertex] = cycle

				# For each vertex in a cycle destroyed by adding the current cycle
				disjointCyclesToAdd = []
				disjoint_cycle_add_score = 0
				for toRemoveVertex in removedVertices:

					# compute cycles disjoint from everything in assignedCopy
					disjointCycles = findTwentyCycles(graph, toRemoveVertex, set(assignedCopy.keys()))
					best_disjoint_cycle = None
					best_disjoint_cycle_score = 0
					
					# consider each disjointCycle
					for disjointCycle in disjointCycles:

						# compute the score of adding this disjoint cycle
						disjointCycleScore = 0
						for possibleDisjointCycleVertex in disjointCycle:
							if possibleDisjointCycleVertex in graph.children_indices:
								disjointCycleScore += 2
							else:
								disjointCycleScore += 1

						# if it is greater than any other disjoint cycle
						# FOR this vertex, make it the best
						if disjointCycleScore > best_disjoint_cycle_score:
							best_disjoint_cycle_score = disjointCycleScore
							best_disjoint_cycle = disjointCycle

					# if a best cycle exists
					if best_disjoint_cycle != None:

						# add it to the list of disjoint cycles to add
						# IF we choose the current cycle
						# assign it to assigned so future disjoint cycles dont
						# overlap
						disjointCyclesToAdd.append(best_disjoint_cycle)
						for local_disjoint_cycle_vertex in best_disjoint_cycle:
							assignedCopy[local_disjoint_cycle_vertex] = best_disjoint_cycle
						
						# add this disjoint cycle to the sum of disjoint cycle scores
						# FOR this current cycle
						disjoint_cycle_add_score += best_disjoint_cycle_score

				# the total score of adding this cycle is
				# the sum of all the disjoint cycles we get to add
				# the sum of the cycle itself
				# minus the cost of the cycles we have to remove
				total_score = disjoint_cycle_add_score + cycle_add_score - cycle_remove_score
				
				# update everything IF this is the best situation
				if total_score > best_score:
					best_score = total_score
					best_cycle = cycle
					bestdisjointCyclesToAdd = disjointCyclesToAdd
					bestVerticesToRemoveFromAssigned = removedVertices

			# no overlapping vertices
			else:
				# then we can greedily compute the score, as it is disjoint
				if cycle_add_score > best_score:
					best_cycle = cycle
					best_score = cycle_add_score

		# remove the destroyed cycles
		for removalVertex in bestVerticesToRemoveFromAssigned:
			assignedCycles.pop(removalVertex)

		# assign the chosen cycle
		for best_cycle_vertex in best_cycle:
			assignedCycles[best_cycle_vertex] = best_cycle

		# add the replacement disjoint cycles
		for disjointCycle in bestdisjointCyclesToAdd:
			for disjoint_cycle_vertex in disjointCycle:
				assignedCycles[disjoint_cycle_vertex] = disjointCycle

	# return a list of tuples
	final_cycles_set = set()
	for key, value in assignedCycles.iteritems():
		final_cycles_set.add(tuple(value))
	final_cycles_list = list(final_cycles_set)
	return final_cycles_list

