# from pytest_timekeeper.writers import Writer, JsonWriter
from typing import List, Optional

from _pytest.config import Config
from _pytest.terminal import TerminalReporter

import dataclasses
from pytest_timekeeper.monitor import Monitor
from pytest_timekeeper.timer import Timer


@dataclasses.dataclass
class TimeKeeper:
    _config: Config
    _timers: List[Timer] = dataclasses.field(default_factory=list)
    _monitor: Optional[Monitor] = None
    _report_lines: List[str] = dataclasses.field(default_factory=list)

    def get_timer(self, test_name, test_version) -> Timer:
        timer = Timer(test_name=test_name, test_version=test_version)
        self._timers.append(timer)
        return timer

    def start_monitor(self):
        self._monitor = self.hooks.pytest_timekeeper_set_monitor()
        self._monitor.start()

    def stop_monitor(self):
        if self._monitor:
            self._monitor.stop()

    def finalize(self):
        self.stop_monitor()
        writer = self.hooks.pytest_timekeeper_set_writer()
        writers = [writer] + self.hooks.pytest_timekeeper_add_writer()
        for w in writers:
            w.finalize(self)

    def report(self, tr: TerminalReporter):
        for line in self.report_lines:
            tr.write_line(line)

    @property
    def timers(self):
        return self._timers

    @property
    def monitor(self):
        return self._monitor

    @property
    def config(self):
        return self._config

    @property
    def hooks(self):
        return self.config.hook

    @property
    def report_lines(self):
        return self._report_lines

    @report_lines.setter
    def report_lines(self, line):
        self._report_lines.append(line)
