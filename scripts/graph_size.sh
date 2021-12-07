#!bin/bash

algorithms=(
    "shortest_path"
    "pagerank"
)

packages=(
    "graphtool"
    "igraph"
    "networkit"
    "networkx"
    "snap"
)

num_nodes=(
    "100"
    "1k"
    "10k"
)

for n in "${num_nodes[@]}"; do
    for pack in "${packages[@]}"; do
        for alg in "${algorithms[@]}"; do
            python code/"$pack"/"$pack"_"$alg".py data/amazon_"$n".txt
            echo
        done
    done
done
