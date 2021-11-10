# Setup and Installation

### Installing graph-tool

```
conda create --name graphtool
conda activate graphtool
conda install -y -c conda-forge graph-tool
```

### Installing igraph

```
conda create --name igraph
conda activate igraph
conda install -y -c conda-forge python-igraph
```

### Installing networkx

```
conda create --name networkx
conda activate networkx
conda install -y -c anaconda networkx
```

### Installing networkit

Install Clang++ (note: have to install 3.7 / 3.8) and cmake

```
sudo apt install clang-3.8
sudo apt install cmake
```

Install networkit

```
pip install ipython
conda create --name networkit
conda activate networkit
conda install -y -c conda-forge networkit ipython
```

### Installing SNAP

```
conda create --name snap
conda activate snap
pip install snap-stanford
```

