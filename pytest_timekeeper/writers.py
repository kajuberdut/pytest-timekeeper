import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union, Any

import requests

import dataclasses
import ujson as json
from pytest_timekeeper.keeper import TimeKeeper


class Writer(ABC):
    """
    An abstract representation of the Writer class.
    This class must provide a finalize method that accepts a list of timers for write out.
    """

    @abstractmethod
    def finalize(self, keeper: TimeKeeper):
        pass


@dataclasses.dataclass  # type: ignore
class Serialize(Writer):
    """
    A writer that outputs serialized time data to a file.

    Inputs:
    filepath: a writeable filepath.
    serializer: a callable able to serialize a object of type List[Dict]
    """

    filepath: str
    serializer: Callable

    def finalize(self, keeper: TimeKeeper):
        serialized = self.serializer([dataclasses.asdict(t) for t in keeper.timers])
        with open(self.filepath, "w") as fh:
            fh.write(serialized)


def default_json_file():
    return Path().cwd() / f"execution_times_{time.time()}.json"


@dataclasses.dataclass  # type: ignore
class JsonWriter(Serialize):
    """
    A writer that outputs json serialized time data to a file.

    Inputs:
    filepath (optional): a writeable filepath.
        Default: Path().cdw()/execution_times_{timestamp}.json
    serializer (optional): a callable able to serialize a object of type List[Dict]
        Default: json.dumps
    """

    filepath: str = dataclasses.field(default_factory=default_json_file)
    serializer: Callable = json.dumps


class PytestReport(Writer):
    """
    A writer that produces a pytest report after all tests have completed.
    """

    def finalize(self, keeper: TimeKeeper):
        for timer in keeper.timers:
            line_string = json.dumps(timer.asdict())
            keeper.report_line(line_string)


@dataclasses.dataclass  # type: ignore
class PostWriter(Writer):
    """
    A writer that posts json Timer data to a specified web address.

    Inputs:
    post_address: the full URI of the end point to which json should be posted.
    """

    base_url: str
    test_times_path: Optional[str] = None
    sys_info_path: Optional[str] = None
    state_history_path: Optional[str] = None
    serializer: Callable = json.dumps

    def urlify(self, *args):
        return "/".join([a.strip("/") for a in [self.base_url] + list(args)])

    @property
    def times_url(self):
        if self.test_times_path is None:
            return self.base_url
        else:
            return self.urlify(self.test_times_path)

    @property
    def sys_info_url(self):
        if self.sys_info_path is None:
            return None
        else:
            return self.urlify(self.sys_info_path)

    @property
    def state_history_url(self):
        if self.state_history_path is None:
            return None
        else:
            return self.urlify(self.state_history_path)

    def post(self, url: str, data: Union[List[Any], Dict[str, Any]]):
        return requests.post(url, json=self.serializer(data))

    def finalize(self, keeper: TimeKeeper):
        r = self.post(self.times_url, keeper.timer_dicts)
        keeper.report_line(f"[{r.status_code}] {self.times_url}")

        sys_info = keeper.monitor.sys_info
        if self.sys_info_url and sys_info:
            r = self.post(self.sys_info_url, sys_info)
            keeper.report_line(f"[{r.status_code}] {self.sys_info_url}")

        state_history = keeper.monitor.sys_state_history
        if self.state_history_url and state_history:
            r = self.post(self.state_history_url, state_history)
            keeper.report_line(f"[{r.status_code}] {self.state_history_url}")
