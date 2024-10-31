from sqlmodel import SQLModel


class Notification(SQLModel):
    text: str
