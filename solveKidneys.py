from initialize import initialize
from assignVertices import assignCycles

def solveKidneys(filename):
	graph = initialize(filename)
	cycles_list = assignCycles(graph)
	print cycles_list

solveKidneys("backtracking_instance.in")