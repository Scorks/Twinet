import sys
import numpy
import os
import operator

input_file = open(sys.argv[1], 'r').read().split('\n')

alpha = sys.argv[2]
beta = sys.argv[3]
conversion_dict = {} # dictionary for conversion of original node values to matrix values (1,2,...n)
adjacency_dict = {} # dictionary for storing the adjacency matrix information
degree_dict = {} # dictionary for storing the degree values for each node
pagerank_dict = {} # dictionary for storing the final pagerank value for each node
final_dict = {} # dictionary for storing the completed output

scoring_dict = {} # keeps track of the final point scoring for recommended users

#-----------------------------------------------------------------------------------------------------

count = 0 # count used for relabelling nodes
for line in iter(input_file):
	line = line.split()
	if line:
		# creating the conversion dictionary
		if (line[0] not in conversion_dict):
			conversion_dict[line[0]] = count
			count+=1
		if (line[1] not in conversion_dict):
			conversion_dict[line[1]] = count
			count+=1
		if(conversion_dict[line[0]] in degree_dict):
			degree_dict[conversion_dict[line[0]]] += 1
		elif (conversion_dict[line[0]] not in degree_dict):
			degree_dict[conversion_dict[line[0]]] = 1
		adjacency_dict[(conversion_dict[line[0]], conversion_dict[line[1]])] = 1

# ALPHA-ADJACENCY MATRIX CREATION --------------------------------------------------------------------

n = len(conversion_dict) # our adjacency matrix will be n x n
adjacency_matrix = [[0 for x in range(n)] for y in range(n)]

for x in adjacency_dict:
	adjacency_matrix[x[1]][x[0]] = float(adjacency_dict[x]) * float(alpha)

# DIAGONAL MATRIX CREATION (D_ii = the max(1, K_i))---------------------------------------------------

diagonal_matrix = [[0 for x in range(n)] for y in range(n)]
for x in range(0, n):
	if x in degree_dict:
		diagonal_matrix[x][x] = max(1, degree_dict[x])
	else:
		diagonal_matrix[x][x] = 1

# DIAGONAL MATRIX MINUS ALPYHA-ADJACENCY MATRIX-------------------------------------------------------
d_minus_a_matrix = [[0 for x in range(n)] for y in range(n)]
for x in range(0, n):
	for y in range(0, n):
		d_minus_a_matrix[x][y] = (float(diagonal_matrix[x][y])-float(adjacency_matrix[x][y]))

# ----------------------------------------------------------------------------------------------------

DIAG = numpy.matrix(diagonal_matrix)
A = numpy.matrix(d_minus_a_matrix)
A = A.I # obtaining the inverse matrix

C = numpy.dot(DIAG, A)
C = C * float(beta)

final_matrix = [[0 for x in range(n)] for y in range(n)] # creating empty final matrix

for x in range(0, n):
	for y in range(0, n):
		final_matrix[x][y] = C[x,y]

for x in range(0, n):
	pagerank = 0.0
	for y in final_matrix[x]:
		pagerank += y
	pagerank_dict[x] = pagerank

# REMATCHING NODE LABELS AND PRINTING RESULTS---------------------------------------------------------

for key, value in conversion_dict.items():
	final_dict[key] = pagerank_dict[value]

# RETRIEVING TOP RESULTS-------------------------------------------------------------------------------

pagerank_t1 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
pagerank_t1_value = final_dict[pagerank_t1]
del final_dict[pagerank_t1]
pagerank_t2 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
pagerank_t2_value = final_dict[pagerank_t2]
del final_dict[pagerank_t2]
pagerank_t3 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
pagerank_t3_value = final_dict[pagerank_t3]

# setting initial dictionary values
scoring_dict[pagerank_t1] = 3
scoring_dict[pagerank_t2] = 2
scoring_dict[pagerank_t3] = 1

# BETWEENNESS CENTRALITY------------------------------------------------------------------------------

udc = {y:x for x,y in conversion_dict.iteritems()} # UDC is the updated conversion dictionary, swapping key/value pairs

input_file = open(sys.argv[1], 'r').read().split('\n')

adjacency_dict = {} # dictionary to store adjacent vertices
visited_dict = {} # dictionary to store the visited status of all vertices
node_list = []
components = []

def print_dict(dictionary):
	for key in dictionary:
		dictionary[int(key)] = dictionary.pop(key)
	for key, value in sorted(dictionary.items()):
		print (key, value)

# FILL ADJACENCY_DICT:

for line in iter(input_file):
	line = line.split()
	if line:
		# creating a list of all the vertices
		line[0] = int(conversion_dict[line[0]])
		line[1] = int(conversion_dict[line[1]])
		if line[1] not in node_list:
			node_list.append(line[1])
		if line[0] not in node_list:
			node_list.append(line[0])
		# creating the dictionary
		if (line[0] in adjacency_dict):
			adjacency_dict[line[0]].append(line[1])
		else:
			adjacency_dict[line[0]] = []
			adjacency_dict[line[0]].append(line[1])
		if (line[1] in adjacency_dict):
			adjacency_dict[line[1]].append(line[0])
		else:
			adjacency_dict[line[1]] = []
			adjacency_dict[line[1]].append(line[0])

#-------------------------------------------------------------------------------------

maxval = max(adjacency_dict, key=int)

for i in range (0, maxval+1):
	if not i in adjacency_dict:
		adjacency_dict[i] = []

#-------------------------------------------------------------------------------------

totals = [0] * len(adjacency_dict) # final values to print

for vertex in adjacency_dict: # for all vertices
	x_array = {} # X_i values
	dist_array = {} # initialize empty distance array
	weight_array =  {}
	for index in adjacency_dict:
		dist_array[index] = -1 # initialize all key values to inifity
		weight_array[index] = 0 # initialize all key values to 0
		x_array[index] = 0
	dist_array[vertex] = 0 # initialize vertex s distance to 0
	weight_array[vertex] = 1 # initialize vertex s weight to 1
	d = 0
	while d in (dist_array.values()):
		for i in adjacency_dict:
			if (dist_array[i] == d):
				for neighbor in adjacency_dict[i]:
					if dist_array[neighbor] == -1:
						dist_array[neighbor] = d+1 # distance[neighbor] = d+1
						weight_array[neighbor] = weight_array[i] # W_j = W_i
					elif (dist_array[neighbor] == d+1):
						weight_array[neighbor] += weight_array[i]
					elif (dist_array[neighbor] <= d):
						continue
		d = d + 1
	d = d-1 # maximum layer
	for z in adjacency_dict:
		if dist_array[z] == d:
			x_array[z] = 1
# all terminal vertices are 1
	d = d - 1
	while (d >= 0):
		for i in adjacency_dict:
			if (dist_array[i] == d): # for each vertex i in the next layer up
				summation = 0
				for neighbor in adjacency_dict[i]:
					#if (x_array[neighbor] is not 0):
					if (dist_array[neighbor] == d+1):
						summation = summation + (float(x_array[neighbor]) * (float(weight_array[i])/float(weight_array[neighbor])))
				x_array[i] = summation + 1
		d = d - 1
	for i in adjacency_dict:
		totals[i] += x_array[i]

# RETRIEVING TOP RESULTS-------------------------------------------------------------------------------

final_dict = {}

for i in sorted(adjacency_dict.keys()):
	final_dict[(udc[i])] = totals[i]

betweenness_t1 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
betweenness_t1_value = final_dict[betweenness_t1]
del final_dict[betweenness_t1]
betweenness_t2 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
betweenness_t2_value = final_dict[betweenness_t2]
del final_dict[betweenness_t2]
betweenness_t3 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
betweenness_t3_value = final_dict[betweenness_t3]

if (betweenness_t1 in scoring_dict):
	scoring_dict[betweenness_t1] += 3
else:
	scoring_dict[betweenness_t1] = 3
if (betweenness_t2 in scoring_dict):
	scoring_dict[betweenness_t2] += 2
else:
	scoring_dict[betweenness_t2] = 2
if (betweenness_t3 in scoring_dict):
	scoring_dict[betweenness_t3] += 1
else:
	scoring_dict[betweenness_t3] = 1

# CLOSENESS CENTRALITY---------------------------------------------------------------------------------

input_file = open(sys.argv[1], 'r').read().split('\n')

adjacency_dict = {} # dictionary to store adjacent vertices
visited_dict = {} # dictionary to store the visited status of all vertices
final_dict = {}
node_list = []
components = []

def print_dict(dictionary):
	for key in dictionary:
		dictionary[int(key)] = dictionary.pop(key)
	for key, value in sorted(dictionary.items()):
		print (key, value)

# FILL ADJACENCY_DICT:

for line in iter(input_file):
	line = line.split()
	if line:
		# creating a list of all the vertices
		line[0] = int(conversion_dict[line[0]])
		line[1] = int(conversion_dict[line[1]])
		if line[1] not in node_list:
			node_list.append(line[1])
		if line[0] not in node_list:
			node_list.append(line[0])
		# creating the dictionary
		if (line[0] in adjacency_dict):
			adjacency_dict[line[0]].append(line[1])
		else:
			adjacency_dict[line[0]] = []
			adjacency_dict[line[0]].append(line[1])
		if (line[1] in adjacency_dict):
			adjacency_dict[line[1]].append(line[0])
		else:
			adjacency_dict[line[1]] = []
			adjacency_dict[line[1]].append(line[0])

#-------------------------------------------------------------------------------------

maxval = max(adjacency_dict, key=int)

for i in range (0, maxval+1):
	if not i in adjacency_dict:
		adjacency_dict[i] = []

#-------------------------------------------------------------------------------------
n = len(adjacency_dict)

for vertex in adjacency_dict: # for all vertices
	x_array = {} # X_i values
	dist_array = {} # initialize empty distance array
	weight_array =  {}
	for index in adjacency_dict:
		dist_array[index] = -1 # initialize all key values to inifity
		weight_array[index] = 0 # initialize all key values to 0
		x_array[index] = 0
	dist_array[vertex] = 0 # initialize vertex s distance to 0
	weight_array[vertex] = 1 # initialize vertex s weight to 1
	d = 0
	while d in (dist_array.values()):
		for i in adjacency_dict:
			if (dist_array[i] == d):
				for neighbor in adjacency_dict[i]:
					if dist_array[neighbor] == -1:
						dist_array[neighbor] = d+1 # distance[neighbor] = d+1
						weight_array[neighbor] = weight_array[i] # W_j = W_i
					elif (dist_array[neighbor] == d+1):
						weight_array[neighbor] += weight_array[i]
					elif (dist_array[neighbor] <= d):
						continue
		d = d + 1
	summ = 0
	for item in dist_array:
		if (dist_array[item] != -1) and (dist_array[item] != 0):
			summ += (1/float(dist_array[item]))
	final = summ * (1.0/(n-1))
	final_dict[udc[vertex]] = str(final)
	# print str(udc[vertex]) + " : " + str(final)

# RETRIEVING TOP RESULTS-------------------------------------------------------------------------------

closeness_t1 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
closeness_t1_value = final_dict[closeness_t1]
del final_dict[closeness_t1]
closeness_t2 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
closeness_t2_value = final_dict[closeness_t2]
del final_dict[closeness_t2]
closeness_t3 = max(final_dict.iteritems(), key=operator.itemgetter(1))[0]
closeness_t3_value = final_dict[closeness_t3]

if (closeness_t1 in scoring_dict):
	scoring_dict[closeness_t1] += 3
else:
	scoring_dict[closeness_t1] = 3
if (closeness_t2 in scoring_dict):
	scoring_dict[closeness_t2] += 2
else:
	scoring_dict[closeness_t2] = 2
if (closeness_t3 in scoring_dict):
	scoring_dict[closeness_t3] += 1
else:
	scoring_dict[closeness_t3] = 1

# FINALIZING RESULTS FOR SOCIAL MEDIA RECOMMENDATIONS--------------------------------------------------

result_1 = max(scoring_dict.iteritems(), key=operator.itemgetter(1))[0]
del scoring_dict[result_1]
result_2 = max(scoring_dict.iteritems(), key=operator.itemgetter(1))[0]
del scoring_dict[result_2]
result_3 = max(scoring_dict.iteritems(), key=operator.itemgetter(1))[0]

# print result_1, result_2, result_3

cmd1 = "twurl /1.1/users/show.json?user_id=" + result_1
cmd2 = "twurl /1.1/users/show.json?user_id=" + result_2
cmd3 = "twurl /1.1/users/show.json?user_id=" + result_3

os.system(cmd1 + ' %s > results.txt')

print "Top users recommended for you: "

initial_file = open('results.txt', 'r').read()
initial_file = initial_file.split(',')
for line in initial_file:
	if ('"screen_name":"' in line and '{' not in line): 
		print line

os.system(cmd2 + ' %s > results.txt')

initial_file = open('results.txt', 'r').read()
initial_file = initial_file.split(',')
for line in initial_file:
	if ('"screen_name":"' in line and '{' not in line): 
		print line

os.system(cmd3 + ' %s > results.txt')

initial_file = open('results.txt', 'r').read()
initial_file = initial_file.split(',')
for line in initial_file:
	if ('"screen_name":"' in line and '{' not in line): 
		print line

os.remove("results.txt")