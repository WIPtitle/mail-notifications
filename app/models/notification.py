class Notification:
    def __init__(self, title: str, priority: str, url: str = None, file: bytes = None):
        self.title = title
        self.priority = priority
        self.url = url
        self.file = file
