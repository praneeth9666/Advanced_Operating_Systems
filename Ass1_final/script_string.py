import sys

pid = int(sys.argv[1])

string1 ="This is my initial string"
string2 ="This is a different string"

maps_filename = "/proc/{}/maps".format(pid)

mem_filename = "/proc/{}/mem".format(pid)

maps_file = open('/proc/{}/maps'.format(pid), 'r')

for line in maps_file:
    sub_line = line.split(' ')
    if sub_line[-1][:-1] != "[heap]":
    	continue
    heap_addr = sub_line[0]
    heap_addr = heap_addr.split("-")
    addr_start = int(heap_addr[0], 16)
    addr_end = int(heap_addr[1], 16)
    mem_file = open(mem_filename, 'rb+')
    mem_file.seek(addr_start)
    heap = mem_file.read(addr_end - addr_start)
    i = heap.index(bytes(string1, "ASCII"))
    mem_file.seek(addr_start + i)
    mem_file.write(bytes(string2, "ASCII"))
    print("String Replaced")
    maps_file.close()
    mem_file.close()
    break
