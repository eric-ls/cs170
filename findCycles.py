import copy

def findTwentyCycles(outgoingEdgesMap, vertexIndex):
	paths = []
	unmarkingDFS(vertexIndex, vertexIndex, outgoingEdgesMap, set(), [], 0, paths, 20)
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


def testOne():
	index = 0
	outgoing = {0:set([1]), 1:set([2]), 2:set([3]), 3:set([4]), 4:set([0])}
	output = [[0, 1, 2, 3, 4]]
	print "\ncomputed value: " + str(findTwentyCycles(outgoing, index))
	print "answer:         " + str(output) + "\n"

def testTwo():
	index = 2
	outgoing = {0:set([1]), 1:set([2]), 2:set([3]), 3:set([4]), 4:set([0, 2])}
	output = [[2, 3, 4, 0, 1], [2, 3, 4]]
	print "\ncomputed value: " + str(findTwentyCycles(outgoing, index))
	print "answer:         " + str(output) + "\n"

def testThree():
	pass

testTwo()