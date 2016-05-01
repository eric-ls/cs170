class Graph:

  def __init__(self, cardinality, children_indices):
    self.cardinality = cardinality
    self.children_indices = dict(zip(children_indices, [True for _ in range(len(children_indices))]))
    self.incoming_edges = {}
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
    children_line = file_instance.readline()
    if len(children_line.strip()) > 0:
      children_indices = [int(child) for child in children_line.split(' ')]
    else:
      children_indices = []
    graph_instance = Graph(cardinality, children_indices)
    current_index = 0
    current_line = file_instance.readline()
    while len(current_line) > 0:
      neighbor_indices = [int(neighbor) for neighbor in current_line.split(' ')]
      for neighbor_index, is_edge in enumerate(neighbor_indices):
        if is_edge is 1:
          graph_instance.add_incoming_edge(current_index, neighbor_index)
          graph_instance.add_outgoing_edge(current_index, neighbor_index)
      current_line = file_instance.readline()
      current_index += 1
    graph_instance.prune()
    return graph_instance

# g = Graph(5, [])
# g.add_outgoing_edge(1, 5)
# g.add_outgoing_edge(1, 10)
# g.add_incoming_edge(3, 5)
# g.add_incoming_edge(2, 5)

