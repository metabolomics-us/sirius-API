from fastapi.testclient import TestClient
from sirius.main import app

client = TestClient(app)

def test_post_get_compounds():
    # Arbitrary test data:
    msms_str = "189.48956:1.9 283.62076:3.4 301.22977:66.3 311.08008:1.3 399.99106:2.3"
    pcm_str = "413.26611887841"

    # post request
    response = client.post("/", params={"msms_str": msms_str, "pcm_str": pcm_str})

    # HTTP response code should be 200 OK
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(item, str) for item in data)
 