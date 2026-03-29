from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from adk_models.agent import read_csv_file, clean_csv_file

app = FastAPI(
    title="ModelMint CSV Cleaner API",
    description="API to read, analyze, and clean CSV files",
    version="1.0.0"
)

# Request models
class ReadCSVRequest(BaseModel):
    file_path: str

class CleanCSVRequest(BaseModel):
    file_path: str
    output_path: str

# Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "csv_cleaner_agent"}

@app.post("/read-csv")
async def read_csv(request: ReadCSVRequest):
    """
    Read and analyze a CSV file.
    Returns column info, row count, missing values, and duplicate count.
    """
    result = read_csv_file(request.file_path)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return {"status": "success", "data": result}

@app.post("/clean-csv")
async def clean_csv(request: CleanCSVRequest):
    """
    Clean a CSV file by removing duplicates, handling missing values,
    and stripping whitespace. Saves the cleaned file.
    Returns a summary of the cleaning process and the output file path.
    """
    result = clean_csv_file(request.file_path, request.output_path)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return {"status": "success", "data": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

