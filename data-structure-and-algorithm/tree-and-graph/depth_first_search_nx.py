'''
this dfs() function works with networkx module, it receives a graph object with networkx type, 
along with the start vertex and the target vertex which default equal to None. 
it returns a list of vertices represents the path from the start to the target vertex and the
parents dict if the target vertex is not None and the target is found in the graph, otherwise
returns an empty list with the parents dict.
'''

def dfs(graph, start, target=None):
    stack = [start]
    parents = {start:start}
    path = list()
    found = False
    while stack:
        vertex = stack.pop(-1)
        print ('Processing %s' % vertex)
        if vertex == target:
            print(f'reaching the goal: {vertex}')
            found = True
            break
        
        # if all the neighbors are in the visited, the sbustract is an empty set(), 
        # that means the node is circling back to the visited graph or a dead-end node, 
        # there is nothing to be added into either the stack or the parents.
        exits = set(graph.neighbors(vertex)) - set(parents.keys())
        if not exits:
            print(f'found no exits from node {vertex}, retracing to node {parents[vertex]}')
            continue
        else:
            print(f'adding {exits} to stack and parents')
        for exit  in exits:
            stack.append(exit)
            parents[exit] = vertex
            
    
    if target and found:
        path += [target]
        parent = target
        while parent != start:
            parent = parents[parent] 
            path += [parent] 
        return path[::-1], parents
    else :
        return [], parents