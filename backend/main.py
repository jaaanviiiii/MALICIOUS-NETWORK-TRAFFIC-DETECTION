"""
FastAPI Backend Application for Malicious Network Traffic Detection
Serves ML predictions, model benchmarking metrics, and flow analysis endpoints.
"""

import os
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.predict import NetworkFlowPredictor

app = FastAPI(
    title="Malicious Network Traffic Detection API",
    description="Machine Learning based Intrusion Detection System trained on CIC-IDS2017",
    version="1.0.0"
)

# Enable CORS for future frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "dataset", "processed", "cicids2017_cleaned_sample.csv")

# Initialize inference predictor
predictor = NetworkFlowPredictor(model_name="best_model.joblib")


class FlowInput(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        example={
            "Destination Port": 80,
            "Flow Duration": 120000,
            "Total Fwd Packets": 4,
            "Total Backward Packets": 2,
            "Flow Bytes/s": 450.5,
            "Flow Packets/s": 12.0
        }
    )
    model_name: Optional[str] = "best_model.joblib"


@app.get("/health")
def health_check():
    """Returns system status, active ML model, and feature count."""
    return {
        "status": "healthy",
        "active_model": predictor.model_name,
        "feature_count": len(predictor.feature_names),
        "available_models": [
            "best_model.joblib (Random Forest Ensemble)",
            "svm.joblib (Support Vector Machine)",
            "decision_tree.joblib (Decision Tree CART)",
            "knn.joblib (K-Nearest Neighbors)",
            "logistic_regression.joblib (Logistic Regression)",
            "naive_bayes.joblib (Gaussian Naive Bayes)",
            "multiclass_rf.joblib (Multiclass Random Forest - 8 Attack Categories)"
        ]
    }


@app.get("/models/metrics")
def get_model_metrics():
    """Returns evaluation metrics and benchmark comparisons for all trained models."""
    metrics_path = os.path.join(REPORTS_DIR, "evaluation_metrics.json")
    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail="Evaluation metrics file not found.")
    
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    return metrics


@app.get("/models/features")
def get_features():
    """Returns the list of 69 network flow features used by the models."""
    return {
        "count": len(predictor.feature_names),
        "features": predictor.feature_names
    }


@app.get("/models/sample-vectors")
def get_sample_vectors():
    """Provides genuine sample flows from the CIC-IDS2017 dataset for instant testing."""
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise HTTPException(status_code=404, detail="Processed dataset not found.")

    df = pd.read_csv(PROCESSED_DATA_PATH)
    sample_benign = df[df["Is_Malicious"] == 0].iloc[0].to_dict()
    sample_malicious = df[df["Is_Malicious"] == 1].iloc[0].to_dict()

    # Clean target columns from sample features
    for col in ["Clean_Label", "Attack_Category", "Is_Malicious"]:
        sample_benign.pop(col, None)
        sample_malicious.pop(col, None)

    return {
        "benign_sample": sample_benign,
        "malicious_sample": sample_malicious
    }


@app.post("/predict")
def predict_single_flow(payload: FlowInput):
    """Predicts threat status for an individual network flow vector."""
    try:
        # If user requests a different model than the default
        if payload.model_name and payload.model_name != predictor.model_name:
            custom_predictor = NetworkFlowPredictor(model_name=payload.model_name)
            result = custom_predictor.predict_flow(payload.features)
        else:
            result = predictor.predict_flow(payload.features)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch_csv(file: UploadFile = File(...)):
    """Accepts a CSV of network flows and predicts each row."""
    try:
        df = pd.read_csv(file.file, nrows=300)
        batch_results = predictor.predict_batch(df, max_rows=300)
        return batch_results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
