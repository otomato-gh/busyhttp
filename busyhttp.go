package main

import (
	"fmt"
	"log"
	"net/http"
	"runtime"
	"strconv"
	"sync"
	"time"
)

const MegaByte = 1024 * 1024

var memBuf [][]byte
var memMutex sync.Mutex

func busyCPU(w http.ResponseWriter, r *http.Request) {
	until := time.Now().Add(time.Second)
	for time.Now().Before(until) {
	}
	fmt.Fprintln(w, "I've been busy for 1 second.")
}

func busyCPUSecs(w http.ResponseWriter, r *http.Request) {
	secsStr := r.URL.Path[len("/cpu/"):] // naive but simple
	secs, err := strconv.Atoi(secsStr)
	if err != nil || secs < 1 {
		http.Error(w, "invalid seconds", http.StatusBadRequest)
		return
	}
	var wg sync.WaitGroup
	for i := 0; i < secs; i++ {
		wg.Add(1)
		go func() {
			busyCPU(nil, nil)
			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Fprintf(w, "I've been busy for %d seconds.\n", secs)
}

func busyMemoryMB(w http.ResponseWriter, r *http.Request) {
	mbStr := r.URL.Path[len("/memory/"):]
	mb, err := strconv.Atoi(mbStr)
	if err != nil || mb < 1 {
		http.Error(w, "invalid mb", http.StatusBadRequest)
		return
	}
	memMutex.Lock()
	for i := 0; i < mb; i++ {
		memBuf = append(memBuf, make([]byte, MegaByte))
	}
	memMutex.Unlock()
	time.Sleep(time.Second)
	fmt.Fprintf(w, "I've allocated %d MB of memory.\n", mb)
}

func freeMemoryMB(w http.ResponseWriter, r *http.Request) {
	mbStr := r.URL.Path[len("/memfree/"):]
	mb, err := strconv.Atoi(mbStr)
	if err != nil || mb < 1 {
		http.Error(w, "invalid mb", http.StatusBadRequest)
		return
	}
	time.Sleep(time.Second)
	memMutex.Lock()
	if len(memBuf) >= mb {
		memBuf = memBuf[:len(memBuf)-mb]
		memMutex.Unlock()
		fmt.Fprintf(w, "I've released %d MB of memory.\n", mb)
		return
	}
	memBuf = nil
	memMutex.Unlock()
	fmt.Fprintln(w, "No more memory to release.")
}

func busyMemory(w http.ResponseWriter, r *http.Request) {
	memMutex.Lock()
	memBuf = append(memBuf, make([]byte, MegaByte))
	memMutex.Unlock()
	time.Sleep(time.Second)
	fmt.Fprintln(w, "I've allocated 1 MB of memory.")
}

func freeMemory(w http.ResponseWriter, r *http.Request) {
	time.Sleep(time.Second)
	memMutex.Lock()
	if len(memBuf) > 0 {
		memBuf = memBuf[:len(memBuf)-1]
		memMutex.Unlock()
		fmt.Fprintln(w, "I've released 1 MB of memory.")
		return
	}
	memBuf = nil
	memMutex.Unlock()
	fmt.Fprintln(w, "No more memory to release.")
}

func root(w http.ResponseWriter, r *http.Request) {
	busyCPU(w, r)
}

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())
	http.HandleFunc("/", root)
	http.HandleFunc("/cpu", busyCPU)
	http.HandleFunc("/cpu/", busyCPUSecs)
	http.HandleFunc("/memory", busyMemory)
	http.HandleFunc("/memory/", busyMemoryMB)
	http.HandleFunc("/memfree", freeMemory)
	http.HandleFunc("/memfree/", freeMemoryMB)
	log.Fatal(http.ListenAndServe(":80", nil))
}
