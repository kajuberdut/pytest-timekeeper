def test_hello(testdir):

    # create a temporary pytest test file
    testdir.makepyfile(
        """
        from pytest_timekeeper.utility import version

        def test_timekeeper(timekeeper):
            timer = timekeeper()
            assert timer.test_name == "test_timekeeper"

        @version(5)
        def test_version(timekeeper):
            timer = timekeeper()
            assert timer.test_version == 5
    """
    )

    # run all tests with pytest
    result = testdir.runpytest()

    # check that all tests passed
    result.assert_outcomes(passed=2)
