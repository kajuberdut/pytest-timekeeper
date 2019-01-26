import time
from pytest_timekeeper.utility import version


@version(2)
def test_timer(timekeeper):
    outer_timer = timekeeper()  # This timer times the entire setup and teardown.
    inner_timer = timekeeper()  # This timer times a single function.
    # timer.note is a dict which can be used to store additional information
    # timer.note is written with each timers record at the end of tests
    outer_timer.note["area"] = "Connect+Query+Close"
    inner_timer.note["area"] = "Query"
    outer_timer.start()
    print("Connect to a database")
    inner_timer.start()
    print("Query the database.")
    inner_timer.stop()
    print("Close connection.")
    outer_timer.stop()

