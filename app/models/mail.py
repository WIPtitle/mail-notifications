# Could save templates on database, maybe in the future, for now it should be enough.
from sqlmodel import SQLModel


class Mail(SQLModel):
    receiver: str
    obj: str
    text: str