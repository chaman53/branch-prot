from fastapi import FastAPI
from pydantic import BaseModel

from app.config import *
from app.multi_summarizer.multi_summarizer import generate_multi_summarizer
from app.table_summary_intro_and_title.table_summary_intro_and_title import generate_table_summary_intro_and_title

class HealthCheckOutputData(BaseModel):
    health_check: str

class InputProjectIdDataModel(BaseModel):
    project_id: int

class OutputData(BaseModel):
    successful: int

app = FastAPI()

@app.get("/", response_model=HealthCheckOutputData)
async def home():
    return {"health_check": "OK"}


@app.post("/multi_summarizer", response_model=OutputData)
def get_multi_summarizer(input_data: InputProjectIdDataModel):
    _id = generate_multi_summarizer(input_data.project_id)
    return {"successful": _id}


@app.post("/get_table_summary_intro_and_title", response_model=OutputData)
def get_table_summary_intro_and_title(input_data: InputProjectIdDataModel):
    _id = generate_table_summary_intro_and_title(input_data.project_id)
    return {"successful": _id}
