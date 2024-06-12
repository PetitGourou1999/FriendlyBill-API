class UserBlockedException(Exception):
    def __init__(self, message='User is blocked'):
        self.message = message
        super().__init__(self.message)