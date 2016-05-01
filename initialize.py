class Graph:

  def __init__(self, cardinality, children_indices):
    self.cardinality = cardinality
    self.children_indices = children_indices
    self.incoming_edges = {}
    self.outgoing_edges = {}

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

def initialize(file_name):
  with open(file_name) as file_instance:
    cardinality = int(file_instance.readLine())
    children_indices = [int(child) for child in file_instance.readLine().split(' ')]
    graph_instance = Graph(cardinality, children_indices)
    current_index = 0
    current_line = file_instance.readLine()
    while current_line is not '':
      neighbor_indices = [int(neighbor) for neighbor in current_line.split(' ')]
      for neighbor_index, is_edge in enumerate(neighbor_indices):
        if is_edge is 1:
          graph_instance.add_incoming_edge(current_index, neighbor_index)
          graph_instance.add_outgoing_edge(current_index, neighbor_index)
      current_index += 1

g = Graph(5, [])
g.add_outgoing_edge(1, 5)
g.add_outgoing_edge(1, 10)
g.add_incoming_edge(3, 5)
g.add_incoming_edge(2, 5)

