from pytest_timekeeper.writers import JsonWriter

pytest_plugins = ["pytester"]


def pytest_timekeeper_add_writer():
    reporter = JsonWriter()
    return reporter
