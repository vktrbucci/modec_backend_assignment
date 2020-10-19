import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestVessel:
    def test_vessel(self):
        obj = mixer.blend('equipment_manager.Vessel')
        assert 'MV' in obj.code, 'Should create a Vessel instance'