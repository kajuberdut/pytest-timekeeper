from typing import List

from pytest_timekeeper.timer import Timer
from pytest_timekeeper.writers import Writer

pytest_plugins = ["pytester"]


def pytest_timekeeper_set_writer():
    class PrintWriter(Writer):
        def finalize(self, timers: List[Timer]):
            for t in timers:
                print(t)

    writer = PrintWriter()
    return writer
