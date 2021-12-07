from igraph import *
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from benchmark import benchmark
from datetime import datetime
import subprocess
import matplotlib.pyplot as plt


script_name = sys.argv[0]
filename = sys.argv[1]
# n = int(sys.argv[2])
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

print("Profiling strongly connected components")
print("=======================================")

g = Graph.Read(filename, format='edges')
# benchmark("[i for i in g.components(mode=STRONG)]", globals=globals(), n=n)

start_time = datetime.now()
res = [i for i in g.components(mode=STRONG)]
end_time = datetime.now()
time_delta = end_time - start_time
print(f'Execute time: {time_delta.seconds + time_delta.microseconds / 1e6}s')
print("=================")

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

# parse the "watch" data
cpu_trend, vm_trend = [], []
with open(watch_outf, 'r', encoding='utf8') as fin:
    for line in fin:
        if not line:
            continue
        fields = line.strip().split()
        cpu_trend.append(float(fields[2]))
        vm_trend.append(round(int(fields[4]) / 1000, 1))

# plot into one figure with double y axes
x = [0.1 * ti for ti in range(len(cpu_trend))]
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(x, cpu_trend, 'g-')
ax_right.plot(x, vm_trend, 'b-')

ax_left.set_xlabel('Run Time')
ax_left.set_ylabel('CPU%', color='g')
ax_right.set_ylabel('VM Size', color='b')

watch_plot_path = f"output/{package_name}/{graph_name}/{alg_name}/watch.png"
plt.savefig(watch_plot_path, bbox_inches='tight')
print(f'Watch data saved to {watch_plot_path}')
