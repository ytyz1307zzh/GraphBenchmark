# Graph Benchmarks
Comparing different open-source graph analysis packages using benchmark graph tasks

### Environment
We suggest set up different Anaconda virtual environments for each of the packages.
Experiments are run with Python 3.7. Besides, you should install `matplotlib==3.3`.
For commands to install the graph packages, see `setup.md`.

### Packages
1. Graph-tool
2. igraph
3. NetworkX
4. Networkit
5. SNAP

### Data
1. [Amazon product co-purchasing network](https://snap.stanford.edu/data/amazon0302.html) (262k nodes, 1.2m edges)
2. [Google web graph](https://snap.stanford.edu/data/web-Google.html) (875k nodes, 5.1m edges)

### Tasks
1. Data loading
2. Shortest path
3. PageRank
4. k-core
5. Strongly connected components

### Features
Outputs of the scripts include:
1. Total runtime
2. Peak virtual memory size
3. CPU usage and Resident Set Size (RSS) throughout the process, given by `procpath` (figure)
4. `ps` data throughout the process
5. CPU usage and Virtual Memory Size (VMS) throughout the process, given by `ps -aux` (figure)

### Run
```bash
sh scripts/snap.sh
```
Scripts for other packages can also be found in `scripts` and run using similar commands.
