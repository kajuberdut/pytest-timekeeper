from typing import List

import pytest

import dataclasses
from pytest_timekeeper.timer import Timer
from pytest_timekeeper.writers import Writer

from pytest_timekeeper import get_writer


@dataclasses.dataclass
class TimeKeeper:
    writer: Writer = dataclasses.field(default_factory=get_writer)
    timers: List[Timer] = dataclasses.field(default_factory=list)

    def get_timer(self, test_name, test_version):
        timer = Timer(test_name=test_name, test_version=test_version)
        self.timers.append(timer)
        return timer

    def finalize(self):
        self.writer.finalize(self.timers)


@pytest.yield_fixture(scope="session")
def keeper():
    k = TimeKeeper()
    yield k
    k.finalize()


@pytest.fixture(scope="function")
def timekeeper(keeper, request):
    f = request.function

    def get_timer():
        if not hasattr(f, "_version"):
            f._version = 0
        return keeper.get_timer(test_name=f.__name__, test_version=f._version)

    return get_timer
