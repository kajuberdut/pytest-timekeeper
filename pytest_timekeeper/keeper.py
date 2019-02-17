# from pytest_timekeeper.writers import Writer, JsonWriter
from statistics import mean
from typing import Any, Dict, List, Optional

import _pytest.config as pytest_config
from _pytest.terminal import TerminalReporter

import dataclasses
from pytest_timekeeper.monitor import Monitor
from pytest_timekeeper.timer import Timer


@dataclasses.dataclass
class TimeKeeper:
    _config: pytest_config.Config = None
    warmup_loops: int = 5
    calibration_loops: int = 15
    _timers: List[Timer] = dataclasses.field(default_factory=list)
    _calibration: List[int] = dataclasses.field(default_factory=list)
    _monitor: Optional[Monitor] = None
    _report_lines: List[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.calibrate()

    def get_timer(self, test_name: str, test_version: Any) -> Timer:
        timer = Timer(test_name=test_name, test_version=test_version)
        self._timers.append(timer)
        return timer

    def run_calibration(self, save=True):
        timer = Timer(test_name=None)
        timer.start()
        timer.stop()
        if save:
            self._calibration.append(timer.runtime_ns)

    def calibrate(self):
        for i in range(self.warmup_loops):
            self.run_calibration(save=False)
        for i in range(self.calibration_loops):
            self.run_calibration(save=True)

    def start_monitor(self) -> None:
        self._monitor = self.config.hook.pytest_timekeeper_set_monitor()
        self._monitor.start()  # type: ignore

    def stop_monitor(self) -> None:
        if self._monitor:
            self._monitor.stop()

    @property
    def monitor(self) -> Optional[Monitor]:
        return self._monitor

    @property
    def monitored(self):
        """ True if an instance of Monitor was setup. """
        return isinstance(self._monitor, Monitor)

    @property
    def config(self) -> pytest_config.Config:
        return self._config

    @property
    def sys_info(self) -> Dict[str, Any]:
        """ A dictionary of basic information about the host system. """
        if self.monitored is not None:
            return self._monitor.sys_info  # type: ignore
        else:
            return {}

    @property
    def sys_state_history(self):
        """ A list of dictionaries containing the system state at a specific time. """
        if self.monitored:
            return self._monitor.sys_state_history
        else:
            return None

    @property
    def sys_dict(self):
        """ A dictionary containing Keeper.sys_info and Keeper.sys_state_history. """
        return {
            "system": {"info": self.sys_info, "state_history": self.sys_state_history}
        }

    @property
    def timers(self) -> List[Timer]:
        """ A list of timer objects created by this Keeper. """
        return self._timers

    @property
    def timer_dict(self) -> Dict[str, Any]:
        """ A dictionary containing timer objects created by this keeper
            {"function_timers": List[Dict]}
        """
        return {"function_timers": [t.asdict() for t in self._timers]}

    @property
    def calibration_dict(self) -> Dict[str, Any]:
        """ A dictionary containing calibration information about the test session
            {"runs": List[int], "mean": int}
        """
        return {
            "calibration": {
                "runs": self._calibration,
                "mean": round(mean(self._calibration)),
            }
        }

    @property
    def data(self):
        """ A dictionary containing Keeper.sys_dict and Keeeper.timer_dict """
        return {**self.sys_dict, **self.timer_dict, **self.calibration_dict}

    def finalize(self):
        self.stop_monitor()
        writer = self.config.hook.pytest_timekeeper_set_writer()
        writers = [writer] + self.config.hook.pytest_timekeeper_add_writer()
        for w in writers:
            w.finalize(self)

    def write_report(self, tr: TerminalReporter):
        for line in self.report:
            tr.write_line(line)

    @property
    def report(self):
        return self._report_lines

    def report_line(self, line):
        self._report_lines.append(line)
