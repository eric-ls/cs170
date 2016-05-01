from initialize import initialize
from assignVertices import assignCycles

def solveKidneys(filename):
	graph = initialize(filename)
	cycles_list = assignCycles(graph)
	return cycles_list

def formatString(cycles):
  if len(cycles) == 0:
    return "None"

  strCyclesList = [' '.join(str(i) for i in tup) for tup in cycles]
  return '; '.join(strCyclesList)

def output():
  output = open('solutions.out', 'w')
  for i in range(1, 493):
    filename = "instances/" + str(i) + ".in"
    cycles_list = solveKidneys(filename)
    instanceString = formatString(cycles_list)
    print(instanceString)
    output.write(instanceString + '\n')

instance = 340
def outputInstance(instance):
  output = open('solutions.out', 'w')
  filename = "instances/" + str(instance) + ".in"
  cycles_list = solveKidneys(filename)
  instanceString = formatString(cycles_list)
  print(instanceString)
  output.write(instanceString + '\n')

output()
# outputInstance()
