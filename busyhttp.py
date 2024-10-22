import time
import multiprocessing

MEGABYTE = 1024 * 1024

from flask import Flask
application = Flask(__name__)

class memBuf:
    buffer = []

#leaving cpu loding on root path for bw compat 
@application.route("/")    
@application.route("/cpu")
def busy_cpu():
    print("busy_cpu\n")
    until = time.time() + 1
    while time.time() < until:
        pass
    return "I've been busy for 1 second.\n"

@application.route("/cpu/<int:seconds>")
def busy_cpu_seconds(seconds):
    processes = [multiprocessing.Process] * seconds
    for i in range(0, seconds):
        processes[i] = multiprocessing.Process(target=busy_cpu)
        processes[i].start()
    for i in range(0, seconds):
        processes[i].join()
    
    return "I've been busy for " + str(seconds) + " seconds.\n"

@application.route("/memory/<int:mb>")
def busy_memory_mb(mb):
    memBuf.buffer += ['A' * MEGABYTE] * mb
    time.sleep(1)
    return "I've allocated " + str(mb) + " MB of memory.\n"

@application.route("/memfree/<int:mb>")
def free_memory_mb(mb):
    time.sleep(1)
    if len(memBuf.buffer) >= mb:
      del memBuf.buffer[len(memBuf.buffer)-mb:]
      return "I've released " + str(mb) + " MB of memory.\n"
    return "No more memory to release.\n"


@application.route("/memory")
def busy_memory():
    memBuf.buffer += ['A' * MEGABYTE]
    time.sleep(1)
    return "I've allocated 1 MB of memory.\n"

@application.route("/memfree")
def free_memory():
    time.sleep(1)
    if len(memBuf.buffer) > 0:
      del memBuf.buffer[len(memBuf.buffer)-1:]
      return "I've released 1 MB of memory.\n"
    return "No more memory to release.\n"
