class Notification:
    def __init__(self, title: str, priority: str, message: str = None, file: bytes = None):
        self.title = title
        self.priority = priority
        self.file = file
        self.message = message
