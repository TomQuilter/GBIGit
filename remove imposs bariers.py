def create_graph(combination, grid_size=4):
    """ Create a graph representation of the grid.  = 3 is a 3 by 3 , 0, 1, 2 """
    graph = {}
    for x in range(grid_size):
        for y in range(grid_size):
            if (x, y) not in combination:
                graph[(x, y)] = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in combination:
                            graph[(x, y)].append((nx, ny))
    return graph
 
def can_reach_target(graph, start, target):
    """ Check if the target is reachable from start using DFS. """
    visited = set()
    stack = [start]
 
    while stack:
        node = stack.pop()
        if node == target:
            return True
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])
 
    return False

def split_into_pairs(lst):
    new_list = []
    for item in lst:
        # Split each tuple into pairs and add them to the new list
        new_list.append([item[i:i+2] for i in range(0, len(item), 2)])
    return new_list

def flatten_pairs(lst):
    new_list = []
    for sublist in lst:
        # Flatten each sublist of tuples into a single tuple
        flattened_tuple = tuple(item for pair in sublist for item in pair)
        new_list.append(flattened_tuple)
    return new_list

# Example input
#sorted_combinations = [
#    [(0, 1), (0, 2)], 
#    [(0, 1), (1, 0)],
#    [(0, 1), (1, 1)],
#    [(0, 1), (1, 1), (2, 1)],
#    [(0, 1), (1, 1), (2, 1), (3, 2)],
#    [(0, 1), (1, 1), (1, 2), (2, 2), (3, 2)],
#    [(0, 1), (1, 1), (1, 2), (2, 1), (1, 3)],  #removed
#    [(0, 1), (1, 1), (2, 1), (1, 3)]
#]

sorted_combinations = [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (0, 1, 0, 2), (0, 1, 1, 0), (0, 1, 1, 1), (0, 1, 1, 2), (0, 1, 2, 0), (0, 1, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), (0, 2, 1, 1), (0, 2, 1, 2), (0, 2, 2, 0), (0, 2, 2, 1), (0, 2, 2, 2), (1, 0, 1, 1), (1, 0, 1, 2), (1, 0, 2, 0), (1, 0, 2, 1), (1, 0, 2, 2), (1, 1, 1, 2), (1, 1, 2, 0), (1, 1, 2, 1), (1, 1, 2, 2), (1, 2, 2, 0), (1, 2, 2, 1), (1, 2, 2, 2), (2, 0, 2, 1), (2, 0, 2, 2), (0, 1), (1, 1), (1, 2), (2, 1), (1, 3)]
print(sorted_combinations)
sorted_combinations = split_into_pairs(sorted_combinations)

print(sorted_combinations)
print(len(sorted_combinations))  
# Remove combinations that block the path from (0,0) to (0,3)
sorted_combinations = [combo for combo in sorted_combinations 
                       if can_reach_target(create_graph(combo), (0, 0), (0, 3))]

sorted_combinations = flatten_pairs(sorted_combinations)

print(sorted_combinations)
print(len(sorted_combinations)) 

