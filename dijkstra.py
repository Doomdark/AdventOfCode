from collections import defaultdict
import heapq as heap

# Construct a weighted graph of the adjacent nodes for a space
## G = {}
## for x in range(max_x):
##     for y in range(max_y):
##         for _x,_y in adjacents(x,y):
##             # If the adjacent node isn't a wall then we can visit it
##             if (_x,_y) not in walls:
##                 if (x,y) not in G:
##                     G[(x,y)] = {}
##                 G[(x,y)][(_x,_y)] = 1

def dijkstra(G, startingNode):
    visited = set()
    parentsMap = {}
    pq = []
    nodeCosts = defaultdict(lambda: float('inf'))
    nodeCosts[startingNode] = 0
    heap.heappush(pq, (0, startingNode))

    while pq:
        # go greedily by always extending the shorter cost nodes first
        _, node = heap.heappop(pq)
        visited.add(node)

        for adjNode, weight in G[node].items():
            if adjNode in visited:  continue

            newCost = nodeCosts[node] + weight
            if nodeCosts[adjNode] > newCost:
                parentsMap[adjNode] = node
                nodeCosts[adjNode] = newCost
                heap.heappush(pq, (newCost, adjNode))

    return parentsMap, nodeCosts
