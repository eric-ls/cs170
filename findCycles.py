import copy
import initialize

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


def testOne():
    index = 0
    # outgoing = {0:set([1]), 1:set([2]), 2:set([3]), 3:set([4]), 4:set([0])}
    graph = initialize.initialize("simple_instance.in")
    output = [[0, 1, 2, 3, 4]]
    print "\ncomputed value: " + str(findTwentyCycles(graph, index))
    print "answer:         " + str(output) + "\n"

def testTwo():
    index = 2
    # outgoing = {0:set([1]), 1:set([2]), 2:set([3]), 3:set([4]), 4:set([0, 2])}
    graph = initialize.initialize("simple_instance2.in")
    output = [[2, 3, 4, 0, 1], [2, 3, 4]]
    print "\ncomputed value: " + str(findTwentyCycles(graph, index))
    print "answer:         " + str(output) + "\n"

def testThree():
    index = 1
    outgoing = {0:set([1, 3, 6]), 1:set([4, 7]), 2:set([0, 1]), 3:set([]), 4:set([5]), 5:set([2]), 6:set([9]), 7:set([]), 8:set([2, 7, 10]), 9:set([10])}
    output = [[1, 4, 5, 2, 0], [1, 4, 5, 2]]
    print "\ncomputed value: " + str(findTwentyCycles(outgoing, index))
    print "answer:         " + str(output) + "\n"

# class Graph(object):
#   pass

def testFour():
    index = 1
    outgoing = {0:set([1, 3, 6]), 1:set([4, 7]), 2:set([0, 1]), 3:set([]), 4:set([5]), 5:set([2]), 6:set([9]), 7:set([]), 8:set([2, 7, 10]), 9:set([10])}
    output = []
    marked = set([2])
    graph = Graph()
    graph.outgoing_edges = outgoing
    print "\ncomputed value: " + str(findTwentyCycles(graph, index, marked))
    print "answer:         " + str(output) + "\n"

def runTests():
    #testOne()
    #testTwo()
    # testThree()
    # testFour()
    pass

# runTests()