from igraph import *
from benchmark import benchmark
from datetime import datetime
import sys
import os
import subprocess

filename = sys.argv[1]
n = int(sys.argv[2])

# get the pid of the current process
pid = os.getpid()
print("Process pid: ", pid)

# start a subprocess to monitor the
monitor_cmd = f"procpath record -i 0.1 -d ff.sqlite '$..children[?(@.stat.pid == {pid})]'"
print("Executing command: ", monitor_cmd)
p_monitor = subprocess.Popen(monitor_cmd, shell=True)

# store the time before data loading
start_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
print("Start time in UTC: ", start_time)

print(f"Profiling dataset {filename}")

print("Profiling loading")
print("=================")
print()

benchmark("Graph.Read(filename, format='edges')", globals=globals(), n=n)
g = Graph.Read(filename, format='edges')

print("Profiling shortest path")
print("=======================")
print()

benchmark("g.shortest_paths([g.vs[0]])", globals=globals(), n=n)

print("Profiling PageRank")
print("==================")
print()

benchmark("g.pagerank(damping=0.85, eps=1e-3)", globals=globals(), n=n)

print("Profiling k-core")
print("================")
print()

benchmark("g.coreness(mode='all')", globals=globals(), n=n)

print("Profiling strongly connected components")
print("=======================================")
print()

benchmark("[i for i in g.components(mode=STRONG)]", globals=globals(), n=n)

# stop the monitor process
p_monitor.kill()

# store the time after running the algorithm
end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
print("End time in UTC: ", end_time)

cpu_draw_cmd = f"procpath plot -d ff.sqlite -q cpu -f output/igraph_cpu.svg -p {pid} -a {start_time} -b {end_time}"
rss_draw_cmd = f"procpath plot -d ff.sqlite -q rss -f output/igraph_rss.svg -p {pid} -a {start_time} -b {end_time}"
print("Executing command: ", cpu_draw_cmd)
os.system(cpu_draw_cmd)
print("Executing command: ", rss_draw_cmd)
os.system(rss_draw_cmd)
