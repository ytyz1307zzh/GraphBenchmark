from igraph import *
from benchmark import benchmark
from datetime import datetime
import sys
import os
import subprocess

script_name = sys.argv[0]
filename = sys.argv[1]
n = int(sys.argv[2])
package_name = script_name.split('/')[-1].split('_')[0]
graph_name = filename.split('.')[0]

if not os.path.exists(f'output/{graph_name}'):
    os.mkdir(f'output/{graph_name}')

# get the pid of the current process
pid = os.getpid()
print("Process pid: ", pid)

# start a procpath subprocess to monitor the cpu and rss of a process
procpath_cmd = f"procpath record -i 0.1 -d ff.sqlite '$..children[?(@.stat.pid == {pid})]'"
print("Executing command: ", procpath_cmd)
p_procpath = subprocess.Popen(procpath_cmd, shell=True)

# store the time before data loading
start_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
print("Start time in UTC: ", start_time)

# start a watch subprocess to monitor the process state
watch_outf = f"output/{package_name}_ps.txt"
if os.path.exists(watch_outf):
    os.remove(watch_outf)
watch_cmd = "watch -n 0.1 'ps -aux | awk \"{if (\$2==%d) print \$0}\" >> %s' > /dev/null" % (pid, watch_outf)
p_watch = subprocess.Popen(watch_cmd, shell=True)

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
p_procpath.kill()
p_watch.kill()

# store the time after running the algorithm
end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
print("End time in UTC: ", end_time)

# plot the curve of cpu and rss usage
cpu_draw_cmd = f"procpath plot -d ff.sqlite -q cpu -f output/{package_name}_cpu.svg " \
               f"-p {pid} -a {start_time} -b {end_time}"
rss_draw_cmd = f"procpath plot -d ff.sqlite -q rss -f output/{package_name}_rss.svg " \
               f"-p {pid} -a {start_time} -b {end_time}"
print("Executing command: ", cpu_draw_cmd)
os.system(cpu_draw_cmd)
print("Executing command: ", rss_draw_cmd)
os.system(rss_draw_cmd)

# find the peak memory usage
peak_cmd = f"grep VmPeak /proc/{pid}/status"
print("Executing command: ", peak_cmd)
os.system(peak_cmd)

# TODO: post-process the "watch" data


