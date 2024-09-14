import os
from typing import List
from sqlmodel import SQLModel
import httpx


class UserResponse(SQLModel):
    id: int
    email: str
    permissions: List[str]


class AuthClient:
    def __init__(self):
        self.auth_hostname = os.getenv("AUTH_HOSTNAME")


    async def get_all_users(self):
        url = f"http://{self.auth_hostname}:8000/users/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            users = response.json()
            return [UserResponse(**user) for user in users]