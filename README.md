# busyhttp.py

This repo provides a simple Flask web application that simulates CPU and memory load for testing purposes.

## Routes:
-     /cpu
        Simulates CPU load for 1 second.
-     /cpu/<int:seconds>
        Simulates CPU load for a specified number of seconds using multiprocessing.
-     /memory/<int:mb>
        Allocates a specified number of megabytes of memory and holds it for 1 second.
-     /memfree/<int:mb>
        Releases a specified number of megabytes of memory if available.
-     /memory
        Allocates 1 megabyte of memory and holds it for 1 second.
-     /memfree
        Releases 1 megabyte of memory if available.

## Classes:
-     memBuf
        A class that contains a static buffer list used to simulate memory allocation.