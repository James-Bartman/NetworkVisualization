import networkbuild as nb
import networkvis as nv
import csv

# file paths
# infopath='DataFiles/KatieResearch/PrioritizationTesting/InfoResourcesZoomA.csv'
# physpath='DataFiles/KatieResearch/PrioritizationTesting/PhysResourcesZoomA.csv'
# allocpath='DataFiles/KatieResearch/PrioritizationTesting/AllocationZoomA.csv'
# infopath = 'data/KatieResearch/FinalReportFiles/InfoResourcesFull.csv'
# infopath='DataFiles/KatieResearch/InfoResourcesFullRobot.csv'
# physpath = 'data/KatieResearch/FinalReportFiles/PhysResourcesFull.csv'
# allocpath = '../data/KatieResearch/FinalReportFiles/AllocationFull.csv'
# allocpath='DataFiles/KatieResearch/AllocationFullRobot.csv'
# fpath = 'data/UTMOps/'
# fpath = 'data/KatieResearch/HFES/'
fpath = 'data/KatieResearch/HFES/case_study/'

# Prefix for nodes in data files
WMname = 'MaintenanceWM'

skipName = 'actionName' # If there is a "Labeling" top line, what is the first element so we can know to skip that when reading

def main():
	# Load file with work allocation
	data = nb.load_data(fpath, WMname)

	# Create separate info & physical resource networks
	G_info = nb.create_network(data.infoEdges, data.actionNodes, WMname, True)
	G_phys = nb.create_network(data.physEdges, data.actionNodes, WMname, False)

	# Prompting user whether or not we should remove cycles
	remEdge = int(input('\nDo you want to remove cyclical edges (1 for yes, 0 for no): '))

	# Create network with just actions
	G, removed_edges = nb.compute_information_constraints(G_info, remEdge)
	G2 = nb.remove_allocation(G)
	G_full, removed_edges = nb.compute_information_constraints_full(G_info, removed_edges, remEdge)
	G2_full = nb.remove_allocation(G_full)
	
	# Separate strategies by control mode
	ctrlmodes = ['-1','0','1']

	# Create an agent list and node agents dictionary holding all the possible agents 
	# and which nodes are assigned to which agents from the csv
	node_agents = {}
	agent_list = []
	with open(fpath+'actionNodes.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter =',', quotechar='|')
		# Skip the first line with header
		next(reader)
		for row in reader:
			if row[0] == 'actionName':
				continue
			if row[1]=='':
				node_agents[row[0][len(WMname):]] = 'Unassigned'
			else:
				node_agents[row[0][len(WMname):]] = row[1]
				if row[1] not in agent_list:
					agent_list.append(row[1])
	agent_list.append('Unassigned')
	agent_list.append(None)

	# Create empty arrays to hold the figures visualizing our networks
	alloc_figs = []
	noalloc_figs = []
	force_alloc_figs = []
	force_no_figs = []
	cluster_figs = []
	full_alloc_figs = []
	full_noalloc_figs = []
	full_force_alloc_figs = []
	full_force_no_figs = []
	full_cluster_figs = []

	positionsArray = [0, 0, 0, 0, 0, 0] # Will hold positions of nodes under the 6 different combinations of sorting algorithms and graph data

	for c in ctrlmodes:
		# If we are on first control mode, we need to get the positions under each sorting algorithm and store them
		if int(c) == -1:
			fig, positionsArray[0] = nv.visualize_network(G, c,'topo', node_agents)
			alloc_figs.append(fig)
			fig, positionsArray[1] = nv.visualize_network(G, c, 'force', node_agents)
			force_alloc_figs.append(fig)
			fig, positionsArray[2] = nv.visualize_network(G, c,'clustered', node_agents)
			cluster_figs.append(fig)
			fig, positionsArray[3] = nv.visualize_network(G_full, c,'topo', node_agents)
			full_alloc_figs.append(fig)
			fig, positionsArray[4] = nv.visualize_network(G_full, c,'force', node_agents)
			full_force_alloc_figs.append(fig)
			fig, positionsArray[5] = nv.visualize_network(G_full, c,'clustered', node_agents)
			full_cluster_figs.append(fig)
		# If we've already sorted the graphs, just use those predetermined positions for the other control modes, all that changes is which edges are shown
		else:
			alloc_figs.append(nv.visualize_network_positions(G, c,'topo', node_agents, positionsArray[0]))
			force_alloc_figs.append(nv.visualize_network_positions(G, c, 'force', node_agents, positionsArray[1]))
			cluster_figs.append(nv.visualize_network_positions(G, c,'clustered', node_agents, positionsArray[2]))
			full_alloc_figs.append(nv.visualize_network_positions(G_full, c,'topo', node_agents, positionsArray[3]))
			full_force_alloc_figs.append(nv.visualize_network_positions(G_full, c,'force', node_agents, positionsArray[4]))
			full_cluster_figs.append(nv.visualize_network_positions(G_full, c,'clustered', node_agents, positionsArray[5]))
		
		# The no allocation graphs can just take their positions from the allocation graphs, all that changes is labeling
		noalloc_figs.append(nv.visualize_network_positions(G2, c, 'topo', node_agents, positionsArray[0]))
		force_no_figs.append(nv.visualize_network_positions(G2, c, 'force', node_agents, positionsArray[1]))
		full_noalloc_figs.append(nv.visualize_network_positions(G2_full, c,'topo', node_agents, positionsArray[3]))
		full_force_no_figs.append(nv.visualize_network_positions(G2_full, c,'force', node_agents, positionsArray[4]))


	# Put the topological sorted and force sorted arrays into 2 easy to find dictionaries
	topo_figs = {'show': alloc_figs, 'no-show': noalloc_figs, 'show-full': full_alloc_figs, 'no-show-full': full_noalloc_figs}
	force_figs = {'showf': force_alloc_figs, 'no-showf': force_no_figs, 'show-fullf': full_force_alloc_figs, 'no-show-fullf': full_force_no_figs}
	return topo_figs, cluster_figs, full_cluster_figs, force_figs
