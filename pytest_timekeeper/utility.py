import socket
from hashlib import md5

import psutil


def version(version):
    def set_version(func):
        func._version = version
        return func

    return set_version


def get_machine_info():
    current, minimum, maximum = psutil.cpu_freq()
    total, available, percent, used, free, active, inactive, buffers, cached, shared, slab = (
        psutil.virtual_memory()
    )
    hostname = socket.gethostname()
    return {
        "threads": psutil.cpu_count(),  # Threads
        "cores": psutil.cpu_count(logical=False),  # Physical CPU
        "freq_min": round(minimum),
        "freq_max": round(maximum),
        "hostname": hostname,
        "mem_total": total,
        "hash": md5(
            f"{hostname}{psutil.cpu_count(logical=False)}{total}".encode()
        ).hexdigest(),
    }


def get_machine_state():
    current, minimum, maximum = psutil.cpu_freq()
    total, available, percent, used, free, active, inactive, buffers, cached, shared, slab = (
        psutil.virtual_memory()
    )
    return {
        "cpu_percent": psutil.cpu_percent(),
        "freq_current": round(current),
        "mem_percent": round(available / total, 2),
    }
