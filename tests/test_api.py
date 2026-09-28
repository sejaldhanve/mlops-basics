import io
import pytest
from PIL import Image
from app import app

@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the /health endpoint returns 200 OK and status 'ok'."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data is not None
    assert json_data.get("status") == "ok"

def test_index_route(client):
    """Test the root endpoint returns metadata and status 200."""
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data is not None
    assert "endpoints" in json_data

def test_predict_no_input(client):
    """Test /predict returns 400 when no image is provided."""
    response = client.post("/predict")
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data

def test_predict_with_image(client):
    """Test /predict returns a prediction given a valid 28x28 image."""
    img = Image.new("L", (28, 28), color=128)
    byte_io = io.BytesIO()
    img.save(byte_io, "PNG")
    byte_io.seek(0)

    data = {
        "file": (byte_io, "digit.png")
    }
    response = client.post("/predict", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data.get("status") == "success"
    assert "predicted_digit" in json_data
    assert isinstance(json_data["predicted_digit"], int)
    assert 0 <= json_data["predicted_digit"] <= 9
    assert "confidence" in json_data
