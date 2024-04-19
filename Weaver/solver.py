from search_tree import SearchTree
import argparse
from tqdm import tqdm

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def get_args():
    # Commandline Arguments
    parser = argparse.ArgumentParser(description='Terminal Arguments for solving Weaver')

    parser.add_argument('start', type=str, help='starting word')
    parser.add_argument('end', type=str, help='ending word')
    parser.add_argument('--verbose', action='store_true', default=False, help='if included, the terminal will print more info')
    parser.add_argument('--progress_bar', action='store_true', default=False, help='if included, the terminal will display a progress bar at each step')
    parser.add_argument('--debug', action='store_true', default=False, help='if included, the terminal will display the level at each step')

    args = parser.parse_args()
    return args

# it is assumed that word and next_word have the same length
# a valid next_word is a word that differs by exactly 1 letter
def valid_next_word(word, next_word):
    n = len(word)
    letters_in_common = sum([c1 == c2 for c1, c2 in zip(word, next_word)])
    return letters_in_common == n-1

def get_possible_next_words(word, dictionary):
    possible_next_words = []
    for next_word in dictionary:
        if valid_next_word(word, next_word):
            possible_next_words.append(next_word)
    return possible_next_words

def get_nodes_at_depth(node, depth):
    if depth == 0:
        return [node]
    
    if len(node.parents) == depth-1:
        return node.children

    nodes = []
    for child in node.children:
        nodes.extend( get_nodes_at_depth(child, depth) )
    
    return nodes  
        
def add_pruned_children(node, dictionary):
    possible_next_words = get_possible_next_words(node.value, dictionary)
    for next_word in possible_next_words:
        # This ensures we don't repeat unoptimal paths
        # This check is very important to keep things efficient
        if next_word in [p.value for p in node.parents]:
            continue
        
        child = SearchTree(next_word)
        node.add_child(child)

# This is just a breadth-first search, but it caps out at about a depth 5
def solver(dictionary, start_word, end_word, verbose=False, progress_bar=False, debug=False):
    
    root = SearchTree(start_word)
    #add_pruned_children(root, dictionary)
    
    depth = -1
    level = [root]
    level_values = [root.value]
    while True:
        depth += 1
        if verbose:
            print("BFS depth:", depth)
        level = get_nodes_at_depth(root, depth)
        level_values = [node.value for node in level]

        if level == []:
            if verbose:
                print("Dead end on BFS")
            return 0, []

        # if the end_word is in this level, then this is the optimal length
        if end_word in level_values:
            break

        # otherwise we continue to the next level
        node_iter = tqdm(level) if progress_bar else level
        for node in node_iter:
            add_pruned_children(node, dictionary)
    

    # now we just search the current level for the solutions
    solutions = []
    for node in level:
        if node.value == end_word:
            solution = [parent.value for parent in node.parents] + [end_word]
            solutions.append(solution)
    
    optimal_length = depth
    return optimal_length, solutions


# This is a bidirectional breadth-first search, so it should be more efficient
# It can get to a bidirectional depth of about 5 (depth 9-10 in total)
def solver_bidirectional(dictionary, start_word, end_word, verbose=False, progress_bar=False, debug=False):
    root1 = SearchTree(start_word)
    root2 = SearchTree(end_word)

    depth1 = -1
    level1 = []
    level1_values = set([])

    depth2 = -1
    level2 = []
    level2_values = set([])

    common_values = set([])
    while True:
       
        # To make things more efficent, if level1 is larger than level2, we skip doing level1
        if len(level1) <= len(level2):

            # root 1 steps
            depth1 += 1
            if verbose:
                print("top BFS depth:", depth1)

            level1 = get_nodes_at_depth(root1, depth1)
            if debug:
                print(level1)

            if level1 == []:
                if verbose:
                    print("Dead end on top BFS")
                return 0, []
            
            node_iter = tqdm(level1) if progress_bar else level1
            for node in node_iter:
                add_pruned_children(node, dictionary)
            
            # check for intersecting solutions
            level1_values = set([node.value for node in level1])
            common_values = level1_values.intersection(level2_values)
            if len(common_values) > 0:
                break

        # same on this end
        if len(level1) >= len(level2):

            # root 2 takes a step
            depth2 += 1
            if verbose:
                print("\t\t\tbottom BFS depth:", depth2)

            level2 = get_nodes_at_depth(root2, depth2)
            if debug:
                print(level2)

            if level2 == []:
                if verbose:
                    print("\t\t\tDead end on bottom BFS")
                return 0, []
            
            node_iter = tqdm(level2) if progress_bar else level2
            for node in node_iter:
                add_pruned_children(node, dictionary)
            
            # check for intersecting solutions
            level2_values = set([node.value for node in level2])
            common_values = level1_values.intersection(level2_values)
            if len(common_values) > 0:
                break
        

    # It's a little tricker to calculate all solutions with bidirectional BFS 
    solutions = []
    for value in common_values:
        root1_leafs = [node for node in level1 if node.value == value]
        root2_leafs = [node for node in level2 if node.value == value]

        # effectively I'm taking the cartesian product of all paths to the common node from both directions
        for leaf1 in root1_leafs:
            for leaf2 in root2_leafs:
                leaf1_trace = [node.value for node in leaf1.parents]
                leaf2_trace = [node.value for node in leaf2.parents]
                solution = leaf1_trace + [value] + list(reversed(leaf2_trace))
                solutions.append(solution)

    optimal_length = depth1 + depth2
    return optimal_length, solutions

def draw_graph_from_solutions(solutions, start_word, end_word):
    if solutions == []:
        return
    
    G = nx.DiGraph()

    # we extract all the graph nodes and the graph edges
    graph_nodes = {}
    graph_edges = set()
    for solution in solutions:
        for i in range(len(solution)-1):
            # i is the "depth" of the node, so we can later display it layer-by-layer
            graph_nodes[solution[i]] = i
            graph_edges.add( (solution[i], solution[i+1]) )
    graph_nodes[end_word] = len(solutions[0])-1

    # we add the 'layer' attribute to the graph
    for node, layer in graph_nodes.items():
        G.add_nodes_from([node], layer=layer)
    G.add_edges_from(list(graph_edges))
    
    # getting node colors
    node_layers = [data["layer"] for v, data in G.nodes(data=True)]
    manual_colors = ["pink", "tab:red", "darkorange", "gold", "limegreen", "lightblue", "tab:blue", "violet"]
    
    # color and position based on layer
    pos = nx.multipartite_layout(G, subset_key="layer")

    # drawing graph
    options = {"with_labels":True, "edgecolors": "black", "node_size": 1000, "alpha": 1.0, "font_size": 10}
    try:
        # the colors I've defined can handle up to a depth of 7, but if we requre more
        # then I can arbitrarily subdivide plt.cm.rainbow
        # I just like my custom colors asthetically better
        manual_node_colors = [manual_colors[data["layer"]] for v, data in G.nodes(data=True)]
        nx.draw(G, pos, node_color=manual_node_colors, **options)
    except:
        nx.draw(G, pos, node_color=node_layers, cmap=plt.cm.rainbow, **options)
    
    # display
    plt.show()

def main(dictionary, args):
    start_word = args.start.lower()
    end_word = args.end.lower()

    optimal_length, solutions = solver_bidirectional(dictionary, start_word, end_word, verbose=args.verbose, progress_bar=args.progress_bar, debug=args.debug)
    number_of_solutions = len(solutions)
    
    print()
    print("Optimal Length:", optimal_length)
    print(f"All Optimal Solutions ({number_of_solutions} total):")

    solution_strings = [" --> ".join(solution) for solution in solutions]
    for solution_string in sorted(solution_strings):
        print('\t', solution_string)

    all_words = set()
    for solution in solutions:
        all_words = all_words.union(solution)
    
    number_of_intermittent_words = len(all_words) - 2

    # roughly speaking, the difficulty is proportional to the length of the optimal sequence
    # since the longer the sequence the more steps you have to think ahead
    # and the difficulty is roughly inversely proportional to the number of intermitten words that are possible
    # because the less words you can use for your solution the hard it is to find a solution
    difficulty = optimal_length / number_of_intermittent_words
    
    # it's not a perfect metric, but it's also not terrible
    print()
    print(f"Difficulty Score: {difficulty:.4f}")

    draw_graph_from_solutions(solutions, start_word, end_word)

if __name__ == "__main__":
    args = get_args()

    if len(args.start) != len(args.end):
        raise ValueError("The length of the two words must be the same")
    
    n = len(args.start)
    word_file = ""
    if n == 4:
        word_file = "words4.txt"
    elif n == 5:
        word_file = "words5.txt"
    else:
        raise ValueError(f"Words of length {n} is not supported")
    
    with open(word_file, 'r') as f:
        lines = f.readlines()
    dictionary = [word.strip() for word in lines]
    
    start_word = args.start.lower()
    end_word = args.end.lower()
    if start_word not in dictionary:
        raise ValueError(f"'{start_word}' is not in our word list")
    if end_word not in dictionary:
        raise ValueError(f"'{end_word}' is not in our word list")
    
    main(dictionary, args)