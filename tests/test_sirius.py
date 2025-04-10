from fastapi.testclient import TestClient
from sirius.main import app

client = TestClient(app)

def test_post_get_compounds():
    # Arbitrary test data:
    msms_str = "55.963573:5938.000000 56.798489:6062.000000 64.927414:10277.000000 65.293808:5628.000000 67.389580:5226.000000 70.065033:18834.000000 73.024750:5421.000000 78.059624:5925.000000 84.080620:1603720.000000 88.075508:12758.000000 89.620560:5591.000000 110.096336:16728.000000 123.964256:10125.000000 128.106689:107149.000000 129.114563:180595.000000 146.059540:22846.000000 146.071335:25567.000000 146.117233:1189030.000000 147.053940:7681.000000"
    pcm_str = "23.6145"

    # post request
    response = client.post("/", params={"msms_str": msms_str, "pcm_str": pcm_str})

    # HTTP response code should be 200 OK
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10
    assert all(isinstance(item, str) for item in data)
 