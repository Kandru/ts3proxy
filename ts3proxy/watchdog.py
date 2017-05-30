import os

"""watch class

class for watching a file
"""


class Watchdog:
    """
    Watch for changes of the file.
    """

    def __init__(self, file):
        self.file = file
        self.last_changed = 0

    def watch(self):
        try:
            timestamp = os.stat(self.file).st_mtime
            if timestamp != self.last_changed:
                self.last_changed = timestamp
                return True
            else:
                return False
        except OSError:
            return True
