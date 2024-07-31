import pytest
from app import app
from app.config import FW_VERSION


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_version(client):
    response = client.get('/version.txt', headers={'br_mac': '00:11:22:33:44:55', 'br_fwv': 'v1.0.0'})
    assert response.status_code == 200
    assert FW_VERSION in response.data.decode()


def test_firmware(client):
    response = client.get('/firmware.bin', headers={'br_mac': '00:11:22:33:44:55', 'br_fwv': 'v1.0.0'})
    assert response.status_code == 200
    assert response.mimetype == 'application/octet-stream'
