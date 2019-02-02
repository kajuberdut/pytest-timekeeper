def pytest_timekeeper_set_writer():
    """
    Replace the default writer for final output by over-writing this hook in your conftest.py:

        from pytest_timekeeper.writers import Writer
        def pytest_timekeeper_set_writer():
            class PrintWriter(Writer):
                def finalize(self, timers: List[Timer]):
                    for t in timers:
                        print(t)

            writer = PrintWriter()
            return writer
    """
    pass


pytest_timekeeper_set_writer.firstresult = True  # type: ignore


def pytest_timekeeper_add_writer():
    """
    Add a writer for final output by including this hook in conftest.py:

        from pytest_timekeeper.writers import Writer
        def pytest_timekeeper_add_writer():
            class PrintWriter(Writer):
                def finalize(self, timers: List[Timer]):
                    for t in timers:
                        print(t)

            writer = PrintWriter()
            return writer
    """
    pass


def pytest_timekeeper_set_monitor():
    """
    Override the system monitor to track system utilization:
        def pytest_timekeeper_add_monitor():
            return Monitor
    """
    pass


pytest_timekeeper_set_monitor.firstresult = True  # type: ignore
