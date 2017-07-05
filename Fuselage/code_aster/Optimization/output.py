import json
import sys

with open(sys.argv[1]) as fson:
    output = json.load(fson)

with open(sys.argv[2]) as f:
    floats = map(float, f)

results = []

# Objective Function
results.append(output['mass'])
# Modify Constraints
#################################################
results.append(output['vmises'] - 1e5)
#################################################

printvector = open(sys.argv[3]).read().splitlines()
printvector = [bool(int(i)) for i in printvector]
resultfile = open(sys.argv[4], 'w')
for i in range(0, len(printvector)):
    if (printvector[i]):
	    resultfile.write("%f\n" % results[i])


