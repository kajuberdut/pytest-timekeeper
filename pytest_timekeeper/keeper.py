# from pytest_timekeeper.writers import Writer, JsonWriter
from typing import List, Optional

from _pytest.config import Config

from pytest_timekeeper.monitor import Monitor
from pytest_timekeeper.timer import Timer

import dataclasses


@dataclasses.dataclass
class TimeKeeper:
    _config: Config
    _timers: List[Timer] = dataclasses.field(default_factory=list)
    _monitor: Optional[Monitor] = None

    def get_timer(self, test_name, test_version) -> Timer:
        timer = Timer(test_name=test_name, test_version=test_version)
        self._timers.append(timer)
        return timer

    def start_monitor(self):
        self._monitor = self._config.hook.pytest_timekeeper_set_monitor()
        self._monitor.start()

    def stop_monitor(self):
        self._monitor.stop()

    def finalize(self):
        writer = self._config.hook.pytest_timekeeper_set_writer()
        writers = [writer] + self._config.hook.pytest_timekeeper_add_writer()
        for w in writers:
            w.finalize(self._timers)
