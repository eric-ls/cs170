# num of vertices, vertex index, dict of key = vertex V & values = set of vertices V has outgoing edges to,
# dict of key = vertex V & values = set of vertices V has incoming edges from

num = 10
index = 0
outgoing = {0:set([1]), 1:set([2]), 2:set([3]), 3:set([4]), 4:set([0, 2])}
incoming = {0:set([4]), 1:set([0]), 2:set([1, 4]), 3:set([2]), 4:set([3])}

output = [[0, 1, 2, 3, 4], [2, 3, 4]]

num = 10
index = 1
outgoing = {0:set([1, 3, 6]), 1:set([4, 7]) 2:set([0, 1]), 3:set([]), 4:set([5]), 5:set([2]), 6:set([9]), 7:set([]), 8:set([2, 7, 10]), 9:set([10])}

output = set([[1, 4, 5, 2], [1, 4, 5, 2, 0]])
