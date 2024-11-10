from sqlmodel import SQLModel


class NtfyCredentials(SQLModel):
    user: str
    password: str
    topic: str
    url: str

    def __init__(self, user: str, password: str, topic: str, url: str):
        self.user = user
        self.password = password
        self.topic = topic
        self.url = url
