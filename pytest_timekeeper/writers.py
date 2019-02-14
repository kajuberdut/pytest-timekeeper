import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import dataclasses
import ujson as json
from pytest_timekeeper.keeper import TimeKeeper

# requests is an optional dependency
try:
    import requests
except ImportError:
    requests = None


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

    def serialized(self, keeper):
        return self.serializer(keeper.data)

    def finalize(self, keeper: TimeKeeper):
        with open(self.filepath, "w") as fh:
            fh.write(self.serialized(keeper))


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
