import time

MEGABYTE = 1024 * 1024

from flask import Flask
application = Flask(__name__)

class memBuf:
    buffer = ['X' * 50 * MEGABYTE]

#leaving cpu loding on root path for bw compat 
@application.route("/")    
@application.route("/cpu")
def busy_cpu():
    until = time.time() + 0.5
    while time.time() < until:
        pass
    return "I've been busy for 0.5 seconds.\n"

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
