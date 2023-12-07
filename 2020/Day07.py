import re
import networkx as nx
from collections import defaultdict
dfs_edges = nx.dfs_edges

G = nx.DiGraph()

first_bag  = re.compile('(\w+) (\w+) bags contain')
other_bags = re.compile('(\d+?) (\w+?) (\w+?) bag[s]*')

with open("Day07_test.txt") as f:
    for line in f.readlines():
        fb = first_bag.match(line.rstrip())
        intensity = fb.group(1)
        colour    = fb.group(2)

        G.add_node((intensity, colour))
        
        remains = re.sub(r'^.*?contains ', '', line.rstrip())
        match = other_bags.findall(remains)
        for m in match:
            _n, _i, _c = m
            G.add_edge((intensity, colour), (_i, _c), weight=int(_n))
            
tops = {}

def part1(node, tops):
    preds = [pred for pred in G.predecessors(node)]
    if preds:
        for p in preds:
            tops[p] = 1
            part1(p, tops)

part1(("shiny","gold"), tops)
print (len(tops.keys()))
    
def dfs_successors(G, source=None, depth_limit=None):
    """Return dictionary of successors in depth-first-search from source.

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
       Specify starting node for depth-first search and return edges in
       the component reachable from source.

    depth_limit : int, optional (default=len(G))
       Specify the maximum search depth.

    Returns
    -------
    succ: dict
       A dictionary with nodes as keys and list of successor nodes as values.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.dfs_successors(G, source=0)
    {0: [1], 1: [2], 2: [3], 3: [4]}
    >>> nx.dfs_successors(G, source=0, depth_limit=2)
    {0: [1], 1: [2]}

    Notes
    -----
    If a source is not specified then a source is chosen arbitrarily and
    repeatedly until all components in the graph are searched.

    The implementation of this function is adapted from David Eppstein's
    depth-first search function in `PADS`_, with modifications
    to allow depth limits based on the Wikipedia article
    "`Depth-limited search`_".

    .. _PADS: http://www.ics.uci.edu/~eppstein/PADS
    .. _Depth-limited search: https://en.wikipedia.org/wiki/Depth-limited_search
    """
    d = defaultdict(list)
    for s, t in dfs_edges(G, source=source, depth_limit=depth_limit):
        d[s].append(t)
    return dict(d)

print (nx.nodes(nx.dfs_tree(G, ("shiny","gold"))))


def part2(parent, node, tops):
    succs = [succ for succ in G.successors(node)]
    # No successors
    if succs == []:
        # What's the multiplier for this edge?
        weight = 
    if succs:
        for s in succs:
            tops[p] = 1
            part1(p, tops)
