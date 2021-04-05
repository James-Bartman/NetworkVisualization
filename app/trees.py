import utility as ut

### Tree class and related functions ###

class Tree:
    '''A Class representing a Tree which is defined as a node and a list of branches, each of which is itself a Tree.'''
    def __init__(self, label, branches = []):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent = 0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()

def add_branches(t, nodes_lst, edges_lst):
    '''Adds all nodes that are connected to the parent node of the Tree 't' by an edge in 'edges_lst' as a branch in 't'.
       Then, does the same for all of those new branch nodes. Hence, it will end up adding all nodes that are connected to the parent node of 't' through any series of edges.'''
    if len(nodes_lst) > 0:
        for edge in edges_lst:
            if edge[0] == t.label and edge[1] in nodes_lst:
                t.branches.append(Tree(edge[1]))
                nodes_lst.remove(edge[1])
            elif edge[1] == t.label and edge[0] in nodes_lst:
                t.branches.append(Tree(edge[0]))
                nodes_lst.remove(edge[0])
        
        for branch in t.branches:
            add_branches(branch, nodes_lst, edges_lst)

    return t

def num_nodes(t):
    '''Returns the total number of nodes in a Tree.'''
    if t.is_leaf():
        return 1
    return 1 + sum([num_nodes(branch) for branch in t.branches])

def tree_depth(t):
    '''Returns the depth of the tree, aka the length of the longest branch.'''
    if t.is_leaf():
        return 1
    return 1 + max([tree_depth(branch) for branch in t.branches])

def has_node(t, node):
    '''Returns True if the tree has the given node, False otherwise.'''
    if t.label == node:
        return True
    elif t.is_leaf():
        return False
    for branch in t.branches:
        if has_node(branch, node):
            return True
    return False

def lst_has_node(tree_lst, node):
    '''Returns the index of the tree in tree_lst that has 'node' in it, returns -1 if no tree in tree_lst has the node.'''
    for i in range(len(tree_lst)):
        if has_node(tree_lst[i], node):
            return i
    return -1

def tree_path(t, node):
    '''Returns a list of the nodes in the tree that form the first path going from the parent to the node.'''
    assert has_node(t, node), 'Node must be in Tree'
    def tree_path_helper(t, node, path):
        found = False
        i = 0
        for branch in t.branches:
            if not found:
                if has_node(branch, node):
                    path.append(i)
                    found = True
                    if branch.label == node:
                        return path
                    return tree_path_helper(branch, node, path)
            i += 1
    if t.label == node:
        return []
    return tree_path_helper(t, node, [])

def tree_branch(t, path):
    '''Returns the tree with node specified in tree_path by following the path generated in tree_path.'''
    if path == []:
        return t
    return tree_branch(t.branches[path[0]], path[1:])

def node_depth(t, node):
    '''Returns the depth of 'node' in t.'''
    if t.label == node:
        return 1
    elif t.is_leaf():
        return 100000
    return 1 + min([node_depth(branch, node) for branch in t.branches])

def last_node(t):
    '''Returns the last node, aka the node at the gretest depth, of the Tree 't'.
       If more than one node is at the greatest depth, it returns the node furthest right, or closest to the end of the list,
       of all nodes at the greatest depth.'''
    if t.is_leaf():
        return t.label
    lst = []
    for i in range(len(t.branches)):
        lst.append([tree_depth(t.branches[i]), i])
    lst = ut.quick_sort(lst)
    return last_node(t.branches[lst[len(lst) - 1][1]])
