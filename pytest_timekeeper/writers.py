import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import dataclasses
import json
from pytest_timekeeper.keeper import TimeKeeper

# requests is an optional dependency
try:
    import requests
except ImportError:
    requests = None  # type: ignore


class Writer(ABC):
    """
    An abstract representation of the Writer class.
    This class must provide a finalize method that accepts a list of timers for write out.
    """

    @abstractmethod
    def finalize(self, keeper: TimeKeeper):
        """
        This method should handle persisting pytest_timekeepers data.
        The primary data object to be persisted is keeper.data containing both system and timer info.
        To handle system info and timers seperately use keeper.timer_dict, keeper.sys_dict.
        For more granular control over data and format examine the properties of pytest_timekeeper.keeper.Keeper
        """
        pass


@dataclasses.dataclass  # type: ignore
class Serialize(Writer):
    """
    A writer that outputs serialized data to a file.

    Inputs:
    filepath: a writeable filepath.
    serializer: a callable able to serialize a object of type Dict[str, Any]]
    """

    filepath: str
    serializer: Callable[[Dict[str, Any]], str]

    def serialized(self, keeper) -> str:
        return self.serializer(keeper.data)  # type: ignore

    def finalize(self, keeper: TimeKeeper):
        with open(self.filepath, "w") as fh:
            fh.write(self.serialized(keeper))


def default_json_file():
    return Path().cwd() / f"execution_times_{time.time()}.json"


@dataclasses.dataclass  # type: ignore
class JsonWriter(Serialize):
    """
    A writer that outputs json serialized data to a file.

    Inputs:
    filepath (optional): a writeable filepath.
        Default: Path().cdw()/execution_times_{timestamp}.json
    """

    filepath: str = dataclasses.field(default_factory=default_json_file)
    serializer: Callable = json.dumps


class PytestReport(Writer):
    """
    A writer that produces a pytest report after all tests have completed.
    """

    def finalize(self, keeper: TimeKeeper):
        if keeper.monitored:
            keeper.report_line(json.dumps(keeper.sys_dict, indent=2))
        for timer in keeper.timers:
            line_string = "\t" + json.dumps(timer.asdict(), indent=2)
            keeper.report_line(line_string)


@dataclasses.dataclass  # type: ignore
class PostWriter(Writer):
    """
    A writer that posts json Timer data to a specified web address.

    Inputs:
    post_address: the full URI of the end point to which json should be posted.
    """

    url: str
    serializer: Callable = json.dumps

    def __post_init__(self):
        if requests is None:
            raise ImportError("Requests library is required to use PostWriter.")

    def post(self, url: str, data: Union[List[Any], Dict[str, Any]]):
        return

    def finalize(self, keeper: TimeKeeper):
        r = requests.post(self.url, json=self.serializer(keeper.data))
        keeper.report_line(f"[{r.status_code}] {self.url}")
