import pytest

from pytest_timekeeper.keeper import TimeKeeper
from pytest_timekeeper.monitor import Monitor
from pytest_timekeeper.writers import PytestReport
from pytest_timekeeper import hookspec


@pytest.mark.tryfirst
def pytest_configure(config):
    config._timekeeper = TimeKeeper(config)


def pytest_sessionstart(session):
    session.config._timekeeper.start_monitor()


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session, exitstatus):
    session.config._timekeeper.finalize()
    yield


def pytest_addhooks(pluginmanager):

    method = getattr(pluginmanager, "add_hookspecs", None)
    if method is None:
        method = pluginmanager.addhooks
    method(hookspec)


def pytest_timekeeper_set_writer():
    writer = PytestReport()
    return writer


def pytest_timekeeper_set_monitor():
    monitor = Monitor()
    return monitor


@pytest.fixture(scope="function")
def timekeeper(request):
    f = request.function
    keeper = request.config._timekeeper

    def get_timer():
        if not hasattr(f, "_version"):
            f._version = 0
        return keeper.get_timer(test_name=f.__name__, test_version=f._version)

    return get_timer
