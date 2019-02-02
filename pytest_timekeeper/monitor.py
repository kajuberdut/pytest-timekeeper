import platform
import socket
import time
from hashlib import md5
from multiprocessing import Pipe, Process, Queue, SimpleQueue
from multiprocessing.connection import Connection
from typing import Any, Dict, List, Optional

import psutil

import dataclasses


def get_machine_state() -> Dict[str, Any]:
    current, minimum, maximum = psutil.cpu_freq()
    total, available, percent, used, free, active, inactive, buffers, cached, shared, slab = (
        psutil.virtual_memory()
    )
    return {
        "cpu_percent": psutil.cpu_percent(),
        "freq_current": round(current),
        "mem_percent": round(available / total, 2),
        "timestamp_ns": time.time_ns(),
    }


def get_machine_info() -> Dict[str, Any]:
    current, minimum, maximum = psutil.cpu_freq()
    total, available, percent, used, free, active, inactive, buffers, cached, shared, slab = (
        psutil.virtual_memory()
    )
    python_implimentation = platform.python_implementation()
    python_version = platform.python_version()
    hostname = socket.gethostname()
    return {
        "threads": psutil.cpu_count(),  # Threads
        "cores": psutil.cpu_count(logical=False),  # Physical CPU
        "freq_min": round(minimum),
        "freq_max": round(maximum),
        "hostname": hostname,
        "mem_total": total,
        "python_implimentation": python_implimentation,
        "python_version": python_version,
        "hash": md5(
            f"{hostname}{psutil.cpu_count(logical=False)}{total}{python_implimentation}{python_version}".encode()
        ).hexdigest(),
    }


def state_farmer(q: Queue, exit_receiever: Connection, interval: int = 5):
    while not exit_receiever.poll():
        q.put(get_machine_state())
        time.sleep(interval)


@dataclasses.dataclass
class Monitor:
    interval: int = 5
    sys_info: Optional[Dict[str, Any]] = None
    state: List = dataclasses.field(default_factory=list)
    queu: Optional[SimpleQueue] = None
    process: Optional[Process] = None
    exit_sender: Optional[Connection] = None
    exit_receiever: Optional[Connection] = None

    def start(self):
        self.queue = SimpleQueue()
        self.sys_info = get_machine_info()
        self.exit_receiever, self.exit_sender = Pipe(duplex=False)
        self.process = Process(
            target=state_farmer, args=(self.queue, self.exit_receiever, self.interval)
        )
        self.process.start()

    def stop(self):
        self.exit_sender.send(True)
        while not self.queue.empty():
            self.state.append(self.queue.get())
        self.process.join()


if __name__ == "__main__":
    m = Monitor()

    m.start()

    start = time.time()
    time.sleep(15)
    print(time.time() - start)

    m.stop()

    print(m.sys_info)
    print(m.state)
