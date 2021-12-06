from graph_tool.all import *
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from benchmark import benchmark
from datetime import datetime
import subprocess


script_name = sys.argv[0]
filename = sys.argv[1]
if len(sys.argv) == 3:
    num_threads = int(sys.argv[2])
else:
    num_threads = 1

# number of threads
openmp_set_num_threads(num_threads)

package_name = script_name.split('/')[-1].split('_')[0]
graph_name = filename.split('/')[-1].split('.')[0]
alg_name = '_'.join(script_name.split('/')[-1].split('.')[0].split('_')[1:])

if not os.path.exists(f'output/{package_name}/{graph_name}/{alg_name}'):
    os.makedirs(f'output/{package_name}/{graph_name}/{alg_name}')

# get the pid of the current process
pid = os.getpid()
print("Process pid: ", pid)

# get the uid of the current user
uid = os.getuid()
print("User id: ", uid)

# start a procpath subprocess to monitor the cpu and rss of a process
procpath_cmd = f"procpath record -i 0.01 -d ff.sqlite '$..children[?(@.stat.pid == {pid})]'"
print("Executing command: ", procpath_cmd)
p_procpath = subprocess.Popen(procpath_cmd, shell=True)

# store the time before data loading
mon_start = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
print("Start time in UTC: ", mon_start)

# start a watch subprocess to monitor the process state
watch_outf = f"output/{package_name}/{graph_name}/{alg_name}/ps.txt"
if os.path.exists(watch_outf):
    os.remove(watch_outf)
watch_cmd = "watch -n 0.1 \'ps -aux | awk \"{if (\$2==%d) print \$0}\" >> %s\' > /dev/null" % (pid, watch_outf)
print("Executing command: ", watch_cmd)
p_watch = subprocess.Popen(watch_cmd, shell=True)

print(f"Profiling dataset {filename}")
print(f"using {openmp_get_num_threads()} threads")

print("Start PageRank")
print("=================")

g = load_graph_from_csv(filename, directed=True, csv_options={
                        'delimiter': '\t', 'quotechar': '"'})
# benchmark('pagerank(g, damping=0.85, epsilon=1e-3, max_iter=10000000).a',
#           globals=globals(), n=n)

start_time = datetime.now()
ret = pagerank(g, damping=0.85, epsilon=1e-3, max_iter=10000000).a
end_time = datetime.now()
time_delta = end_time - start_time
print(f'Execute time: {time_delta.seconds + time_delta.microseconds / 1e6}s')

# stop the monitor process
p_procpath.kill()
pkill_cmd = f"pkill -f \"watch -n 0.1 ps -aux \| awk .*\" -u {uid}"
print("Executing command: ", pkill_cmd)
os.system(pkill_cmd)

# store the time after running the algorithm
mon_end = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
print("End time in UTC: ", mon_end)

# plot the curve of cpu and rss usage
draw_cmd = f"procpath plot -d ff.sqlite -q cpu -q rss " \
           f"-f output/{package_name}/{graph_name}/{alg_name}/cpu_rss.svg " \
           f"-p {pid} -a {mon_start} -b {mon_end}"
print("Executing command: ", draw_cmd)
os.system(draw_cmd)

# find the peak memory usage
peak_cmd = f"grep VmPeak /proc/{pid}/status"
print("Executing command: ", peak_cmd)
os.system(peak_cmd)

# TODO: post-process the "watch" data

