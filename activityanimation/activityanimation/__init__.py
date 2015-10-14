import threading
import time
import itertools
import builtins


class Spinner(object):
    def __init__(self, task="Running: ", done="Done"):
        self._task = task
        self._done = done
        self._builtin_print = builtins.print  # Store copy for restoration
        self._stop_flag = threading.Event()
        self._lock = threading.Lock()

        # spin thread declaration
        self._thread = threading.Thread(
            target=self._spin,
        )
        self._thread.deamon = True

    def __enter__(self):

        # Print function used to temporarily override the builtin print function
        # this would in most cases be dangerous however all arguments are passed
        # to print un-altered after aquiring a lock
        def _print(*args, **kwargs):
            with self._lock:
                self._clear()
                self._builtin_print(*args, **kwargs)

        builtins.print = _print  # Replace print to ensure exclusive print

        self._thread.start()
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        self._stop_flag.set()

        while self._thread.isAlive():
            time.sleep(0.1)

        builtins.print = self._builtin_print  # Restore old print function

    def _spin(self):
        sp = itertools.cycle(['-', '/', '|', '\\'])

        while (not self._stop_flag.is_set()):
            with self._lock:
                self._draw(sp.__next__())
                time.sleep(0.05)

        with self._lock:
            self._clear()
            self._builtin_print(self._task + " " + self._done)

    def _draw(self, spn):
        self._builtin_print(
            "\r" + self._task + " " + spn,
            end=""
        )

    def _clear(self):
        clear_string = "\r  "  # space for extra space and spin char
        for char in self._task:
            clear_string += " "
        clear_string += "\r"

        self._builtin_print(clear_string, end="")
