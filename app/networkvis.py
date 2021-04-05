import plotly.graph_objects as go
import networkx as nx
import sorting as sort
import utility as ut
import forceSort as fs
import csv
import math
pi = math.pi

### Functions for changing the positions of nodes based on a corresponding Tree ###

node_agents = {}
agent_list = []
with open('data/KatieResearch/HFES/case_study/actionNodes.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
    for row in reader:
        if row[0] == 'actionName':
            continue
        if len(row) == 1 or row[1] == '':
            node_agents[row[0]] = 'Unassigned'
            if 'Unassigned' not in agent_list:
                agent_list.append('Unassigned')
        else:
            node_agents[row[0]] = row[1]
            if row[1] not in agent_list:
                agent_list.append(row[1])

if 'Unassigned' not in agent_list:
    agent_list.append('Unassigned')
agent_list.append(None)

# Blue, Red, Cyan, Green, Orange, Purple, Yellow, Magenta, Pink, Gray
color_list = ['#0000FF','#FF0000',  '#00FFFF', '#00FF00', '#FF8000', '#7F00FF', '#FFFF00', '#FF00FF', '#FF3399', '#A0A0A0']
color_lst2 = [['#FF6666', '#FF9999'], ['#6666FF', '#9999FF'], ['#66FF66', '#99FF99'], ['#FF9933', '#FFB266'], ['#B266FF', '#CC99FF'], ['#FFFF66', '#FFFF99'], ['#FF66FF', '#FF99FF'], ['#66FFFF', '#99FFFF'], ['#FF66B2', '#FF99CC'], ['#C0C0C0', '#E0E0E0']]
node_colors, i = {None: '#000000'}, 0
for agent in agent_list:
    if agent != None:
        node_colors[agent] = color_list[i]
        i += 1

act_dict = {}
for agent in agent_list:
    if agent != None:
        act_name = agent
        act_dict[agent] = {'shown': 'False', 'name': act_name}

#nodelegend={'Action': {'Humanoid': {'shown': False, 'name': 'Action - Humanoid'}, 'Astronaut': {'shown': False, 'name': 'Action - Astronaut'}, 'Unassigned': {'shown': False, 'name': 'Action - Unassigned'}},
#                'Resource': {None: {'shown': False, 'name': 'Resource'}},
#                'TeamworkCommand': {'Astronaut': {'shown': False, 'name': 'Command'}, None: {'shown': False, 'name': 'Command'}},
#                'TeamworkConfirm': {'Astronaut': {'shown': False, 'name': 'Confirm'}, None: {'shown': False, 'name': 'Confirm'}}}

nodelegend = {'Action': act_dict,
              'Resource': {None: {'shown': False, 'name': 'Resource'}},
              'TeamworkCommand': {'Astronaut': {'shown': False, 'name': 'Command'}, None: {'shown': False, 'name': 'Command'}},
              'TeamworkConfirm': {'Astronaut': {'shown': False, 'name': 'Confirm'}, None: {'shown': False, 'name': 'Confirm'}}}

node_shapes = {'Action': "circle", 'Resource': "square", 'TeamworkCommand': "triangle-up", 'TeamworkConfirm': 'diamond-tall'}

# Edge options for color and dash type
edge_color = {'0': '#000000', '1': '#0000FF', '-1': '#FF0000'}
edge_dash = {'0': 'solid', '1': 'dash', '-1': 'dash'}
edge_highlight = "#78fd9c"

def change_positions(t, positions, range_x, range_y, step_x):
    '''Changes the positions of all nodes in the tree t such that they will be displayed in a left-to-right tree format
       wherein each branch will be equally spaced from its parent node regardless of how long the branch is.'''
    pos_x = range_x[0]
    pos_y = (range_y[0] + range_y[1]) / 2
    positions[t.label] = [pos_x, pos_y]

    height = len(t.branches)
    # height = 1
    if height != 0:
        step_y = (range_y[1] - range_y[0]) / height
    steps_down = 0
    for branch in t.branches:
        change_positions(branch, positions, [range_x[0] + step_x, range_x[1] + step_x], [range_y[1] - (steps_down + 1) * step_y, range_y[1] - steps_down * step_y], step_x)
        steps_down += 1

    return None

def change_positions_lst(tree_lst, positions, range_x, range_y):
    '''Changes the positions for all nodes in the list of trees 'tree_lst' such that will be displayed in the given window formed by 'range_x' and 'range_y'.'''
    height = len(tree_lst)
    step_y = (range_y[1] - range_y[0]) / height

    i = 0
    for tree in tree_lst:
        step_x = (range_x[1] - range_x[0]) / tr.tree_depth(tree)
        change_positions(tree, positions, [range_x[0], range_x[0] + step_x], [range_y[1] - (i + 1) * step_y, range_y[1] - i  * step_y], step_x)
        i += 1

    return None

def new_change_pos(tree_lst, positions, range_x, range_y):
    '''Changes the positions of all nodes in a list of trees such that at each depth, all the nodes are equally spaced regardless of which tree they are in.'''
    def lst_change(tree_lst):
        '''Helper Function that creates a list of lists where each sub-list contains all nodes at any one depth.'''
        lst, branch_lst, temp_lst = [], [], []
        if len(tree_lst) == 0:
            return []
        for tree in tree_lst:
            temp_lst.append(tree.label)
            for branch in tree.branches:
                branch_lst.append(branch)

        lst.append(temp_lst)
        lst.extend(lst_change(branch_lst))
        return lst

    lst = lst_change(tree_lst)
    step_x = (range_x[1]  -range_x[0]) / len(lst)
    x_pos = (2 * range_x[0] + step_x) / 2
    for sec in lst:
        step_y = (range_y[1] - range_y[0]) / len(sec)
        y_pos = (2 * range_y[1] - step_y) / 2
        for node in sec:
            positions[node] = [x_pos, y_pos]
            y_pos -= step_y
        x_pos += step_x

    return None

def int_lst(num):
    '''Returns a list of all the integers, starting at 0, going up to num-1.'''
    lst = []
    for i in range(num):
        lst.append(i)
    return lst

def let_lst(num):
    '''Returns a list of letter identifiers, a, b, c, ... z; aa, ab, ac, ... az; ba, bb, bc, ... bz; ... za, zb, zc, ... zz.'''
    lst = []
    x, i, j = 0, 97, 97
    while x < num:
        if x < 26:
            lst.append(chr(i))
            i += 1
        else:
            lst.append(chr(i) + chr(j))
            j += 1

        if i > 122:
            i -= 26
        if j > 122:
            j -= 26
            i += 1

        x += 1
    return lst

def unline_positions(positions):
    '''Moves the positions of nodes slightly up and down such that there will be no edges exactly overlapping.'''
    node_lst = []
    grouped_lst = []

    for node in positions.keys():
        node_lst.append(node)

    while len(node_lst) > 0:
        temp_lst = [node_lst[0]]
        y = positions[node_lst[0]][1]
        node_lst.remove(node_lst[0])
        lst = int_lst(len(node_lst))
        lst = lst[::-1]
        for i in lst:
            if abs(positions[node_lst[i]][1] - y) < 0.01:
                temp_lst.append(node_lst[i])
                node_lst.remove(node_lst[i])
        grouped_lst.append(temp_lst)

    for group in grouped_lst:
        if len(group) > 1:
            j = 1 - len(group)
            for node in group:
                positions[node][1] += j * .1
                j += 2

    return positions

### Grouping functions ###

def group_pos_lists(node_lst, positions):
    '''Returns an x-list and y-list of positions for each of the nodes in 'node_lst' with positions specified in the dictionary positions.
       Also returns the mid-point coordinates as a separate list.'''
    left, top  = positions[node_lst[0]]
    right, bottom = positions[node_lst[0]]
    x_lst, y_lst = [], []

    for node in node_lst:
        x, y = positions[node]
        if x < left:
            left = x
        elif x > right:
            right = x
            
        if y > top:
            top = y
        elif y < bottom:
            bottom = y

        x_lst.append(x)
        y_lst.append(y)

    return x_lst, y_lst, [(left + right) / 2, (top + bottom) / 2]

def grouping_shape_positions(x_lst, y_lst, mid_x, mid_y, length):
    '''Returns a new x-list and y-list of positions that are one 'length' outwards from the midpoint.'''
    new_x_lst, new_y_lst = [], []
    for i in range(len(x_lst)):
        x, y = x_lst[i], y_lst[i]
        theta = ut.find_theta(mid_x, x, mid_y, y)

        new_x, new_y = x + length * math.cos(theta), y + length * math.sin(theta)
        new_x_lst.append(new_x)
        new_y_lst.append(new_y)

    return new_x_lst, new_y_lst

def order_of_points(x_lst, y_lst, mid_x, mid_y):
    '''Lists the x and y points in order moving around in a circle from the midpoint.'''
    theta_lst = []
    for i in range(len(x_lst)):
        x, y = x_lst[i], y_lst[i]
        theta = ut.find_theta(mid_x, x, mid_y, y)
        theta_lst.append([theta, i])

    theta_lst = ut.quick_sort(theta_lst)
    new_x_lst, new_y_lst = [], []

    for element in theta_lst:
        new_x_lst.append(x_lst[element[1]])
        new_y_lst.append(y_lst[element[1]])

    return new_x_lst, new_y_lst

def add_groups(groups, positions):
    '''Returns a text trace and a shapes trace where the text is the names of certain groups positioned at the center of the shapes that outline the respective groups.'''
    text_trace, shape_traces, color_lst = [], [], []
    text_lst, text_x, text_y = [], [], []
    for group in groups:
        node_cluster = groups[group]['tasks']
        if len(node_cluster) > 0:
            x_lst, y_lst, midpoint = group_pos_lists(node_cluster, positions)  # Get positions list for a group
            x_lst, y_lst = grouping_shape_positions(x_lst, y_lst, midpoint[0], midpoint[1], .1)  # Move positions outward
            x_lst, y_lst = order_of_points(x_lst, y_lst, midpoint[0], midpoint[1])  # Orders the positions around

            # Creates interpretable string that represents the path in plotly
            path = " M " + str(x_lst[0]) + "," + str(y_lst[0]) + " "
            for i in range(1,len(x_lst)):
                path = path + "L" + str(x_lst[i]) + "," + str(y_lst[i]) + " "
            path = path + "Z"

            # Add dictionary representing this group to shape_traces and add text characteristics to their respective lists
            shape_traces.append(dict(type = "path", path = path, line_color = groups[group]['colors'][0], fillcolor = groups[group]['colors'][1], opacity = .2))
            color_lst.append(groups[group]['colors'][0])
            text_lst.append(str(group))
            text_x.append(midpoint[0])
            text_y.append(midpoint[1])
    text_trace = go.Scatter(x = text_x, y = text_y, text = text_lst, mode = "text", hoverinfo = 'none', showlegend = False, name = str(group), textfont = dict(family = "sans serif", size = 14, color = color_lst))

    return text_trace, shape_traces

def draw_groups(fig, groups, positions):
    '''Draws groups based on the nodes defined in the dictionary 'groups'.'''
    text_trace, shape_traces = add_groups(groups, positions)  # Create text and shape traces for groups using given functions above
    fig.update_layout(shapes = shape_traces)  # Add in the shape traces outlining each region
    fig.add_trace(text_trace)  # Add in traces with text for the different groups

def add_arrow(x0, y0, x1, y1, color, width):
    # Adds two lines making an arrow at the midpoint of the edge
	# The math here is tricky but similar to the multiple edge plotting algorithm, LOTS OF TRIGONOMETRY
	arrow_length = .03
	arrow_angle = pi / 6
	if x1 != x0:
		edge_angle = math.atan((y1 - y0) / (x1 - x0))
	else:
		if y1 > y0:
			edge_angle = pi/2
		else:
			edge_angle = -1 * pi/2

	midpoint_x = x0 + (x1 - x0) / 2
	midpoint_y = y0 + (y1 - y0) / 2
	sign = 1
	if x0 <= x1:
		sign = -1  # ensures the arrow is pointing the proper way

	# Calculates changes in x and y and adds them to the midpoint coordinates to draw one-half of the arrow
	dx1 = arrow_length  *math.cos(edge_angle + arrow_angle)
	dy1 = arrow_length * math.sin(edge_angle + arrow_angle)
	edge_x1 = [midpoint_x, midpoint_x + dx1 * sign, None]
	edge_y1 = [midpoint_y, midpoint_y + dy1 * sign, None]
	trace1 = go.Scatter(x = edge_x1, y = edge_y1, hoverinfo = 'skip', line = dict(width = width, color = color),  mode = 'lines', showlegend = False)

	# Calculates changes in x and y and adds them to the midpoint coordinates to draw the other half of the arrow
	dx2 = arrow_length * math.cos(edge_angle - arrow_angle)
	dy2 = arrow_length * math.sin(edge_angle - arrow_angle)
	edge_x2 = [midpoint_x, midpoint_x + dx2 * sign, None]
	edge_y2 = [midpoint_y, midpoint_y + dy2 * sign, None]
	trace2 = go.Scatter(x = edge_x2, y = edge_y2, hoverinfo = 'skip', line = dict(width = width, color = color), mode = 'lines', showlegend = False)

	return trace1, trace2

### Trace making functions ###

def make_edge_trace(G, positions, controlmode):
    '''Creates and returns a list of traces that cover all the edges in the graph 'G' based on the positions of nodes given in 'positions'
       Also includes traces 'half1' and 'half2' which form arrows to indicate direction of edges.'''
    prev_edges = []

    # Create trace
    trace = []
    # Dictionary for tracking if legend is shown and name for each edge type
    edgelegend = {'-1': {'shown': False, 'name': 'Soft interdependency (scrambled)'},
                  '0': {'shown': False, 'name': 'Hard interdependency'},
                  '1': {'shown': False, 'name': 'Soft interdependency (strategic)'}}

    edgelist = []
    for edge in G.edges:
        edgelist.append(edge[0:2])

    for edge in G.edges:
        u = edge[0]
        w = edge[1]
        x0, y0 = positions[u]
        x1, y1 = positions[w]

        dep = G.edges[edge]['dependency']
        
        # Don't add edges for other control modes
        if dep != '0' and dep != controlmode:
            continue

        name = edgelegend[dep]['name']
        width = 1.5

        # Only show one legend entry for each edge type
        if not edgelegend[dep]['shown']:
            edgelegend[dep]['shown'] = True
            showleg = True
        else:
            showleg = False
        
        # Complex algorithm for plotting multiple edges between the same 2 nodes
        # Maximum of 3 identical edges connecting the same 2 nodes plotted
        repeat = ut.num_repeats(u, w, edgelist)
        if repeat > 1:
            if repeat > 3:
                repeat = 3
            units = 1 - repeat
            curr = ut.num_repeats(u, w, prev_edges)
            if curr > 2:
                curr = 2
            units += 2 * curr
            theta = ut.find_theta(y0, y1, x1, x0)
            delta_x, delta_y = units * math.cos(theta) / 125, units * math.sin(theta) / 125
            x0, x1 = x0 + delta_x, x1 + delta_x
            y0, y1 = y0 + delta_y, y1 + delta_y

            prev_edges.append([u, w])

        # Highlight edges that have teamwork interactions
        # IF source node is resource
        if G.nodes[u]['type'] == 'Resource':
            for n in G.predecessors(u):
                if G.nodes[n]['agent'] != None and G.nodes[n]['agent'] != G.nodes[w]['agent']:
                    t1 = go.Scatter(x = [x0, x1, None], y = [y0, y1, None], hoverinfo = 'skip', line = dict(color = edge_highlight, dash = 'solid', width = 4.5), showlegend = False)
                    trace.append(t1)

        # If source node is action
        else:
            # action to action
            if G.nodes[u]['agent'] != None and  G.nodes[w]['agent'] != None:
                if (G.nodes[u]['agent'] != G.nodes[w]['agent']):
                    t1 = go.Scatter(x = [x0, x1, None], y = [y0, y1, None], hoverinfo = 'skip', line = dict(color = edge_highlight, dash = 'solid', width = 4.5), showlegend = False)
                    trace.append(t1)
            # action to resource
            else:
                for n in G.successors(w):
                    if G.nodes[u]['agent'] !=None and G.nodes[n]['agent'] != None and G.nodes[u]['agent'] != G.nodes[n]['agent']:
                       t1 = go.Scatter(x = [x0, x1, None], y = [y0, y1, None], hoverinfo = 'skip', line = dict(color = edge_highlight, dash = 'solid', width = 4.5), showlegend = False)
                       trace.append(t1) 


        t = go.Scatter(x = [x0,x1,None], y = [y0, y1, None], hoverinfo = 'skip', line = dict(color = edge_color[dep], dash = edge_dash[dep], width = width), showlegend = showleg, name = name, legendgroup = 'group0')
        half1, half2 = add_arrow(x0, y0, x1, y1, edge_color[dep], width)
        trace.extend([t, half1, half2])
       
    return trace

def make_node_trace(G, positions, textorhover):
    '''Creates and returns a list of traces for all of the nodes in 'G' based on their positions in 'positions'. It colors and shapes the nodes based on their corresponding agent in 'node_colors' and 'node_shapes'.
       Also accounts for each type of node only once in the legend. It labels the nodes either as full text above each one or by hovering over them based on the variable 'textorhover' being set to 'text' or 'hover'.'''
    typ = True
    if textorhover == 'hover':
        typ = False

    # Ceate trace
    trace = []
    shown = []
    # Dictionary for tracing if legend is shown and name for each node type
    for node in G.nodes():
        x,y = positions[node]
        agent = G.nodes[node]['agent']
        nodetype = G.nodes[node]['type']
        name = nodelegend[nodetype][agent]['name']


        if nodelegend[nodetype][agent] not in shown:
            shown.append(nodelegend[nodetype][agent])
            showleg = True
        else:
            showleg = False

        if typ: 
            t = go.Scatter(
                x = tuple([x]),
                y = tuple([y]),
                hoverinfo = 'none',
                text = str(node),
                marker = dict(color = node_colors[G.nodes[node]['agent']],
                            symbol = node_shapes[G.nodes[node]['type']],
                            size = 10,
                            line_width = 2),
                mode = 'markers+text',
                textposition = 'top center',
                name = name,
                showlegend = showleg,
                legendgroup = 'group1'
            )
        else:
            t = go.Scatter(
                x = tuple([x]),
                y = tuple([y]),
                hoverinfo = 'text',
                text = str(node),
                marker = dict(color = node_colors[G.nodes[node]['agent']],
                            symbol = node_shapes[G.nodes[node]['type']],
                            size = 10,
                            line_width = 2),
                mode = 'markers',
                name = name,
                showlegend = showleg,
                legendgroup = 'group1'
            )
        trace.append(t)
    return trace
 
def make_node_trace_legend(G, positions):
    '''Creates and returns a list of traces for each node in 'G' such that a number will appear over each node and then that number will appear in the legend referring to the full name of the node.'''
    numbers, i = int_lst(len(G.nodes())), 0
    letters, j = let_lst(len(G.nodes())), 0
    ag_id = let_lst(len(agent_list))
    gr_id = {}
    for k in range(len(ag_id)):
        gr_id[agent_list[k]] = ag_id[k]

    # Create the trace
    trace = []

    for node in G.nodes():
        x,y = positions[node]
        agent = G.nodes[node]['agent']
        nodetype = G.nodes[node]['type']
        
        if nodetype == 'Action':
            t = go.Scatter(
                x = tuple([x]),
                y = tuple([y]),
                hoverinfo = 'none',
                text = str(numbers[i]),
                marker = dict(color = node_colors[G.nodes[node]['agent']],
                            symbol = node_shapes[G.nodes[node]['type']],
                            size = 10,
                            line_width = 2),
                mode = 'markers+text',
                textposition = 'top center',
                name = str(numbers[i]) + ': ' + str(node),
                showlegend = True,
                legendgroup = gr_id[agent]
            )
            i += 1
        else:
            t = go.Scatter(
                x = tuple([x]),
                y = tuple([y]),
                hoverinfo = 'none',
                text = str(letters[j]),
                marker = dict(color = node_colors[G.nodes[node]['agent']],
                            symbol = node_shapes[G.nodes[node]['type']],
                            size = 10,
                            line_width = 2),
                mode = 'markers+text',
                textposition = 'top center',
                name = str(letters[j]) + ': ' + str(node),
                showlegend = True,
                legendgroup = gr_id[agent]
            )
            j += 1

        trace.append(t)
    return trace

### Main function creating and visualizing the Network as a Figure ###

def visualize_network(G, ctrlmode, layoutstyle, node_agents):
    '''Creates a figure representing the graph 'G' with the specified layout style and control mode.'''
    positions = nx.circular_layout(G) # set positions of nodes to a basic circular layout for further modification

    # Generate a list of all the edges in the graph that is easy to handle later on
    edgelist = []
    for edge in G.edges:
        edgelist.append(edge[0:2])
        
    # Reposition nodes based on sorting algorithm specified in layoutstyle
    # and change the positions dictionary to reflect these changes
    if layoutstyle == 'topo':
        tree_lst = sort.topological_sort(edgelist, list(G.nodes))
        new_change_pos(tree_lst, positions, [-1, 1], [-1, 1])
        positions = unline_positions(positions)
    elif layoutstyle == 'clustered':
        tree_lst = sort.new_ag_sort(edgelist, list(G.nodes), node_agents)
        new_change_pos(tree_lst, positions, [-1, 1], [-1, 1])
        positions = unline_positions(positions)
    elif layoutstyle == 'force':
        edgelist2, nodelist2 = [], []
        for i in list(G):
            nodelist2.append([i, 1, 1])
        for edge in G.edges:
            edgelist2.append([edge[0], edge[1], 1])

        positions = fs.force_directed_sort(edgelist2, nodelist2, positions)

    # Create a figure with our new positional layout
    fig = visualize_network_positions(G, ctrlmode, layoutstyle, node_agents, positions)

    return fig, positions

def visualize_network_positions(G, ctrlmode, layoutstyle, node_agents, positions):
    '''Creates a figure representing the graph 'G' given predetermined positions.'''
    textorhover = 'hover'
    # Create the layout for the figure with specified styling
    layout = go.Layout(
        paper_bgcolor = 'rgba(0,0,0,0)',  # transparent background
        plot_bgcolor = 'rgba(0,0,0,0)',  # transparent 2nd background
        title = '<br>Network Graph',
        titlefont_size = 16,
        showlegend = True,
        legend_title_text = 'Edge and Node Types',
        hovermode='closest',
        xaxis =  {'showgrid': False, 'showticklabels': False, 'zeroline': False},  # no gridlines
        yaxis = {'showgrid': False, 'showticklabels': False, 'zeroline': False},  # no gridlines
        font = dict(size = 18) # making font bigger
    )
        
    fig = go.Figure(layout = layout)

    # Draw groups if we are in the Agent-Clustering layout
    if layoutstyle == 'clustered':
        # Create the list to hold the clusters for each agent
        cluster = []
        for agent in agent_list:
            cluster.append([])

        # Place all the nodes in their proper cluster matching their assigned agent
        for node in G.nodes:
            Found, index = False, 0
            for agent in agent_list:
                if not Found and G.nodes[node]['agent'] == agent:
                    cluster[index].append(node)
                    Found = True
                index += 1

        # Previous hard coded agents and their clusters/groups
        #            if G.nodes[node]['agent']=='Astronaut':
		#                cluster1.append(node)
		#            elif G.nodes[node]['agent']=='Humanoid':
		#                cluster2.append(node)
		#            elif G.nodes[node]['agent']=='Unassigned':
		#                cluster3.append(node)
		#            else:
		#                cluster4.append(node)

		# groups = {'Astronaut': {'tasks': cluster1, 'colors':['#FF33FF', '#FF99FF']},'Humanoid': {'tasks': cluster2, 'colors': ['#CCCC00', '#FFFF00']}, 'Unassigned': {'tasks': cluster3, 'colors': ['#33FFFF', '#99FFFF']}, None: {'tasks': cluster4, 'colors': ['#B2B2B2', '#E3E3E3']}} 

		# Generating the Dictionary of groups where we now have each group assigned a unique color representing the unique agent
        groups = {}
        i = 0
        for agent in agent_list:
            if agent != None:
                groups[agent] = {'tasks': cluster[i], 'colors': color_lst2[i]}
                i += 1

        draw_groups(fig, groups, positions)

    # Create all of the edge and node traces and add them to the figure
    edge_trace = make_edge_trace(G, positions, ctrlmode)
    node_trace = make_node_trace(G, positions, textorhover)
    node_trace_legend = make_node_trace_legend(G, positions)
    
### Note that you must make 2 kinds of node traces to have the legend show what type of nodes exist and have a key for which number corresponds to the name of which node
### The 'textorhover' attribute in make_node_trace should be set to 'hover' if you want this to happen correctly, otherwise there will be both a number and a full name as text above each node.
### However, you won't be able to hover for the name because it will plot the second trace of every node over top of the first trace, therefore covering up the hover point.

    fig.add_traces(edge_trace)
    fig.add_traces(node_trace)
    fig.add_traces(node_trace_legend)

    return fig
