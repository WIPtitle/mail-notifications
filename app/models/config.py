from sqlmodel import SQLModel, Field


class Config(SQLModel, table=True):
    alarm_topic: str = Field(primary_key=True)
