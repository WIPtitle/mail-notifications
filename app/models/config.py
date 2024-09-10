from sqlmodel import SQLModel


class Config(SQLModel):
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    email_from: str

class ConfigResponse(SQLModel):
    smtp_server: str
    smtp_port: int
    smtp_user: str
    email_from: str