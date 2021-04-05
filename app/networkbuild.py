import csv
import copy
import networkx as nx

# Class for storing data from the csv-files from WMC
class Data:

    # Nodes representing the actions
    actionNodes = []

    # Nodes representing information resources
    infoNodes = []

    # Nodes representing physical resources
    physNodes = []

    # Edges between actions and information resources
    infoEdges = []

    # Edges between actions and physical resources
    physEdges = []

# Reads in csv file and formats actions and resources uniformly
# Returns list of lists with file contents
def load_data(fpath, prefix):

    # Instance of the Data class
    data = Data()

    # Read the csv-file for action nodes and the allocation
    data.actionNodes = []
    # Read in data
    with open(fpath+'actionNodes.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
        # Skip the first line because of header
        next(reader)
        for row in reader:
            if row[0] == 'actionName':
                continue
            # Make node names pretty
            for i in range(3):
                temp = row[i].replace(prefix,'') # remove prefix
                row[i] = "".join(temp) # join separated words into one string
            data.actionNodes.append(row)

    # Read the csv-file for information resource nodes
    data.infoNodes = []
    # Read in data
    with open(fpath+'infoNodes.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
        # Skip the first line because of header
        next(reader)
        for row in reader:
            if row[0] == 'resourceName':
                continue
            data.infoNodes.append(row[0].replace(prefix,'')) # remove prefix

    # Read the csv-file for physical resource nodes
    data.physNodes = []
    # Read in data
    with open(fpath+'physNodes.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
        # Skip the first line because of header
        next(reader)
        for row in reader:
            if row[0] == 'resourceName':
                continue
            data.physNodes.append(row[0].replace(prefix,'')) # remove prefix

    # Read the csv-file for edges between actions and information resources
    data.infoEdges = []
    # Read in data
    with open(fpath+'infoEdges.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
        # Skip the first line because of header
        next(reader)
        for row in reader:
            if row[0] == 'actionName':
                continue
            # Make node names pretty
            for i in range(2):
                # Remove prefix
                temp = row[i].replace(prefix,'')
                # Join separated words into one string
                row[i] = "".join(temp)
            data.infoEdges.append(row)

    # Read the csv-file for edges between actions and physical resources
    data.physEdges = []
    # Read in data
    with open(fpath+'physEdges.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
        # Skip the first line because of header
        next(reader)
        for row in reader:
            if row[0] == 'actionName':
                continue
            # Make node names pretty
            for i in range(1):
                temp = row[i].replace(prefix,'') # remove prefix
                row[i] = "".join(temp) # join separated words into one string
            data.physEdges.append(row)

    return data

def create_network(edges, alloc, prefix, directional):
    '''Builds network from edges and assigns edge & node attributes and returns graph/digraph object.'''
    if directional:
        G = nx.MultiDiGraph()
    else:
        G = nx.Graph()

    agent_dict = {}
    # Add node attribute for assigned agent           
    for row in alloc:
        # Assign 'Unassigned' value to unassigned actions
        if row[1] != '':
            agent_dict[row[0]] = row[1]

    for row in edges:
        # Create edges based on action-resource dependency & add edge attribute for priority
        act = row[0]
        res = row[1]
        
        # Add nodes if they don't already exist
        if not G.has_node(act):
            if "Command" in act:
                G.add_node(act, type = 'TeamworkCommand', agent = agent_dict[act])
            elif "Confirm" in act:
                G.add_node(act, type = 'TeamworkConfirm', agent = agent_dict[act])
            else:
                G.add_node(act, type = 'Action', agent = agent_dict.get(act, 'Unassigned'))
    
        if not G.has_node(res):
            G.add_node(res,type = 'Resource', agent = None)
        
        # Add edge
        if row[2] == 'get':
            G.add_edge(res, act, dependency = row[3])
        else:
            G.add_edge(act, res, dependency = row[3])

    return G

def compute_information_constraints(G_old, remEdge):
    '''Returns the network with actions only.'''
    G = copy.deepcopy(G_old)
    removed_edges = [] # the remove inactive edges
    
    # Remove any cycles in graph if remEdge is True
    if (remEdge):

        # prompt user with cyclical edges and ask which to remove
        cycles = list(nx.simple_cycles(G_old))
        for cycle in cycles:
            try:
                cycle_edges = list(nx.find_cycle(G,cycle[0]))
            except:
                continue

            # Ask user which edge to remove
            # print(f'\nCycle detected for edges: \n')
            # for i in range(len(cycle_edges)):
            #     print(f'edge {i}: {cycle_edges[i]}')
            # edge_remove = int(input('\nEnter number of edge to remove: '))
            edge_remove = 0
            G.remove_edge(cycle_edges[edge_remove][0], cycle_edges[edge_remove][1])
            removed_edges.append(edge_remove)

    # Remove resource nodes
    resource_nodes = [x for x,y in G.nodes(data = True) if y['type'] == 'Resource']
    for n in resource_nodes:
        incoming = list(G.predecessors(n))
        outgoing = list(G.successors(n))
        # Add edge between each incoming and outgoing node
        for i in incoming:
            for j in outgoing:
                dep = G[n][j][0]['dependency']
                G.add_edge(i, j, dependency = dep)
        G.remove_node(n)
    return G, removed_edges


def compute_information_constraints_full(G_old, removed_edges, remEdge):
    '''Returns network with both actions and resources.'''
    G = copy.deepcopy(G_old)
    
    # Remove any cycles in graph if remEdge is True
    if (remEdge):
        i = 0
        cycles = list(nx.simple_cycles(G_old))
        for cycle in cycles:
            try:
                cycle_edges = list(nx.find_cycle(G,cycle[0]))
            except:
                continue
            if i < len(removed_edges):
                G.remove_edge(cycle_edges[removed_edges[i]][0], cycle_edges[removed_edges[i]][1])
                i += 1
            else:
                # Ask user which edge to remove
                # print(f'\nCycle detected for edges: \n')
                # for i in range(len(cycles)):
                #     print(f'edge {i}: {cycle_edges[i]}')
                # edge_remove = int(input('\nEnter number of edge to remove: '))
                edge_remove = 0
                G.remove_edge(cycle_edges[edge_remove][0], cycle_edges[edge_remove][1])
                removed_edges.append(edge_remove)
                
    return G, removed_edges

def separate_networks(G):
    '''Remove soft interdepencies to create separate figures for different control modes.'''
    Gscram = copy.deepcopy(G)
    Gstrat = copy.deepcopy(G)
    Greg = copy.deepcopy(G)

    for edge in G.edges:
        # Remove scrambled dependencies
        if G.edges[edge]['dependency'] == '-1':
            Gstrat.remove_edge(edge[0],edge[1])
            Greg.remove_edge(edge[0],edge[1])
        # Remove strategic dependencies
        elif G.edges[edge]['dependency'] == '1':
            Gscram.remove_edge(edge[0],edge[1])
            Greg.remove_edge(edge[0],edge[1])
    return [Gscram, Greg, Gstrat]

def remove_allocation(G):
    '''Remove work allocation from network.'''
    G_copy = copy.deepcopy(G)
    # for G in glist_copy:
    #     for node in G.nodes:
    #         G.nodes[node]['agent']=None
    for node in G_copy.nodes:
        if G.nodes[node]['type'] == 'Action':
            G_copy.nodes[node]['agent'] = 'Unassigned'
        else:
            G_copy.nodes[node]['agent'] = None
    return G_copy
