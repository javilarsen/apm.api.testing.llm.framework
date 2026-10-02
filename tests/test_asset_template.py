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

        equipment_name = "Pump"
        phase_text = "please generate the template now considering only the following sensors: bearing temperature, bearing vibration, flow, input pressure, output pressure, current, voltage, temp of windings, speed"
        
        # Arrange
        request_data = AssetTemplateRequest(
            equipment_name,
            phase_text
        )

        # Act
        raw_result = asset_client.generate_asset_template(request_data)
        validated_template = AssetTemplateResponse(**raw_result)
        
        # Assert: 
        
        # Validate the response generated as a asset template against the AssetTemplateResponse model
        assert validated_template, "Template does not exist"
        
        # Validate the template name against the equipment name provided in the response
        valid_template_name = self._validate_template_name(validated_template, equipment_name)
        assert valid_template_name, "Template name does not match the equipment name"
       
        # Validate that the template contains sensor variables
        sensors_exist = self._validate_sensor_variables(validated_template)
        assert sensors_exist, "Template does not contain any sensor variables"
        
        # Validate that the template contains failure modes
        failure_modes_exist = self._validate_failure_modes_generated(validated_template)
        assert failure_modes_exist, "Template does not contain any failure modes"

        # Validate that there are no duplicate sensor variables
        no_duplicates_sensor = self._validate_no_duplicates_in_sensor_variables(validated_template)
        assert no_duplicates_sensor, "Template contains duplicate sensor variables"

        # Validate that RPN values are not all the same
        rpn_not_all_same = self._validate_that_RPN_are_not_the_same(validated_template)
        assert rpn_not_all_same, "All RPN values are the same"



    
    # region Validation Helper Methods

    def _validate_template_name(self, validated_template, equipment_name):
        if validated_template.templateName == equipment_name:
            return True
        return False

    def _validate_sensor_variables(self, validated_template):
        if len(validated_template.sensorVariables) > 0:
            return True
        return False

    def _validate_failure_modes_generated(self, validated_template):
        if len(validated_template.failureModes) > 0:
            return True
        return False

    def _validate_no_duplicates_in_sensor_variables(self, validated_template):
        sensor_names = [sensor.name for sensor in validated_template.sensorVariables]
        if len(sensor_names) == len(set(sensor_names)):
            return True
        return False

    def _validate_that_RPN_are_not_the_same(self, validated_template):
        rpn_values =[fm["extended"]["RPN"] for fm in validated_template.failureModes if "extended" in fm and "RPN" in fm["extended"]]
        all_same_rpn = len(set(rpn_values)) == 1
        if all_same_rpn:
            return False
        return True
    
    #endregion
    
