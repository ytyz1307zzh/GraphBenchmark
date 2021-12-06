#!bin/bash

algorithms=(
    "io"
    "shortest_path"
    "pagerank"
    "kcore"
    "scc"
)

graphs=("google")

num_threads=(1 4 8 16)

for data in "${graphs[@]}"; do
    for alg in "${algorithms[@]}"; do
        for n in "${num_threads[@]}" do
            python code/graphtool/graphtool_"$alg".py data/"$data".txt "$n"
            echo
        done
    done
done
