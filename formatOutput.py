def outputFile(solutions):


def formatString(cycles):
  if len(cycles) == 0:
    return "None"

  strCyclesList = [' '.join(str(i) for i in tup) for tup in cycles]
  return '; '.join(strCyclesList)

