from pytest_timekeeper.writers import PostWriter

# from pytest_timekeeper.writers import JsonWriter

pytest_plugins = ["pytester"]


def pytest_timekeeper_add_writer():
    reporter = PostWriter(url="")
    return reporter


# def pytest_timekeeper_add_writer():
#     reporter = JsonWriter()
#     return reporter
