import pytest
from services.user_service import UserService

@pytest.fixture
def user_service():
    return UserService()