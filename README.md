# python-activityanimation
A simple set of python tools to display various sorts of activity animation on
the console.

## Examples
### Spinner
The Splinner class has __enter__ and __exit__ methods and is intended to be
used with a context manager.

```python
from activityanimation import Spinner
import time

def long_running_function():
    time.sleep(2)
    print("Hello")
    time.sleep(2)
    print("I take a long time to comlete")
    time.sleep(2)

with Spinner(task="Runing big task:", done="All done"):
    long_running_function()
```
