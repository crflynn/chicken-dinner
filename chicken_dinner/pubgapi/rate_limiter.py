"""Rate limiter class."""
from collections import deque
import logging
import time


DEFAULT_CALL_COUNT = 10
DEFAULT_CALL_WINDOW = 60
SLEEP_BUFFER = 2


class RateLimiter(object):
    """The RateLimiter class.

    This class stores a specific rate limit call/window pair as well as the
    timestamps of recent calls within the window. It can check against the
    limit and add calls to the deque of calls.
    """

    def __init__(self, calls=DEFAULT_CALL_COUNT, window=DEFAULT_CALL_WINDOW):
        """Instantiate the class."""
        self.calls = calls
        self.window = window
        self.deq = deque()

    def check(self):
        """Check the previous calls and discard calls ouside of the window."""
        if len(self.deq) >= self.calls:
            # Check calls history
            for k in range(len(self.deq)):
                # Trash the calls that are before the start of the window
                if (len(self.deq) > 0 and
                        self.deq[0] < time.time() - self.window):
                    self.deq.popleft()
                else:
                    break
        # If at the limit still, store the required wait time.
        if len(self.deq) >= self.calls:
            return self.deq[0] - (time.time() - self.window) + SLEEP_BUFFER
        else:
            return 0

    def call(self, check=True):
        """Check the deque, optionally sleep, and add a call to the window."""
        if check:
            sleep_seconds = self.check()
            if sleep_seconds > 0:
                logging.warning("Rate limiter sleeping for {} seconds.".format(
                    str(int(sleep_seconds))
                ))
                time.sleep(self.check())
        self.deq.append(time.time())
