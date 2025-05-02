import uvicorn
import tempfile
import subprocess
import os
import shutil
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()
query_lock = asyncio.Lock()

class PCM(BaseModel):
    pre_cursor_mass: float

class Peak(BaseModel):
    mz: float # m/z: mass to charge ratio
    intensity: float # intensity

class MSMS(BaseModel):
    peaks: List[Peak] # list of peaks, each with mz and intensity

# Can use this as the input payload for the post request so that post requests can be made in JSON format
class Request(BaseModel):
    msms_str: str
    pcm_str: str
    charge: bool # 1-positive, 0-negative

# And this as a return type
class ResultLists(BaseModel):
    formulas: list[str]
    sirius_scores: list[float]
    adducts: list[str]
    precursor_formulas: list[str]


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)



# takes in an msms represented as a string and parses it into MSMS object
def parse_msms_string(msms_str: str) -> MSMS:
    temp_peaks: List[Peak] = []
    for pair in msms_str.strip().split():
        try: 
            mz_str, intensity_str = pair.split(":")
            peak = Peak(mz=float(mz_str), intensity=int(float(intensity_str)))
        except (ValueError, IndexError):
            raise HTTPException(status_code=400, detail="Invalid MSMS format. Expected 'mz:intensity' number pairs.")
        temp_peaks.append(peak)

    return MSMS(peaks=temp_peaks)



# takes in MSMS and PCM objects and creates a temporary MGF file to be passed to the sirius CLI command 
# returns the file path of that MGF file as a string
def create_mgf_file(msms: MSMS, pcm: PCM, charge: bool) -> str:
    mgf_content = ["BEGIN IONS"]
    mgf_content.append(f"PEPMASS={pcm.pre_cursor_mass}")
    if charge:
        mgf_content.append(f"CHARGE=1+")
    else:
        mgf_content.append(f"CHARGE=1-")

    for peak in msms.peaks:
        mgf_content.append(f"{peak.mz} {peak.intensity}")
    mgf_content.append("END IONS")
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mgf", delete=False) as tmpMGF:
        tmpMGF.write("\n".join(mgf_content))
        return tmpMGF.name # returns the path of the temporary MGF file as a string



# takes in the MGF filepath as argument, returns formula_identifications.tsv file path
def run_sirius_CLI(mgf_file_path: str) -> str:
# if we want to change output directories, change function signature to:
# def run_sirius_CLI(mgf_file_path: str, output_dir: str, summary_dir: str) -> str:
    output_dir = "/code/query-results/sirius-output"
    summary_dir = "/code/query-results/sirius-summary"

    command = [
        "sirius",
        "--input", mgf_file_path,
        "--output", output_dir,
        "formula",
        "-p", "orbitrap",
        "fingerprint",
        "compound-classes",
        "structures",
        # "--database", "pubchem" # unsure of effect
        "write-summaries",
        "--output", summary_dir,
        "--top-k-summary=10"
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        raise HTTPException(status_code=500, detail=f"Unexpected error. The Sirius CLI command failed:   {error}")

    try:
        os.remove(mgf_file_path) # delete temporary MGF file as it is no longer needed after being passed to sirius command
    except FileNotFoundError:
        pass

    # absolute path of formulas identified tsv file, should not change (unless we take in output and summary dir as args)
    return "/code/query-results/sirius-summary/formula_identifications_top-10.tsv"



# takes in the formula_candidates.tsv file and parses it into result lists
def parse_sirius_output(formula_candidates_tsv_path: str) -> tuple[list[str], list[float], list[str], list[str]]:
    formula_list = []
    sirius_scores_list = []
    adducts_list = []
    precursor_formulas_list = []

    with open(formula_candidates_tsv_path, "r") as file:
        lines = file.readlines()
        for line in lines[1:11]: # skip header line
            values = line.strip().split("\t") # strip \n and split by tabs, list of values per line
            formula_list.append(values[1]) # values at index 1 hold molecular formula 
            sirius_scores_list.append(values[6]) # index 6 holds sirius_score
            adducts_list.append(values[2]) # index 2 holds adducts
            precursor_formulas_list.append(values[3]) # index 3 holds precursor formulas

    # remove generated files by sirius
    try:
        os.remove("/code/query-results/sirius-output.sirius")
    except FileNotFoundError:
        pass
    shutil.rmtree("/code/query-results/sirius-summary", ignore_errors=True)

    # empty lists will be handled in JS and throw appropriate error ("sirius couldn't find any matches...")
    return formula_list, sirius_scores_list, adducts_list, precursor_formulas_list



# a post request taking in MSMS and PCM (as a request object), returning a resultLists object with formulas and scores
# response as a JSON, return status code 200 (OK) if successful
@app.post("/formulas", status_code=200, response_model=ResultLists)
async def create_query(payload: Request) -> ResultLists:
    # lock so that if we have multiple requests, they wait their turn and do not cause errors
    async with query_lock:
        # if MSMS is not entered, throw error
        if not payload.msms_str:
            raise HTTPException(status_code=400, detail="Invalid MSMS. Cannot be empty.")
        msms = parse_msms_string(payload.msms_str)

        # type cast pcm as float, if it fails, throw error
        try:
            pcm = PCM(pre_cursor_mass=float(payload.pcm_str))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid precursor mass format. Expected a number.")

        mgf = create_mgf_file(msms, pcm, payload.charge)
        candidates_tsv = run_sirius_CLI(mgf)
        formula_list, sirius_scores_list, adducts_list, pcf_list = parse_sirius_output(candidates_tsv)

        return ResultLists(
            formulas=formula_list, 
            sirius_scores=sirius_scores_list, 
            adducts=adducts_list, 
            precursor_formulas=pcf_list
        )



# mount frontend HTML, CSS, and JS
app.mount("/", StaticFiles(directory="web", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", port=80, log_level="info")
    