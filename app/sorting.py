import trees as tr
from trees import Tree
import utility as ut

### 5 algorthms for sorting nodes in a Tree ###

def graph_first_sort(edges_lst):
    '''Creates and returns a list of trees that adds edges in order as long as one of their nodes isn't already in the graph.'''
    tree_lst = [Tree(edges_lst[0][0])]
    for edge in edges_lst:
        first, second = [], []
        for i in range(len(tree_lst)):
            if tr.has_node(tree_lst[i], edge[0]):
                first.append(i)
            if tr.has_node(tree_lst[i], edge[1]):
                second.append(i)

        go = True
        if len(first) == 0:
            if len(second) == 0:
                tree_lst.append(Tree(edge[0]))
                tree_lst[len(tree_lst) - 1].branches.append(Tree(edge[1]))
                go = False
            else:
                lowest = second[0]
        else:
            lowest = first[0]
            if len(second) != 0 and second[0] < first[0]:
                lowest = second[0]

        if go:
            if not tr.has_node(tree_lst[lowest], edge[0]):
                path = tr.tree_path(tree_lst[lowest], edge[1])
                temp_branch = tr.tree_branch(tree_lst[lowest], path)
                temp_branch.branches.append(Tree(edge[0])) # In the branch that contains edge[1], append edge[0]
            else:
                if not tr.has_node(tree_lst[lowest], edge[1]):
                    path = tr.tree_path(tree_lst[lowest], edge[0])
                    temp_branch = tr.tree_branch(tree_lst[lowest], path)
                    temp_branch.branches.append(Tree(edge[1]))

    return tree_lst

def depth_first_sort(edges_lst, nodes_lst):
    '''Creates and returns a Tree that stars with the first node, then adds all nodes connected to the parent node through any series of edges.
       If there are still nodes left, adds the first node not already in the graph and then recursively calls the algorithm on that node.'''
    tree_lst = [Tree(edges_lst[0][0])]
    nodes_lst.remove(edges_lst[0][0])
    tr.add_branches(tree_lst[0], nodes_lst, edges_lst)  # Adds all nodes that are connected to the parent node through any series of edges

    while len(nodes_lst) > 0:
        found = False
        for edge in edges_lst:
            if not found:
                if edge[0] in nodes_lst:
                    tree_lst.append(Tree(edge[0]))
                    nodes_lst.remove(edge[0])
                    found = True
                elif edge[1] in nodes_lst:
                    tree_lst.append(Tree(edge[1]))
                    nodes_lst.remove(edge[1])
                    found = True

        tr.add_branches(tree_lst[len(tree_lst)-1], nodes_lst, edges_lst)

    return tree_lst

def topological_sort(edges_lst, nodes_lst):
    '''Creates and returns a Tree that has all edges moving from left to right.'''
    tree_lst = []
    unchanged_edges = edges_lst[::]
    erred, erred_lst = False, []

    while len(nodes_lst) > 0:
        
        try:    
            temp_lst = nodes_lst[::]
            
            # Make temp_lst a list of nodes that have no edges going into them
            for edge in edges_lst:
                if edge[1] in temp_lst and edge[1] != edge[0]:
                    temp_lst.remove(edge[1])

            node = temp_lst[0]  # Selects the first node with no edges going into it
            nodes_lst.remove(node)
        
            # Removes all edges starting at node from edges list
            i = len(edges_lst) - 1
            while i >= 0:
                if edges_lst[i][0] == node:
                    edges_lst = edges_lst[:i] + edges_lst[i + 1:]
                i = i - 1

            # Creates a list of all other nodes that have an edge going in to the current node
            prev_nodes = []
            for edge in unchanged_edges:
                if edge[1] == node and edge[0] != node:
                    prev_nodes.append(edge[0])

            paths_lst = []
            if len(prev_nodes) == 0:
                tree_lst.append(Tree(node))
            else:
                for n in prev_nodes:
                    j = tr.lst_has_node(tree_lst, n)
                    d = tr.node_depth(tree_lst[j], n)
                    p = tr.tree_path(tree_lst[j], n)
                    paths_lst.append([d, j, p])
                paths_lst = ut.quick_sort(paths_lst)
                my_path = paths_lst[len(paths_lst) - 1]
                temp_branch = tr.tree_branch(tree_lst[my_path[1]], my_path[2])
                temp_branch.branches.append(Tree(node))
    
        except IndexError:
            if not erred:
                erred = True
                print("There are cycles in the given graph. Continuing with modified Topological Sort")
            erred_lst.append(nodes_lst[0])
            nodes_lst.remove(nodes_lst[0])

    # For all nodes that were a part of a cycle, add them back in after the first node they were connected to
    while len(erred_lst) > 0:
        node = erred_lst[0]
        found = False
        for edge in unchanged_edges:
            if not found and edge[1] == node:
                j = tr.lst_has_node(tree_lst, edge[0])
                if j != -1:
                    p = tr.tree_path(tree_lst[j], edge[0])
                    temp_branch = tr.tree_branch(tree_lst[j], p)
                    temp_branch.branches.append(Tree(node))
                else:
                    tree_lst.append(Tree(node))
                erred_lst.remove(node)
                found = True

    return tree_lst

def agent_clustering_sort(G):
    '''Sorts the nodes into trees based on which agent they correspond to.'''
    tree_lst = []
    agent_dict, i = {}, 0

    for edge in G.edges():
        # if G.nodes[edge[0]]['agent'] == None:
        #     num, other = 0, 1
        # else:
        #     num, other = 1, 0
        num, other = 1, 0
        ag = G.nodes[edge[0]]['agent']

        if ag not in agent_dict.keys():
            agent_dict[ag] = i
            i += 1
            if tr.lst_has_node(tree_lst, edge[other]) == -1:
                tree_lst.append(Tree(edge[num], [Tree(edge[other])]))
            else:
                tree_lst.append(Tree(edge[num]))
        else:
            j = tr.lst_has_node(tree_lst, edge[num])
            k = tr.lst_has_node(tree_lst, edge[other])
            if j == -1:
                if k == -1:
                    tree_lst[agent_dict[ag]].branches.append(Tree(edge[num], [Tree(edge[other])]))
                else:
                    if k == agent_dict[ag]:
                        path = tr.tree_path(tree_lst[k], edge[other])
                        temp_branch = tr.tree_branch(tree_lst[k], path)
                        temp_branch.branches.append(Tree(edge[num]))
                    else:
                        tree_lst[agent_dict[ag]].branches.append(Tree(edge[num]))
            else:
                if k == -1:
                    path = tr.tree_path(tree_lst[j], edge[num])
                    temp_branch = tr.tree_branch(tree_lst[j], path)
                    temp_branch.branches.append(Tree(edge[other]))

    return tree_lst

def new_ag_sort(edges_lst, nodes_lst, node_agents):
    '''Sorts the nodes into a list of trees based on which agent corresponds to which node. Will create a new tree for each type of agent except 'Resource'
       and will place resource nodes in the tree of the agent that is connected to that node first. This is a more comprehensive although less efficient algorithm
       than agent_clustering_sort, yet this one, new_ag_sort, is still the preferrable method if sorting by agent.'''
    tree_lst, new_nodes_lst = [], nodes_lst[:]

    agent_dict, i = {}, 0
    for edge in edges_lst:
        both = False
        if node_agents.get(edge[0], 'Resource') != 'Resource':
            num, other = 0, 1
        else:
            num, other = 1, 0

        if node_agents.get(edge[other], 'Resource') != 'Resource':
            both = True

        ag0 = node_agents.get(edge[num], 'Resource')
        ag1 = node_agents.get(edge[other],'Resource')

        if both:
            if ag0 not in agent_dict.keys():
                agent_dict[ag0] = i
                i += 1
                tree_lst.append(Tree(edge[num]))
                new_nodes_lst.remove(edge[num])
            elif tr.lst_has_node(tree_lst, edge[num]) == -1:
                nod = tr.last_node(tree_lst[agent_dict[ag0]])
                path = tr.tree_path(tree_lst[agent_dict[ag0]], nod)
                temp_branch = tr.tree_branch(tree_lst[agent_dict[ag0]], path)
                temp_branch.branches.append(Tree(edge[num]))
                new_nodes_lst.remove(edge[num])

            if ag1 not in agent_dict.keys():
                agent_dict[ag1] = i
                i += 1
                tree_lst.append(Tree(edge[other]))
                new_nodes_lst.remove(edge[other])
            elif tr.lst_has_node(tree_lst, edge[other]) == -1:
                nod = tr.last_node(tree_lst[agent_dict[ag1]])
                path = tr.tree_path(tree_lst[agent_dict[ag1]], nod)
                temp_branch = tr.tree_branch(tree_lst[agent_dict[ag1]], path)
                temp_branch.branches.append(Tree(edge[other]))
                new_nodes_lst.remove(edge[other])
        else:
            if ag0 not in agent_dict.keys():
                agent_dict[ag0] = i
                i += 1
                if tr.lst_has_node(tree_lst, edge[other]) == -1:
                    tree_lst.append(Tree(edge[0], [Tree(edge[1])]))
                    new_nodes_lst.remove(edge[0])
                    new_nodes_lst.remove(edge[1])
                else:
                    tree_lst.append(Tree(edge[num]))
                    new_nodes_lst.remove(edge[num])
            else:
                j = tr.lst_has_node(tree_lst, edge[num])
                k = tr.lst_has_node(tree_lst, edge[other])
                if j == -1:
                    if k == -1:
                        tree_lst[agent_dict[ag0]].branches.append(Tree(edge[0], [Tree(edge[1])]))
                        new_nodes_lst.remove(edge[0])
                        new_nodes_lst.remove(edge[1])
                    else:
                        if k == agent_dict[ag0]:
                            path = tr.tree_path(tree_lst[k], edge[other])
                            temp_branch = tr.tree_branch(tree_lst[k], path)
                            temp_branch.branches.append(Tree(edge[num]))
                        else:
                            tree_lst[agent_dict[ag0]].branches.append(Tree(edge[num]))
                        new_nodes_lst.remove(edge[num])
                else:
                    if k == -1:
                        path = tr.tree_path(tree_lst[j], edge[num])
                        temp_branch = tr.tree_branch(tree_lst[j], path)
                        temp_branch.branches.append(Tree(edge[other]))
                        new_nodes_lst.remove(edge[other])

    more = False
    if len(new_nodes_lst) > 0:
        more = True
        temp_tree = Tree(new_nodes_lst[0])
        temp_branch = temp_tree.branches
        new_nodes_lst = new_nodes_lst[1:]
    while len(new_nodes_lst) > 0:
        temp_branch.append(Tree(new_nodes_lst[0]))
        temp_branch = temp_branch[0].branches
        new_nodes_lst = new_nodes_lst[1:]
    if more:
        tree_lst.append(temp_tree)

    return tree_lst
