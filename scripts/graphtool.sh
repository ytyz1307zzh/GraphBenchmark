#!bin/bash

algorithms=(
    "io"
    "shortest_path"
    "pagerank"
    "kcore"
    "scc"
)

graphs=("amazon" "google")

for data in "${graphs[@]}"; do
    for alg in "${algorithms[@]}"; do
        python code/graphtool/graphtool_"$alg".py data/"$data".txt
        echo
    done
done
