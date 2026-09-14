import requests
from services.base_client import BaseClient
from models.user import UserPayload

class UserService(BaseClient):
    def __init__(self):
        super().__init__()
        self.ENDPOINT = "/users"

    def create_user(self, payload: UserPayload) -> requests.Response:
        return self.post(self.ENDPOINT, json=payload.model_dump())