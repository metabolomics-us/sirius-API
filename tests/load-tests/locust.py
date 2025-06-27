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
        
        """
        # PAYLOAD THAT TAKES OVER 60 SECONDS
        pcm = "752.22614166061"
        msms = "81.070710:37.000000 85.030206:5.000000 93.015338:8.000000 97.005582:138.000000 99.071119:3.000000 99.081315:26.000000 111.019875:69.000000 115.059585:9.000000 115.079907:23.000000 133.088407:7.000000 135.015608:7.000000 135.023109:23.000000 156.980920:54.000000 159.078251:7.000000 174.992925:89.000000 176.520200:8.000000 176.528428:43.000000 176.541302:24.000000 177.068023:6376.000000 178.308946:12.000000 180.853249:4.000000 184.065161:25.000000 184.076312:25.000000 191.082850:91.000000 203.119538:17.000000 255.055187:1616.000000 255.085102:4.000000 255.682185:14.000000 273.065947:359.000000 273.080646:70.000000 286.210703:54.000000 287.083081:1184.000000 353.108513:11.000000 353.131191:78.000000 365.065421:47.000000 365.081062:5.000000 371.133401:5.000000 449.127981:1858.000000 461.709342:19.000000 463.138937:3015.000000 527.074723:7.000000 527.107673:10.000000 527.121208:63.000000 541.118076:68.000000 559.137459:94.000000 559.175553:10.000000 569.485166:92.000000 622.403960:7.000000 "
        charge = 1
        """

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
