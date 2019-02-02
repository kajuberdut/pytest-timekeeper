import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, List

import requests

import dataclasses
from pytest_timekeeper.timer import Timer


class Writer(ABC):
    """
    An abstract representation of the Writer class.
    This class must provide a finalize method that accepts a list of timers for write out.
    """

    @abstractmethod
    def finalize(self, timers: List[Timer]):
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

    def finalize(self, timers: List[Timer]):
        serialized = self.serializer([dataclasses.asdict(t) for t in timers])
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

    def finalize(self, timers: List[Timer]):
        # TODO make this do something
        pass


@dataclasses.dataclass  # type: ignore
class PostWriter(Writer):
    """
    A writer that posts json Timer data to a specified web address.

    Inputs:
    post_address: the full URI of the end point to which json should be posted.
    """

    post_address: str
    serializer: Callable = json.dumps

    def finalize(self, timers: List[Timer]):
        serialized = self.serializer([dataclasses.asdict(t) for t in timers])
        requests.post(self.post_address, json=serialized)
