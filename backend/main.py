import os
import json
import pandas as pd
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.predict import NetworkFlowPredictor

app = FastAPI(title="Malicious Network Traffic Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_PATH = os.path.join(BASE_DIR, "dataset", "processed", "cicids2017_cleaned_sample.csv")

predictor = NetworkFlowPredictor(model_name="best_model.joblib")


class FlowInput(BaseModel):
    features: Dict[str, float]
    model_name: Optional[str] = "best_model.joblib"


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "active_model": predictor.model_name,
        "feature_count": len(predictor.feature_names),
        "available_models": [
            "best_model.joblib (Random Forest)",
            "svm.joblib (Support Vector Machine)",
            "decision_tree.joblib (Decision Tree)",
            "knn.joblib (K-Nearest Neighbors)",
            "logistic_regression.joblib (Logistic Regression)",
            "naive_bayes.joblib (Gaussian Naive Bayes)",
            "multiclass_rf.joblib (Multiclass Random Forest)"
        ]
    }


@app.get("/models/metrics")
def get_model_metrics():
    metrics_path = os.path.join(REPORTS_DIR, "evaluation_metrics.json")
    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail="Metrics file not found")
    with open(metrics_path, "r") as f:
        return json.load(f)


@app.get("/models/features")
def get_features():
    return {
        "count": len(predictor.feature_names),
        "features": predictor.feature_names
    }


@app.get("/models/sample-vectors")
def get_sample_vectors():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Sample dataset not found")

    df = pd.read_csv(DATA_PATH)
    benign = df[df["Is_Malicious"] == 0].iloc[0].to_dict()
    malicious = df[df["Is_Malicious"] == 1].iloc[0].to_dict()

    for col in ["Clean_Label", "Attack_Category", "Is_Malicious"]:
        benign.pop(col, None)
        malicious.pop(col, None)

    return {
        "benign_sample": benign,
        "malicious_sample": malicious
    }


@app.post("/predict")
def predict_single_flow(payload: FlowInput):
    try:
        if payload.model_name and payload.model_name != predictor.model_name:
            custom_predictor = NetworkFlowPredictor(model_name=payload.model_name)
            return custom_predictor.predict_flow(payload.features)
        return predictor.predict_flow(payload.features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch_csv(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file, nrows=300)
        return predictor.predict_batch(df, max_rows=300)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
