import uvicorn
import tempfile
import subprocess
import os
import csv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


app = FastAPI()

class PCM(BaseModel):
    pre_cursor_mass: float

class Peak(BaseModel):
    mz: float # m/z mass to charge ratio
    intensity: int # intensity

class MSMS(BaseModel):
    peaks: List[Peak] # list of peaks, each with mz and intensity

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# takes in an msms value represented as a string and parses it into MSMS data type
def parse_msms_string(msms_str: str) -> MSMS:
    temp_peaks: List[Peak] = []
    for pair in msms_str.strip().split():
        mz_str, intensity_str = pair.split(":")
        peak = Peak(mz=float(mz_str), intensity=int(float(intensity_str)))
        temp_peaks.append(peak)
    return MSMS(peaks=temp_peaks)

# takes in MSMS and PCM and creates a temporary MGF file to be passed to the sirius CLI command as input
# returns the file path of that MGF file as a string
def create_mgf_file(msms: MSMS, pcm: PCM) -> str:
    mgf_content = ["BEGIN IONS"]
    mgf_content.append(f"PEPMASS={pcm.pre_cursor_mass}")
    for peak in msms.peaks:
        mgf_content.append(f"{peak.mz}, {peak.intensity}")
    mgf_content.append("END IONS")
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mgf", delete=False) as tmpMGF:
        tmpMGF.write("\n".join(mgf_content))
        return tmpMGF.name # returns the path of the temporary MGF file as a string

# takes in the MGF file as argument, as well as output and summary directory, returns a formula_candidates.tsv file in summary dir
# probably hardcode the output and summary directories on the database:
# def run_sirius_CLI(mgf_file_path: str) -> str:
def run_sirius_CLI(mgf_file_path: str, output_dir: str, summary_dir: str) -> str:
    command = [
        "sirius",
        "--input", mgf_file_path,
        "--output", output_dir,
        "formula",
        "-p", "orbitrap",
        "fingerprint",
        "structure",
        "compound-classes",
        "write-summaries",
        "--output", summary_dir
    ]

    subprocess.run(command, check=True)

    os.remove(mgf_file_path) # delete temporary MGF file as it is no longer needed after being passed to sirius command
    return f"{summary_dir}/...TODO" # TODO, how do we get the filepath of the formula_candidates.tsv file

# takes in the formula_candidates.tsv file and parses them into a list of strings
def parse_sirius_output(formula_candidates_file: str) -> list[str]:
    #TODO 
    pass

# a post request taking in MSMS and PCM, returning a list of the 10 most probable elements in order of probability
# responce as a JSON
@app.post("/")
def get_compounds(msms_str: str, pcm_str: str) -> list[str]:
    #TODO
    msms = parse_msms_string(msms_str)
    pcm = PCM(pre_cursor_mass=float(pcm_str))
    mgf = create_mgf_file(msms, pcm)
    candidates = run_sirius_CLI(mgf)
    topten = parse_sirius_output(candidates)
    return topten

    dummy_compounds = [
        "H2O", "CO2", "H2", "O2", "H2SO4",
        "NaCl", "CH4", "C2H6", "C3H8", "KCl"
    ]
    # implement use of sirius here to get the elements
    return dummy_compounds

if __name__ == "__main__":
    uvicorn.run("main:app", port=80, log_level="info")
    