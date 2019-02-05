from pytest_timekeeper.writers import PostWriter

pytest_plugins = ["pytester"]


def pytest_timekeeper_add_writer():
    reporter = PostWriter(
        base_url="https://ptsv2.com/t/timer",
        test_times_path="post",
        sys_info_path="post",
        state_history_path="post",
    )
    return reporter
