import pytest
import json
from models.request_models import AssetTemplateRequest
from models.response_models import AssetTemplateResponse

@pytest.mark.api
class TestAssetTemplateAPI:

# Region generate asset template

        # Function to generate an asset template 
    def request_asset_template(self, asset_client, equipment_name: str, phase_text: str):

        request_data = AssetTemplateRequest(
            equipment_name=equipment_name,
            phase_text=phase_text
        )
        return asset_client.generate_asset_template(request_data)

    @pytest.fixture
    def raw_asset_template_data(self, asset_client):
        equipment_name = "Motor"
        phase_text = "please generate the template now considering only the following sensors: bearing temperature, bearing vibration, flow, input pressure, output pressure, current, voltage, temp of windings, speed"
        raw_result = self.request_asset_template(asset_client, equipment_name, phase_text)
        return {
            "raw_result": raw_result,
            "equipment_name": equipment_name
            }

    @pytest.fixture
    def validated_template(self, raw_asset_template_data):
        return AssetTemplateResponse(**raw_asset_template_data["raw_result"])
    # endregion

# endregion
        
# Region Business Logic Validation

        """
        Function to validate the schema of the generated asset template
        """
    def test_generate_asset_template_success(self, raw_asset_template_data):
        # Arrange
        raw_result = raw_asset_template_data["raw_result"]
        #Act
        validate_template = AssetTemplateResponse(**raw_result)
        # Assert
        assert validate_template is not None, "The template should not be None"

        """ 
        Function to validate the template name against the equipment name provided in the response
        """
    def test_validate_asset_name(self, validated_template, raw_asset_template_data):
        # Arrange
        expected_name = raw_asset_template_data["equipment_name"]
        # Act & Assert
        assert validated_template.templateName == expected_name, "Template name does not match the equipment name"

        """
        Function to validate that the template contains sensor variables
        """
    def test_sensor_variables_exist(self, validated_template):
        # Arrange
        sensors = validated_template.sensorVariables
        # Act & Assert
        assert len (sensors) > 0, "No sensor variables found in the template"

        """
        Function to validate that the template contains failure modes
        """
    def test_failure_modes_exist(self, validated_template):
        # Arrange
        failure_modes = validated_template.failureModes
        # Act & Assert
        assert len(failure_modes) > 0, "No failure modes found in the template"

        """
        Function to validate that there are no duplicate sensor variables in the template
        """
    def test_no_duplicate_sensor_variables(self, validated_template):
        # Arrange
        sensor_names = [sensor.name for sensor in validated_template.sensorVariables]
        # Act & Assert
        assert len(sensor_names) == len(set(sensor_names)), "Duplicate sensor variables found in the template"

        """
        Function to validate that RPN values are not all the same
        """
    def test_rpn_not_all_same(self, validated_template):
        rpn_values = []
        for raw_fm in validated_template.failureModes:
            fm = self._parse_fm(raw_fm)
            rpn = fm.get("extended", {}).get("RPN")
            if rpn is not None:
                rpn_values.append(rpn)

        if rpn_values:
            assert len(set(rpn_values)) > 1, "All RPN values are the same"

    def test_rpn_values_validations(self, validated_template):
        rpn_values = []
        for raw_fm in validated_template.failureModes:
            fm = self._parse_fm(raw_fm)
            rpn = fm.get("extended", {}).get("RPN")
            if rpn is not None:
                assert 1 <= rpn <= 1000, f"RPN fuera de rango: {rpn}"
                
    def test_severity_detection_and_likelihood_ranges(self, validated_template):
        metrics = ["Severity", "Detection", "Likelihood"]
        for raw_fm in validated_template.failureModes:
            fm = self._parse_fm(raw_fm)
            extended = fm.get("extended", {})

            for metric in metrics:
                val = extended.get(metric)
                if val is not None:
                    assert 1 <= val <= 10, f"Métrica {metric} fuera de rango: {val}"
# endregion

    # region Helper Methods

    def _parse_fm(self, fm):
        if isinstance(fm, str):
            fm = json.loads(fm)
        elif hasattr(fm, "model_dump"):  # Pydantic v2
            fm = fm.model_dump()
        elif hasattr(fm, "dict"):  # Pydantic v1
            fm = fm.dict()

        if isinstance(fm, dict) and isinstance(fm.get("extended"), str):
            fm["extended"] = json.loads(fm["extended"])

        return fm if isinstance(fm, dict) else {}
    
    # endregion
    
