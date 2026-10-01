import pytest
from models.request_models import AssetTemplateRequest
from models.response_models import AssetTemplateResponse

@pytest.mark.api
class TestAssetTemplateAPI:

        # Funtion to validate the health check endpoint of the API
    def test_health_check_returns_ok(self, asset_client):
        # Arrange & Act
        health = asset_client.check_health()
        # Assert
        assert health.get("status") == "ok"


        # Function to validate the successful generation os an asset template
    def test_generate_asset_template_success(self, asset_client):
        # Arrange
        request_data = AssetTemplateRequest(
            equipment_name="Centrifugal Pump",
            phase_text="please generate the template now considering only the following sensors: bearing temperature, bearing vibration, flow, input pressure, output pressure, current, voltage, temp of windings, speed"
        )
        # Act
        raw_result = asset_client.generate_asset_template(request_data)
        # Assert: 
        # Validate the response generated as a asset template against the AssetTemplateResponse model
        validated_template = AssetTemplateResponse(**raw_result)
        # Validate the template name against the equipment name provided in the response
        assert validated_template.templateName == "Centrifugal Pump"
        # Validate that the template contains sensor variables
        assert len(validated_template.sensorVariables) > 0
        

