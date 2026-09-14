import pytest
from models.user import UserPayload, UserResponse

class TestUsers:

    @pytest.mark.smoke
    def test_create_user_success(self, user_service):
        # Arrange
        payload = UserPayload(name="Jeanette", job="Quality Engineer")

        # Act
        response = user_service.create_user(payload)

        # Assert
        assert response.status_code == 201, f"Se esperaba 201 pero fue {response.status_code}"
        
        user_data = UserResponse(**response.json())
        assert user_data.name == payload.name
        assert user_data.job == payload.job
        assert user_data.id is not None