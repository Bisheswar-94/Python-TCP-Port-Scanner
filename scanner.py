import socket
import threading
from queue import Queue
from datetime import datetime

# Banner
print("=" * 60)
print("        PYTHON TCP PORT SCANNER WITH THREADS")
print("=" * 60)

# User Input
target = input("Enter Target IP or Domain: ")

start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

# Resolve Domain to IP
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("[-] Invalid Target")
    exit()

print(f"\n[+] Scanning Target: {target}")
print(f"[+] IP Address: {target_ip}")
print(f"[+] Port Range: {start_port} - {end_port}")
print(f"[+] Scan Started At: {datetime.now()}\n")

# Queue for Ports
port_queue = Queue()

# Lock for Clean Output
print_lock = threading.Lock()


# Port Scanning Function
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            with print_lock:
                print(f"[OPEN] Port {port}")

        sock.close()

    except:
        pass


# Thread Worker
def worker():
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(port)
        port_queue.task_done()


# Add Ports to Queue
for port in range(start_port, end_port + 1):
    port_queue.put(port)

# Number of Threads
thread_count = 100

threads = []

# Start Threads
for _ in range(thread_count):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)

# Wait for Completion
for thread in threads:
    thread.join()

print("\n[+] Scanning Completed")
print(f"[+] Finished At: {datetime.now()}")