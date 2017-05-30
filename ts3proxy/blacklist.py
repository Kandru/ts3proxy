import os

from .watchdog import watchdog

"""blacklist class

class for blacklisting or whitelisting IP addresses
"""


class blacklist:

    def __init__(self, blacklist_file, whitelist_file):
        self.blacklist = []
        self.whitelist = []
        self.blacklist_file = blacklist_file
        self.whitelist_file = whitelist_file
        self.create(self.blacklist_file)
        self.create(self.whitelist_file)
        self.whitelist_file_wd = watchdog(self.whitelist_file)
        self.blacklist_file_wd = watchdog(self.blacklist_file)

    def check(self, IP):
        self.watch()
        if len(self.whitelist) > 0:
            if IP in self.whitelist:
                return True
            else:
                return False
        else:
            if IP in self.blacklist:
                return False
            else:
                return True

    def watch(self):
        if self.whitelist_file_wd.watch():
            with open(self.whitelist_file, 'r') as file:
                self.whitelist = []
                for line in file:
                    self.whitelist.append(line.strip())
        if self.blacklist_file_wd.watch():
            with open(self.blacklist_file, 'r') as file:
                self.blacklist = []
                for line in file:
                    self.blacklist.append(line.strip())

    def create(self, file, times=None):
        with open(file, 'a'):
            os.utime(file, times)
