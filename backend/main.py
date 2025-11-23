from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules.repo_fetcher import RepoFetcher

app = FastAPI(title="DeadRepo Doctor API")

# Initialize repo fetcher
repo_fetcher = RepoFetcher()

class DiagnoseRequest(BaseModel):
    repo_url: str

class FetchRequest(BaseModel):
    repo_url: str

class FetchResponse(BaseModel):
    local_path: str

@app.get("/")
def root():
    return {"message": "DeadRepo Doctor API is running"}

@app.post("/api/fetch", response_model=FetchResponse)
def fetch_repository(request: FetchRequest):
    """
    Fetch a GitHub repository and return its local path.
    """
    try:
        result = repo_fetcher.fetch_repository(request.repo_url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repository: {str(e)}")

@app.post("/api/diagnose")
def diagnose(request: DiagnoseRequest):
    # Placeholder response for now
    return {
        "status": "success",
        "message": f"Diagnosis started for {request.repo_url}",
        "diagnosis_report": {}
    }
