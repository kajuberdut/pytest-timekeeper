import json
import time
from pathlib import Path
from typing import List

import pytest

import dataclasses
from pytest_timekeeper.timer import Timer


def time_log_name():
    p = Path().cwd() / "test" / "times"
    p.mkdir(parents=True, exist_ok=True)
    filename = f"execution_times_{time.time()}.json"
    final = p / filename
    return final


@dataclasses.dataclass
class TimeKeeper:
    filepath: str = dataclasses.field(default_factory=time_log_name)
    timers: List[Timer] = dataclasses.field(default_factory=list)

    def get_timer(self, test_name, test_version):
        timer = Timer(test_name=test_name, test_version=test_version)
        self.timers.append(timer)
        return timer

    def write_times(self):

        with open(self.filepath, "w") as fh:
            json.dump([dataclasses.asdict(t) for t in self.timers], fh)


@pytest.yield_fixture(scope="session")
def keeper():
    k = TimeKeeper()
    yield k
    k.write_times()


@pytest.fixture(scope="function")
def timekeeper(keeper, request):
    f = request.function

    def get_timer():
        if not hasattr(f, "_version"):
            f._version = 0
        return keeper.get_timer(test_name=f.__name__, test_version=f._version)

    return get_timer
