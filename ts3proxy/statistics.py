class Statistics:

    def __init__(self, max_users):
        self.num_users = 0
        self.max_users = max_users

    def addUser(self, addr=None):
        self.num_users += 1

    def removeUser(self, addr=None):
        self.num_users -= 1
