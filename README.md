# pytest-timekeeper

A simple timer for your pytest functions.
                            
## Installation
                      
Install using pip:

```bash
pip install git+https://github.com/kajuberdut/pytest-timekeeper.git
```
                      
## Basic Usage

Here's a test showing the basic functionality:

```python

    from time import sleep

    def test_timer(timekeeper):
        timer = timekeeper() # Use the factory to make a timer.
        # You could do additional setup here before starting your timer.
        timer.start() # Starts the timer
        sleep(1) # Do the parts of your test you want to time
        timer.stop() # Stop the timer
        # Additional non-timed parts of this test would go here.
```

Timekeeper is a factory that produces timers, this allows it to play nicely with tests that run multiple times such as tests that have parameterized fixtures or tests using Hypothesis to generate test data.

The name of the calling function, and it's start and stop times, any notes you add, and optional system information, are stored in the timer to be written to the configured writer(s) the end of all tests. To customize this see [Customizing Output](#customizing-output)

## Multiple Timers, annotated times, and test versions.

Multiple timers in a single function are supported. Use the timer.note dictionary to annotate the purpose of each timer:

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

The note dictionary is also a good place to store data that might help you decide in later analysis why an instance of a test was slow such as the @given values when using Hypothesis.

The version wrapper is a utility function to help keep track of when your tests change. This helps isolate changes in performance that occur due to your tests being changed from those changes that occur in the underlying app being tested.



## Customizing Output

After all tests complete pytest_timekeeper calls the finalize() method of any Writer object(s) that have been added through hooks in conftest.py.
By defaults a writer is set to output to the pytest summary report. However, pytest_timekeeper has several built-in writers and supports you writing your own.

Here is an example of using the built in PostWriter to post results as json to a web address.

```python
from pytest_timekeeper.writers import PostWriter


def pytest_timekeeper_add_writer():
    poster = PostWriter(post_address="http://localhost")
    return poster
```

You can also create your own Writer by subclassing pytest_timekeeper.Writer:

**Note:** pytest_timekeeper_set_writer overwrites the default writer while pytest_timekeeper_add_writer adds additional writers called after the default (or last set writer).

```python
from pytest_timekeeper import Writer, set_writer


def pytest_timekeeper_set_writer():
    class PrintWriter(Writer):
        def finalize(self, timers: List[Timer]):
            for t in timers:
                print(t)

    writer = PrintWriter()
    return writer

```

Now run pytest with the -s flag and you will see the timer results of your tests printed to STDOUT.


## Running tests on pytest_timekeeper

Pipenv is reccomended

```bash
git clone https://github.com/kajuberdut/pytest-timekeeper.git
pipenv install --dev
pipenv shell
pip install -e .
pytest
```