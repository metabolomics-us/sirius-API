import requests
# these tests are conducted on the live API

def test_valid_post_200():
    # Arbitrary test data:
    msms_str = "189.48956:1.9 283.62076:3.4 301.22977:66.3 311.08008:1.3 399.99106:2.3"
    pcm_str = "413.26611887841"
    charge = True

    url = "https://sirius.metabolomics.us/formulas"
    payload = {
        "msms_str": msms_str,
        "pcm_str": pcm_str,
        "charge": charge
    }

    response = requests.post(url, json=payload)

    # HTTP response code should be 200 - OK
    assert response.status_code == 200

    data = response.json()
    # asser format of our return object is as expected
    assert isinstance(data, dict)
    assert "formulas" in data
    assert "sirius_scores" in data
    assert "adducts" in data
    assert "precursor_formulas" in data

    # type assertions of each element in our lists
    assert all(isinstance(formula, str) for formula in data["formulas"])
    assert all(isinstance(score, float) for score in data["sirius_scores"])
    assert all(isinstance(adduct, str) for adduct in data["adducts"])
    assert all(isinstance(pcf, str) for pcf in data["precursor_formulas"])

 
def test_invalid_PCM_input():
    # Arbitrary test data:
    msms_str = "189.48956:1.9 283.62076:3.4 301.22977:66.3 311.08008:1.3 399.99106:2.3"
    pcm_str = "chararacters"
    charge = True

    url = "https://sirius.metabolomics.us/formulas"
    payload = {
        "msms_str": msms_str,
        "pcm_str": pcm_str,
        "charge": charge
    }

    response = requests.post(url, json=payload)

    # HTTP response code should be 400 - client error
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid precursor mass format. Expected a number."
    


def test_invalid_MSMS_input():
    # Arbitrary test data:
    msms_str = "characters for example"
    pcm_str = "1.0"
    charge = False

    url = "https://sirius.metabolomics.us/formulas"
    payload = {
        "msms_str": msms_str,
        "pcm_str": pcm_str,
        "charge": charge
    }

    response = requests.post(url, json=payload)
    # HTTP response code should be 400 - client error
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid MSMS format. Expected 'mz:intensity' number pairs."



def test_empty_MSMS_input():
    # Arbitrary test data:
    msms_str = ""
    pcm_str = "1.0"
    charge = False

    url = "https://sirius.metabolomics.us/formulas"
    payload = {
        "msms_str": msms_str,
        "pcm_str": pcm_str,
        "charge": charge
    }

    response = requests.post(url, json=payload)
    # HTTP response code should be 400 - client error
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid MSMS. Cannot be empty."