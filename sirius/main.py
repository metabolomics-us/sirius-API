import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

class MSMS(BaseModel):
    ion1: int
    ion2: int
    ion3: int

class PCM(BaseModel):
    pre_cursor_mass: float

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# a post request taking in MSMS and PCM, returning a list of the 10 most probable elements in order of probability
# respond as a JSON
@app.post("/")
def get_compounds(msms: MSMS, pcm: PCM) -> list[str]:
    dummy_compounds = [
        "H2O", "CO2", "H2", "O2", "H2SO4",
        "NaCl", "CH4", "C2H6", "C3H8", "KCl"
    ]
    # implement use of sirius here to get the elements
    return dummy_compounds

if __name__ == "__main__":
    uvicorn.run("main:app", port=80, log_level="info")
    