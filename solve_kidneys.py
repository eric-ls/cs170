import copy

class Graph:

  def __init__(self, cardinality, children_indices):
    self.cardinality = cardinality
    self.children_indices = dict(zip(children_indices, [True for _ in range(len(children_indices))]))
    self.incoming_edges = {}
    self.iterations = 0
    self.outgoing_edges = {}
    self.vertices = [index for index in range(cardinality)]

  def add_incoming_edge(self, frm, to):
    if to in self.incoming_edges:
      self.incoming_edges[to].add(frm)
    else:
      self.incoming_edges[to] = set([frm])

  def remove_incoming_edge(self, frm, to):
    self.incoming_edges[to].remove(frm)

  def add_outgoing_edge(self, frm, to):
    if frm in self.outgoing_edges:
      self.outgoing_edges[frm].add(to)
    else:
      self.outgoing_edges[frm] = set([to])

  def remove_outgoing_edge(self, frm, to):
    self.outgoing_edges[frm].remove(to)

  def output_attributes(self):
    print self.cardinality
    print self.children_indices
    print self.incoming_edges
    print self.outgoing_edges
    print self.vertices

  def summary(self):
    print "FINAL LENGTH: " + str(len(self.vertices))
    print "NUM OF ITERATIONS: " + str(self.iterations)

  def prune(self):
    should_continue = True

    def prune_vertex(vertex):
      if vertex in self.outgoing_edges:
        neighbors = self.outgoing_edges.pop(vertex)
        for neighbor in neighbors:
          self.remove_incoming_edge(vertex, neighbor)
      if vertex in self.incoming_edges:
        parents = self.incoming_edges.pop(vertex)
        for parent in parents:
          self.remove_outgoing_edge(parent, vertex)

    while should_continue:
      self.iterations += 1
      should_continue = False
      to_remove = []
      for vertex in self.vertices:
        if vertex not in self.incoming_edges or len(self.incoming_edges[vertex]) is 0:
          prune_vertex(vertex)
          to_remove += [vertex]
        elif vertex not in self.outgoing_edges or len(self.outgoing_edges[vertex]) is 0:
          prune_vertex(vertex)
          to_remove += [vertex]
      for _ in to_remove:
        should_continue = True
        self.vertices.remove(_)

def initialize(file_name):
  with open(file_name, 'r') as file_instance:
    cardinality = int(file_instance.readline())
    children_line = file_instance.readline().strip()
    if len(children_line) > 0:
      children_indices = [int(child) for child in children_line.split(' ')]
    else:
      children_indices = []
    graph_instance = Graph(cardinality, children_indices)
    current_index = 0
    current_line = file_instance.readline().strip()
    while len(current_line) > 0:
      neighbor_indices = [int(neighbor) for neighbor in current_line.split(' ')]
      for neighbor_index, is_edge in enumerate(neighbor_indices):
        if is_edge is 1:
          graph_instance.add_incoming_edge(current_index, neighbor_index)
          graph_instance.add_outgoing_edge(current_index, neighbor_index)
      current_line = file_instance.readline().strip()
      current_index += 1
    graph_instance.prune()
    return graph_instance

def findTwentyCycles(graph, vertexIndex, marked=None):
  outgoingEdgesMap = graph.outgoing_edges
  if marked == None:
    marked = set()

  paths = []
  unmarkingDFS(vertexIndex, vertexIndex, outgoingEdgesMap, marked, [], 0, paths, 20)
  return paths

def unmarkingDFS(startvertex, vertex, outgoingEdgesMap, marked, stack, depth, paths, pathCap):
  if vertex not in marked and len(paths) < pathCap:

    marked.add(vertex)
    stack.append(vertex)

    if depth < 5:
      for outgoingVertex in (outgoingEdgesMap[vertex]):
        if outgoingVertex == startvertex:
          # we've found a path
          # the path is the stack
          path = copy.copy(stack)
          paths.append(path)

        else:
          unmarkingDFS(startvertex, outgoingVertex, outgoingEdgesMap, marked, stack, depth + 1, paths, pathCap)

    marked.remove(vertex)
    stack.pop()

def assignCycles(graph):

  # maps vertices to their assigned cycle
  assignedCycles = {}

  def sortfunc(vertex):
    if vertex in graph.children_indices:
      return 0
    else:
      return 1
  allVertices = sorted(graph.vertices, key=sortfunc)
  # iterate through all the vertices, considering one at a time
  for vertex in allVertices:

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


def solve_kidneys(filename):
	graph = initialize(filename)
	cycles_list = assignCycles(graph)
	return cycles_list

def format_string(cycles):
  if len(cycles) == 0:
    return "None"

  strCyclesList = [' '.join(str(i) for i in tup) for tup in cycles]
  return '; '.join(strCyclesList)

def output():
  output = open('solutions.out', 'w')
  for i in range(1, 493):
    file_name = "instances/" + str(i) + ".in"
    cycles_list = solve_kidneys(file_name)
    instance_string = format_string(cycles_list)
    print(instance_string)
    output.write(instance_string + '\n')

instance = 340
def output_instance(instance):
  output = open('solutions.out', 'w')
  file_name = "instances/" + str(instance) + ".in"
  cycles_list = solve_kidneys(file_name)
  instance_string = format_string(cycles_list)
  print(instance_string)
  output.write(instance_string + '\n')

output()
# output_instance()
