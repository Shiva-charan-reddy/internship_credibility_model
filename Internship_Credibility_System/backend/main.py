from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import math
import os
from pathlib import Path

from model.inference import CredibilityModel
from utils.preprocessing import prepare_input_text
from utils.rules import run_hybrid_checks

app = FastAPI(title="Internship Credibility API", version="1.0.0")

# Determine the absolute path to the frontend directory
# We try multiple locations to be robust across different deployment environments
frontend_path = Path("frontend").resolve()
if not frontend_path.exists():
    # If starting from backend/ folder
    frontend_path = Path("../frontend").resolve()
if not frontend_path.exists():
    # Absolute fallback (Current File -> backend -> root -> frontend)
    frontend_path = Path(__file__).resolve().parent.parent / "frontend"

print(f"Frontend path resolved to: {frontend_path}")

# Define API routes first
@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model.is_loaded}

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the deeply learned model in memory on startup
model = CredibilityModel()

class JobPosting(BaseModel):
    job_description: str
    company_name: str = ""
    email: str = ""
    salary: str = ""
    job_link: str = ""

@app.get("/health_legacy")
def health_check_legacy():
    return {"status": "ok", "model_loaded": model.is_loaded}

# Mount static files at the root - MUST BE LAST
@app.post("/predict")
def predict_credibility(job: JobPosting):
    try:
        # 1. Base Transformer Prediction
        combined_text = prepare_input_text(
            job.job_description, job.company_name, job.email, job.salary
        )
        dl_result = model.predict(combined_text)
        dl_prob_scam = dl_result["probability"]
        
        # 2. Rule-Based Checks
        rule_result = run_hybrid_checks(
            job.job_description, job.company_name, job.email, job.job_link
        )
        
        # 3. Hybrid Confidence Calculation
        final_scam_prob = dl_prob_scam + rule_result["rule_penalty"]
        
        # If rules pass completely entirely, boost the confidence of it being legit
        if rule_result["rule_penalty"] == 0 and final_scam_prob < 0.5:
            final_scam_prob *= 0.6 # Reduces scam probability, maximizing "Legit" confidence (e.g. 95%+)

        # Aggressively boost if rules were broken / suspicious metadata found
        if rule_result["rule_penalty"] > 0:
            final_scam_prob = max(final_scam_prob, 0.85 + (rule_result["rule_penalty"] * 0.05))

        final_scam_prob = min(max(final_scam_prob, 0.01), 0.99)
             
        final_label = 1 if final_scam_prob >= 0.5 else 0
        final_confidence = math.floor(final_scam_prob * 100) if final_label == 1 else math.floor((1 - final_scam_prob) * 100)
        
        # 4. Generate structured explanation
        explanation_reasons = []
        if final_label == 1:
            explanation_reasons.extend(rule_result["reasons"])
            if dl_prob_scam > 0.6:
                explanation_reasons.append("The Deep Learning model classified the text pattern as highly similar to known scams.")
            if not explanation_reasons:
                 explanation_reasons.append("The posting structure and language raised automated flags.")
        else:
            explanation_reasons.append("No significant red flags detected in company domain, URLs, or language patterns.")
            if dl_prob_scam < 0.2:
                 explanation_reasons.append("The Deep Learning model strongly aligns this posting with legitimate jobs.")
                 
        return {
            "prediction_label": "Scam" if final_label == 1 else "Legit",
            "confidence_score": final_confidence,
            "reasons": explanation_reasons,
            "highlighted_words": rule_result["highlights"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files at the root - MUST BE LAST
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
