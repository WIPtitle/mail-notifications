class Notification:
    def __init__(self, title: str, priority: str, file: bytes = None):
        self.title = title
        self.priority = priority
        self.file = file
