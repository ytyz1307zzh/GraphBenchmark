"""
Down-sample a sub-graph of the original graph.
"""

import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('-input', required=True, help='path to input file')
parser.add_argument('-max_node', required=True, type=int, help='The number of nodes to keep')
parser.add_argument('-output', required=True, help='path to output file')
opt = parser.parse_args()
print(opt)

edge_cnt = 0
node_set = set()

with open(opt.input, 'r', encoding='utf8') as fin:
    with open(opt.output, 'w', encoding='utf8') as fout:

        for line in tqdm(fin.readlines()):
            edge = line.strip().split()
            from_node = int(edge[0])
            to_node = int(edge[1])

            if from_node >= opt.max_node or to_node >= opt.max_node:
                continue

            fout.write(line)
            edge_cnt += 1

            if from_node not in node_set:
                node_set.add(from_node)
            if to_node not in node_set:
                node_set.add(to_node)

print(f'A sub-graph with {len(node_set)} nodes and {edge_cnt} edges created.')

