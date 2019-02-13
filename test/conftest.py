from pytest_timekeeper.writers import PostWriter

# from pytest_timekeeper.writers import JsonWriter

pytest_plugins = ["pytester"]


def pytest_timekeeper_add_writer():
    reporter = PostWriter(url="https://ptsv2.com/t/timer/post")
    return reporter


# def pytest_timekeeper_add_writer():
#     reporter = JsonWriter()
#     return reporter
