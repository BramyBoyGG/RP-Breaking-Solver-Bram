#!/usr/bin/env python3
# encoding: utf-8
"""
@time: 5/28/21 4:56 PM
@file: generate-tree-bn.py
@desc: Script to generate a TREE-like Bayesian Network with a fraction of the
nodes deterministic, and one query node. Also creates an associated evidence file.
"""

import argparse
import numpy as np
import os
import random
from datetime import datetime

parser = argparse.ArgumentParser(description='Generate Tree-like Bayesian Network in .net format.')
parser.add_argument_group('Mandatory arguments')
parser.add_argument('--size', type=int, help='Number of nodes in the tree.')
parser.add_argument('--maxchild', type=int, help='Maximum number of children per node')
parser.add_argument('--seed', type=int, help='Random seed.')
parser.add_argument('--outdir', type=str, help='Path to where to write the file.')
parser.add_argument('--outfile', type=str, help='Filename for outfile.')
args = parser.parse_args()

PROJECT_HOME = os.environ.get('PROJECT_HOME')
OUT_DIR = args.outdir

# Create outdirs
for outdir in ['/net', '/evidence']:
    if not os.path.exists(OUT_DIR + outdir):
        os.makedirs(OUT_DIR + outdir)

# Initialise random seed
np.random.seed = args.seed

# Define outfiles
net_outfile = args.outfile if args.outfile.endswith('.net') else args.outfile + '.net'
evi_outfile = args.outfile.replace('.net', '.inst') if args.outfile.endswith('.net') else args.outfile + '.inst'


def make_tree(size_):
    """
    Create a TREE Bayesian Network.
    :param size_: Number of nodes in the tree.
    :param det_: Fraction of nodes that is deterministic
    """
    string = "net\n{\n}\n"

    # NODES
    nodes = []
    for i in range(size_):
        nodeId = "v_{}".format(i + 1)
        # Each node has two states, e.g., "v_1_true" and "v_1_false"
        string += "node " + nodeId + "\n{\n\t states = (\"" + nodeId + "true\" \"" + nodeId + "false\");\n}\n"
        nodes.append(nodeId)

    q_node = nodes[-1]

    # EDGES (tree structure: each node has max maxchild number of children, randomly assign parents to nodes)
    parent_map = {nodes[0]: []}  # Root node has no parents
    for node in nodes[1:]:
        parent_candidates = list(parent_map.keys())
        parent = random.choice(parent_candidates)
        if len(parent_map.get(parent, [])) < args.maxchild:
            parent_map.setdefault(parent, []).append(node)
        else: # if more than maxchild get previous node
            previous_node = nodes[nodes.index(node) - 1]
            parent_map.setdefault(previous_node, []).append(node)

    for index, node in enumerate(nodes):
        input_nodes = parent_map.get(node, [])

        string += "potential ( {}".format(node)
        if len(input_nodes) > 0:
            string += " | "
            string += " ".join(input_nodes)
        string += " )\n{\n\t data = ("

        for _ in range(2 ** len(input_nodes)):
            if len(input_nodes) > 0:
                string += "\t("
            string += "{0:.2f} {1:.1f}".format(1, 0)
            if len(input_nodes) > 0:
                string += ")\n"

        if string.endswith('\n'):
            string = string[:-1] + ");\n}\n"
        else:
            string += ");\n}\n"

    return string, q_node


def create_evidence(q_node):
    """ Create an evidence file for the query node.
    :param q_node: string that represents the id of the node that we want to query.
    :return: string of the evidence file.
    """
    s = '<?xml version="1.0" encoding="UTF-8"?>\n'
    s += '<instantiation date="{date}">\n'.format(date=datetime.now().strftime("%d %B %Y, %H:%M:%S"))
    s += '<inst id="{nodeID}" value="{nodeID}{choice}"/>\n'.format(nodeID=q_node, choice=np.random.choice(['true', 'false']))
    s += '</instantiation>'
    return s


# Create the tree Bayesian Network
tree_bn, query_node = make_tree(args.size)

# Write the network to the .net file
with open(OUT_DIR + '/net/' + net_outfile, "w") as fh:
    fh.write(tree_bn)
    fh.close()

# Create the evidence file
evi = create_evidence(query_node)
with open(OUT_DIR + '/evidence/' + evi_outfile, "w") as fh:
    fh.write(evi)
    fh.close()
