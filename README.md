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