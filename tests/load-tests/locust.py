import logging
import csv
import random

from locust import HttpUser, task, between

class apiUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        file = "testdata.csv"
        logging.info("Reading data from testdata.csv")
        with open(file, "r") as f:
            reader = csv.DictReader(f)
            self.lines = list(reader)

    @task
    def formulas(self):
        line = random.choice(self.lines)
        pcm = line["pre_cursors_mass"]
        msms = line["msms"]
        charge_str = line["ion_mode"]
        # convert charge string to boolean
        if charge_str == "POSITIVE":
            charge = 1
        else:
            charge = 0

        # create JSON payload
        payload = {
            "pcm_str": pcm,
            "msms_str": msms,
            "charge": charge
        }
                
        logging.debug(f"Performing formula prediction with PCM: {pcm}, MSMS: {msms}, Charge: {charge}")
        with self.client.post(f"/formulas", json=payload, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed with status {response.status_code}: {response.text}")
