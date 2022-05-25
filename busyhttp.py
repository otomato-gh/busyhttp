import time

MEGABYTE = 1024 * 1024

from flask import Flask
application = Flask(__name__)

class memBuf:
    buffer = []
    
@application.route("/cpu")
def busy_cpu():
    until = time.time() + 1
    while time.time() < until:
        pass
    return "I've been busy for 1 second.\n"

@application.route("/memory")
def busy_memory():
    buffer += ['A' * MEGABYTE for _ in range(0, 1)]
    time.sleep(1)
    return "I've consumed 1 MB of memory.\n"


