from fastapi.testclient import TestClient
from sirius.main import app

client = TestClient(app)

def test_post_get_compounds():
    # sample payload for post request
    # TODO: fix the format of the payload with new MSMS fields
    payload = {
        "msms": {
            "ion1": 1,
            "ion2": 2,
            "ion3": 3
        },
        "pcm": {
            "pre_cursor_mass": 50
        }
    }

    response = client.post("/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10
    assert all(isinstance(item, str) for item in data)
