# pytest-timekeeper

A simple timer for your pytest functions.
                            
## Installation
                      
Install using pip:

```bash
pip install git+https://github.com/kajuberdut/pytest-timekeeper.git
```

Enable the fixture explicitly in your tests or conftest.py (not required when using setuptools entry points):

```python
    pytest_plugins = ['pytest_timekeeper']
```
                      
## Basic Usage

Here's a test showing the basic functionality:

```python

    import time

    def test_timer(timekeeper):
        timer = timekeeper() # Use the factory to make a timer.
        # You could do additional setup here before starting your timer.
        timer.start() # Starts the timer
        time.sleep(1) # Do the parts of your test you want to time
        timer.stop() # Stop the timer
        # Additional non-timed parts of this test would go here.
```

Because timekeeper is a factory that produces timers, it will play nice with tests that run multiple times such as tests that have parameterized fixtures or tests using Hypothesis to generate test data.

The name of the calling functin and it's start and stop times will be written to a .json file at the end of all tests.

## Multiple Timers, annotated times, and test versions.

Multiple timers are not problem:

```python

    import time
    from pytest_timekeeper.utility import version

    @version(2)
    def test_timer(timekeeper):
        outer_timer = timekeeper() # This timer times the entire setup and teardown.
        inner_timer = timekeeper() # This timer times a single function.
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
```

The note dictionary is also a good place to store data that may inform why a particular test was slow such as the @given values from Hypothesis.

The version wrapper is a utility function to help keep track of when your tests change. This helps isolate changes in performance that occur due to your tests being changes vs. those that occur from changes in the underlying app being tested.


## Running tests on pytest_timekeeper

Pipenv is reccomended

```bash
git clone https://github.com/kajuberdut/pytest-timekeeper.git
pipenv install --dev
pipenv shell
pip install -e .
pytest
```