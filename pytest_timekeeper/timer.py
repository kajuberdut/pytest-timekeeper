import time
from typing import Any, Dict

import dataclasses


@dataclasses.dataclass
class Timer:
    test_name: str
    test_version: int = 0
    start_time_ns: int = 0
    end_time_ns: int = 0
    note: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def start(self):
        if self.start_time_ns != 0:
            raise RuntimeError("Timer was already started.")
        self.start_time_ns = time.time_ns()

    def stop(self):
        self.end_time_ns = time.time_ns()

    def asdict(self):
        return dataclasses.asdict(self)

    @property
    def runtime_ns(self):
        return self.end_time_ns - self.start_time_ns

    @property
    def runtime(self):
        return self.runtime_ns // 1000
