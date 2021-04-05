import utility as ut
import math
pi = math.pi
k = 1.1 # Constant for node forces (Point charges acting under Coulomb's Law)
c2 = 1.25 # Constant for edge forces (Springs acting under Hookes Law)
m = .1 # Total Force multiplier
step = .1 # Step time constant

# nodes_lst is a list where each element represents a node as a 3 element list. 
# Element 0 is the name, Element 1 is the charge, and Element 2 is the mass

# edges_lst is a list where each element represents an edge as a 3 element list. 
# Element 0 is the starting node, Element 1 is the ending node, Element 2 is the force multiplier


# movement_lst is a list where each element represents a node's movement as a 2 element list.
# Element 0 is the x velocity, 1 is the y velocity

def to_cartesian(mag, theta):
	'''Converts Polar velocity to Cartesian velocity in units of x and y.'''
	return mag * math.cos(theta), mag * math.sin(theta)

def to_polar(x, y):
	'''Converts Cartesian x and y velocity to Polar velocity in magnitude and radians.'''
	theta = ut.find_theta(0, x, 0, y)
	mag = math.sqrt(x * x + y * y)
	return mag, theta

def force_directed_sort(edges_lst, nodes_lst, positions):
	movement_lst = []
	maxVelo = 10000
	for i in range(len(nodes_lst)):
		movement_lst.append([0,0])

	i = 0
	while i < 65:
		positions, movement_lst, maxVelo = one_iteration(edges_lst, nodes_lst, positions, movement_lst, step)
		i += 1
	while i < 100 and maxVelo > .75:
		positions, movement_lst, maxVelo = one_iteration(edges_lst, nodes_lst, positions, movement_lst, step)
		i += 1
	return positions

def single_node_force(n0, n1, positions):
	'''Returns the magnitude and direction of the force on n0 from n1 using inverse square distnce and
	   assuming that both particles have charge of 1C.'''
	x0, y0 = positions[n0[0]]
	x1, y1 = positions[n1[0]]
	theta = ut.find_theta(x1, x0, y1, y0)
	dist = ut.find_dist(x0, x1, y0, y1)
	mag = k * n0[1] * n1[1] / (dist ** 2)
	return mag, theta

def total_node_force(ind, nodes_lst, positions):
	'''Returns the total force of nodes on node at position i in the nodes_lst.'''
	x, y = 0, 0
	for i in range(len(nodes_lst)):
		if i != ind:
			mag, theta = single_node_force(nodes_lst[ind], nodes_lst[i], positions)
			dx, dy = to_cartesian(mag, theta)
			x += dx
			y += dy
	return x, y

def single_edge_force(n0, n1, c1, positions):
	'''Returns the magnitude and direction of the force on n0 from the edge connecting
	   n0 to n1 using logarithmic force and multiplier c1 (characteristic of the edge itself).'''
	x0, y0 = positions[n0]
	x1, y1 = positions[n1]
	if x1 == x0 and y1 == y0:
		return 0, 0
	theta = ut.find_theta(x0, x1, y0, y1)
	dist = ut.find_dist(x0, x1, y0, y1)
	mag = c1 * math.log(dist / c2)
	return mag, theta

def total_edge_force(n, edges_lst, nodes_lst, positions):
	'''Returns the total force of all edges conatining node n.'''
	x, y = 0, 0
	for edge in edges_lst:
		mag, theta = 0, 1
		if edge[0] == n[0]:
			mag, theta = single_edge_force(edge[0], edge[1], edge[2], positions)
		elif edge[1] == n[0]:
			mag, theta = single_edge_force(edge[1], edge[0], edge[2], positions)
		dx, dy = to_cartesian(mag, theta)
		x += dx
		y += dy
	return x, y

def total_acceleration(ind, edges_lst, nodes_lst, positions):
	'''Returns the total acceleration of the node at index 'ind' of nodes_lst.'''
	x1, y1 = total_node_force(ind, nodes_lst, positions)
	x2, y2 = total_edge_force(nodes_lst[ind], edges_lst, nodes_lst, positions)
	x = x1 + x2
	y = y1 + y2
	mag, theta = to_polar(x, y)
	mag = mag * m / nodes_lst[ind][2]
	return to_cartesian(mag, theta)

def one_iteration(edges_lst, nodes_lst, positions, movement_lst, step):
	'''Runs one iteration of duration 'step' on the nodes in nodes_lst.'''
	maxVelo = 0
	for i in range(len(nodes_lst)):
		ax, ay = total_acceleration(i, edges_lst, nodes_lst, positions)
		vx, vy = movement_lst[i][0], movement_lst[i][1]
		vx += step * ax
		vy += step * ay
		movement_lst[i] = [vx, vy]
		magVelo = math.sqrt(vx * vx + vy * vy)
		if  magVelo > maxVelo:
			maxVelo = magVelo

	for i in range(len(nodes_lst)):
		node = nodes_lst[i]
		x, y = positions[node[0]]
		vx, vy = movement_lst[i][0], movement_lst[i][1]
		x += step * vx
		y += step * vy
		positions[node[0]] = [x, y]

	return positions, movement_lst, maxVelo
