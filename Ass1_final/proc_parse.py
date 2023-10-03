import os
import sys
import time

# Function to read and parse values from /proc files
def read_proc_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "N/A"

# Function to print system information for the default version
def print_default_info():
    print("Processor type:", os.uname().machine)
    print("Kernel version:", os.uname().release)
    print("Memory configured (KB):", int(read_proc_file('/proc/meminfo').split()[1]))
    print("Virtual memory address range mapped to System RAM, Kernel:")
    print(read_proc_file('/proc/iomem').splitlines()[29])
    print(read_proc_file('/proc/iomem').splitlines()[30])
    print(read_proc_file('/proc/iomem').splitlines()[31])
    print(read_proc_file('/proc/iomem').splitlines()[32])
    print(read_proc_file('/proc/iomem').splitlines()[33])
    print("Total RAM (KB):", int(read_proc_file('/proc/meminfo').split()[1]))
    print("Available RAM (KB):", int(read_proc_file('/proc/meminfo').split()[7]))
    uptime = float(read_proc_file('/proc/uptime').split()[0])
    print("Time since last boot (seconds):", uptime)

# Function to print dynamic system information for the second version
def print_dynamic_info(read_rate, print_rate):
    num_samples = print_rate // read_rate
    total_time=0
    user_percent=0
    sys_percent=0
    idle_percent=0
    free_mem=0
    total_mem=0
    diskstats=0
    disk_read_rate=0
    disk_write_rate=0
    ctxt=0
    forks=0
    while True:
        user_time = os.popen("grep 'cpu ' /proc/stat | awk '{print $2}'").readline()
        nice_time = os.popen("grep 'cpu ' /proc/stat | awk '{print $3}'").readline()
        sys_time = os.popen("grep 'cpu ' /proc/stat | awk '{print $4}'").readline()
        idle_time = os.popen("grep 'cpu ' /proc/stat | awk '{print $5}'").readline()

        user_time = int(user_time)
        nice_time = int(nice_time)
        sys_time = int(sys_time)
        idle_time = int(idle_time)

        total_time = user_time + nice_time + sys_time + idle_time + total_time
        user_percent = ((user_time / total_time) * 100)+user_percent
        sys_percent = ((sys_time / total_time) * 100)+sys_percent
        idle_percent = ((idle_time / total_time) * 100)+idle_percent

        free_mem = (int(read_proc_file('/proc/meminfo').split()[7]))+free_mem
        total_mem = (int(read_proc_file('/proc/meminfo').split()[1]))+total_mem 

        diskstats = os.popen("cat /proc/diskstats | awk 'NR==1{print $6,$10}'").readline().split()
        disk_read_rate = disk_read_rate+(int(diskstats[0]))
        disk_write_rate = disk_write_rate+(int(diskstats[1]))
        with open('/proc/stat', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('ctxt '):
                    ctxt_line = line.strip().split()
                    ctxt = ctxt+int(ctxt_line[1])
                if line.startswith('processes '):
                    fork_line = line.strip().split()
                    forks = forks+int(fork_line[1])    
        num_samples -= 1
        if num_samples == 0:
        	avg= print_rate // read_rate
        	user_percent=user_percent/avg
        	sys_percent=sys_percent/avg
        	idle_percent=idle_percent/avg
        	free_mem=free_mem/avg
        	total_mem=total_mem/avg
        	disk_read_rate=disk_read_rate/avg
        	disk_write_rate=disk_write_rate/avg
        	ctxt=ctxt/avg
        	forks=forks/avg
        	print(f"User CPU usage: {user_percent:.2f}%")
        	print(f"System CPU usage: {sys_percent:.2f}%")
        	print(f"Idle CPU usage: {idle_percent:.2f}%")
        	print(f"Free memory (KB): {free_mem}")
        	print(f"Total memory (KB): {total_mem}")
        	print(f"Disk read rate (sectors/s): {disk_read_rate}")
        	print(f"Disk write rate (sectors/s): {disk_write_rate}")
        	print(f"Context switches per second: {ctxt}")
        	print(f"Process creations per second: {forks}")
        	num_samples= print_rate // read_rate			
        time.sleep(read_rate)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_default_info()
    elif len(sys.argv) == 3 and sys.argv[1].isdigit() and sys.argv[2].isdigit():
        read_rate = float(sys.argv[1])
        print_rate = float(sys.argv[2])
        print_dynamic_info(read_rate, print_rate)
