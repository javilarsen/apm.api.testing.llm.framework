import pytest
import json
from models.request_models import AssetTemplateRequest
from models.response_models.asset_template import asset_template

# fixture to create an asset template
@pytest.fixture
def raw_asset_template_data(asset_client):
    equipment_name = "Motor"
    phase_text = ""
    
    request_data = AssetTemplateRequest(
        equipment_name=equipment_name,
        phase_text=phase_text
    )
    raw_result = asset_client.generate_asset_template(request_data)
    
    return {
        "raw_result": raw_result
    }

@pytest.mark.api
class TestDeterministic:

# test to verify that the asset template contains all expected fields
    def test_raw_result_contains_all_template_fields(self, raw_asset_template_data):
        # Arrange
        raw_result = raw_asset_template_data["raw_result"]
        
        if isinstance(raw_result, str):
            raw_result = json.loads(raw_result)
        
        assert isinstance(raw_result, dict), "raw_result debe ser un diccionario"
        
        # Call asset_template to get the expected fields
        expected_fields = asset_template.model_fields.keys()
        
        # Act & Assert
        missing_fields = [field for field in expected_fields if field not in raw_result]
        
        assert not missing_fields, f"there are missing fields in the asset template: {missing_fields}"