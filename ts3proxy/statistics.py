class Statistics:

    def __init__(self, max_users):
        self.num_users = 0
        self.max_users = max_users

    def add_user(self, addr=None):
        self.num_users += 1

    def remove_user(self, addr=None):
        self.num_users -= 1

    def user_limit_reached(self):
        if self.num_users >= self.max_users:
            return True
        else:
            return False
