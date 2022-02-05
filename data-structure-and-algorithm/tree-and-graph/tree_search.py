from graph_samples import graph

def dfs(graph, start, target=None):
    stack = [start]
    parents = {start: start}
    path = list()
    while stack:
        print ('Stack is: %s' % stack)
        vertex = stack.pop(-1)
        print ('Processing %s' % vertex)
        for candidate in graph[vertex]:
            if candidate not in parents:
                parents[candidate] = vertex
                stack.append(candidate)
                print ('Adding %s to the stack' % candidate) 
        path.append(parents[vertex]+'->'+vertex)
        if vertex == target:
            return target, path[1:]
    return None, path[1:]

def dfs_2(graph, start, target=None):
    stack = [start]
    visited = [start]
    path = list()
    while stack:
        print ('Stack is: %s' % stack)
        vertex = stack.pop(-1)
        visited += [vertex]
        print ('Processing %s' % vertex)
        for candidate in graph[vertex]:
            if candidate not in visited:
                stack.append(candidate)
                print ('Adding %s to the stack' % candidate) 
        path.append(vertex +'->' )
        if vertex == target:
            return target, ''.join(path).rstrip('->')
    return None, ''.join(path).rstrip('->')

def bfs(graph, start, target):
    queue = [start]
    processed = [start]
    path = []
    while queue:
        print(f'queue: {queue}\nprocessed: {processed}')
        vertex = queue.pop(0)
        for candidate in graph[vertex] :
            if candidate not in processed :
                queue.append(candidate)
                processed.append(candidate)
                path.append(vertex + '->' + candidate)
                if candidate == target :
                    return target, path     
    return None, path




def test():
    print(dfs(graph, 'A', 'F'))

    print(dfs_2(graph, 'A', 'F'))

    print(bfs(graph, 'A', 'G'))

if __name__ == '__main__':
    test()
