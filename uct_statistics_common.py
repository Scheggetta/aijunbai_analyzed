import os
import datetime
import time
import random
import numpy as np
import pandas as pd
import common


def uct(root_state, iter_max, search_tree=None, verbose=True):
    """ Conduct a uct search for __iter_max iterations starting from root_state.
        Return the best move from the root_state.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    """ Setting csv name and header """
    filename = "plain-uct_" + datetime.datetime.now().strftime('%d%m%y%H%M%S') + ".csv"
    header = ["Iteration", "Move", "Q", "V", "N", "tU", "tR", "tT"]
    np_array = None

    should_clean = True

    if search_tree is None:
        search_tree = common.SearchTree()
        should_clean = False

    max_depth = 0
    node_count = search_tree.size()

    root_node = common.SearchNode(tree_node=search_tree.get_node(root_state))

    for i in range(iter_max):

        node = root_node

        # Select
        t1 = time.time()
        while not node.untried_moves() and node.child_nodes():  # node is fully expanded and non-terminal
            node = node.uct_select_child(1.0)
        tU = time.time() - t1

        state = node.state().clone()

        # Expand
        m = random.choice(node.untried_moves()) if node.untried_moves() else None
        if m is not None:  # if we can expand (i.e. state/node is non-terminal)
            state.do_move(m)
            node = node.add_child(m, search_tree.get_node(state))  # add child and descend search_tree
        max_depth = max(node.depth, max_depth)

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        t2 = time.time()
        moves = state.get_moves()
        while moves:  # while state is non-terminal
            state.do_move(random.choice(moves))
            moves = state.get_moves()
        tR = time.time() - t2

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node

            # state is terminal. update node with get_result from POV of node.player_just_moved
            node.update(state.get_result(node.player_just_moved()))

            if node.parent_node == root_node:
                # print "Root node! " + i.__str__()
                tree_node = node.get_tree_node()

                for (m, n) in root_node.child_nodes().items():
                    if n.state() == tree_node.state():
                        move = m
                        q = n.value()

                v = tree_node.get_wins()
                n = tree_node.get_visits()

            node = node.parent_node

        tT = time.time() - t1

        """ Updating array """
        row = np.array([i, move, q, v, n, tU, tR, tT])
        if i == 0:
            np_array = row
        else:
            np_array = np.vstack((np_array, row))

    pd_array = pd.DataFrame(np_array)
    pd_array.columns = header
    print pd_array

    """ Creating csv file """
    project_dir = os.path.dirname(__file__)
    stat_dir = os.path.join(project_dir, 'stat/')
    filename = stat_dir + filename
    pd_array.to_csv(filename, index=False)

    selected_node = root_node.uct_select_child(0.0)

    if verbose:
        print "Max search depth:", max_depth
        print "Nodes generated:", str(search_tree.size() - node_count)
        print
        print root_node.children2string()

    if should_clean:
        root_node.clean_sub_tree(selected_node, search_tree)
        if verbose:
            print "Nodes remaining:", str(search_tree.size())

    if verbose:
        print

    return selected_node.move
