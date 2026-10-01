import pytest
from services.asset_template_client import AssetTemplateClient

@pytest.fixture
def asset_client():
    return AssetTemplateClient()