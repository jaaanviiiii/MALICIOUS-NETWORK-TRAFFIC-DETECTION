"""
Network Flow Prediction and Real-Time Inference Module
Machine Learning Pipeline - Prediction & Evaluation

Features:
- Single-flow prediction with risk confidence scoring
- Dual-mode prediction: Binary Threat Status (Safe/Malicious) & Multiclass Attack Classification
- Batch CSV inference with summary reporting
- Multi-model support (Random Forest, Decision Tree, Logistic Regression, Naive Bayes, SVM)
- Robust feature validation, infinite value suppression, and standard scaling
- Built-in benchmark self-test to verify working ML models
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Union

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "dataset", "processed", "cicids2017_cleaned_sample.csv")


class NetworkFlowPredictor:
    def __init__(self, model_name: str = "best_model.joblib"):
        """
        Initializes the inference engine by loading the specified trained model,
        feature scaler, and selected feature schema.
        Also loads multiclass classifier if available for attack family classification.
        """
        self.model_name = model_name
        self.model_path = os.path.join(MODELS_DIR, model_name)
        self.scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
        self.features_path = os.path.join(MODELS_DIR, "selected_features.json")
        self.multiclass_path = os.path.join(MODELS_DIR, "multiclass_rf.joblib")
        self.label_encoder_path = os.path.join(MODELS_DIR, "label_encoder.joblib")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}. Train models first.")
        if not os.path.exists(self.features_path):
            raise FileNotFoundError(f"Feature list not found at: {self.features_path}.")
        if not os.path.exists(self.scaler_path):
            raise FileNotFoundError(f"Scaler not found at: {self.scaler_path}.")

        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        with open(self.features_path, "r") as f:
            self.feature_names = json.load(f)

        # Optional multiclass model
        self.multiclass_model = None
        self.label_encoder = None
        if os.path.exists(self.multiclass_path) and os.path.exists(self.label_encoder_path):
            try:
                self.multiclass_model = joblib.load(self.multiclass_path)
                self.label_encoder = joblib.load(self.label_encoder_path)
            except Exception as e:
                print(f"[Warning] Could not load multiclass model: {e}")

        # Check if the loaded model requires scaled inputs (e.g., Logistic Regression, SVM, KNN)
        self.requires_scaling = any(k in model_name.lower() for k in ["logistic", "naive", "knn", "svm"])
        print(f"[Predictor Initialized] Model: {model_name} | Scaling Required: {self.requires_scaling} | Expected Features: {len(self.feature_names)}")

    def _prepare_input_df(self, flow_dict: Dict[str, Any]) -> pd.DataFrame:
        """Aligns incoming dictionary keys to the trained feature schema and validates numbers."""
        row = {}
        for feature in self.feature_names:
            # Check direct match or stripped match
            val = flow_dict.get(feature, flow_dict.get(feature.strip(), 0.0))
            try:
                fval = float(val) if val is not None else 0.0
                if np.isnan(fval) or np.isinf(fval):
                    fval = 0.0
                row[feature] = fval
            except (ValueError, TypeError):
                row[feature] = 0.0
        return pd.DataFrame([row], columns=self.feature_names)

    def predict_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts whether a single network flow is BENIGN or MALICIOUS.
        If malicious, also predicts the specific attack category via multiclass model.
        Returns prediction label, probability, risk level, and contributing factors.
        """
        df_input = self._prepare_input_df(flow_data)

        if self.requires_scaling:
            X_input = self.scaler.transform(df_input)
        else:
            X_input = df_input

        # Make binary prediction
        pred_class = int(self.model.predict(X_input)[0])
        label = "MALICIOUS" if pred_class == 1 else "BENIGN"

        # Probability estimate
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_input)[0]
            prob_benign = float(probs[0])
            prob_malicious = float(probs[1]) if len(probs) > 1 else float(1.0 - probs[0])
        elif hasattr(self.model, "decision_function"):
            score = float(self.model.decision_function(X_input)[0])
            # Sigmoid conversion for SVM margin score
            prob_malicious = float(1.0 / (1.0 + np.exp(-score)))
            prob_benign = 1.0 - prob_malicious
        else:
            prob_malicious = 1.0 if pred_class == 1 else 0.0
            prob_benign = 1.0 - prob_malicious

        # Threat severity level
        if prob_malicious < 0.20:
            threat_level = "SAFE"
            severity = "Low"
        elif prob_malicious < 0.60:
            threat_level = "SUSPICIOUS"
            severity = "Medium"
        elif prob_malicious < 0.85:
            threat_level = "MALICIOUS"
            severity = "High"
        else:
            threat_level = "CRITICAL THREAT"
            severity = "Critical"

        # Predict specific attack category if multiclass model is available
        attack_category = "BENIGN"
        if pred_class == 1 and self.multiclass_model is not None and self.label_encoder is not None:
            try:
                cat_idx = int(self.multiclass_model.predict(df_input)[0])
                predicted_cat = self.label_encoder.classes_[cat_idx]
                attack_category = predicted_cat if predicted_cat != "BENIGN" else "Malicious (General)"
            except Exception:
                attack_category = "Malicious Flow"
        elif pred_class == 0:
            attack_category = "BENIGN"

        # Highlight key contributing features
        top_indicators = {}
        key_signals = [
            "Destination Port",
            "Flow Duration",
            "Total Fwd Packets",
            "Total Length of Fwd Packets",
            "Flow Bytes/s",
            "Flow Packets/s",
            "SYN Flag Count",
            "ACK Flag Count",
            "Init_Win_bytes_forward"
        ]
        for sig in key_signals:
            if sig in df_input.columns:
                top_indicators[sig] = df_input[sig].iloc[0]

        return {
            "prediction": label,
            "is_malicious": bool(pred_class == 1),
            "attack_category": attack_category,
            "threat_level": threat_level,
            "severity": severity,
            "confidence_score": round(prob_malicious if pred_class == 1 else prob_benign, 4),
            "probability_malicious": round(prob_malicious, 4),
            "probability_benign": round(prob_benign, 4),
            "key_flow_indicators": top_indicators,
            "model_used": self.model_name
        }

    def predict_batch(self, df_or_csv: Union[pd.DataFrame, str], max_rows: int = 500) -> Dict[str, Any]:
        """Runs batch prediction on a pandas DataFrame or CSV filepath."""
        if isinstance(df_or_csv, str):
            df = pd.read_csv(df_or_csv, nrows=max_rows)
        else:
            df = df_or_csv.head(max_rows).copy()

        df.columns = df.columns.str.strip()
        aligned_rows = []
        for _, row in df.iterrows():
            aligned_rows.append(self._prepare_input_df(row.to_dict()).iloc[0])

        X_batch_df = pd.DataFrame(aligned_rows, columns=self.feature_names)
        X_batch = self.scaler.transform(X_batch_df) if self.requires_scaling else X_batch_df

        preds = self.model.predict(X_batch)
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_batch)
            malicious_probs = probs[:, 1]
        elif hasattr(self.model, "decision_function"):
            scores = self.model.decision_function(X_batch)
            malicious_probs = 1.0 / (1.0 + np.exp(-scores))
        else:
            malicious_probs = (preds == 1).astype(float)

        results = []
        for i in range(len(preds)):
            results.append({
                "index": i,
                "prediction": "MALICIOUS" if preds[i] == 1 else "BENIGN",
                "is_malicious": bool(preds[i] == 1),
                "malicious_probability": round(float(malicious_probs[i]), 4)
            })

        summary = {
            "total_evaluated": len(preds),
            "total_benign": int((preds == 0).sum()),
            "total_malicious": int((preds == 1).sum()),
            "malicious_ratio_percent": round(float((preds == 1).mean() * 100), 2),
            "results_sample": results[:10]
        }
        return summary


def run_benchmark_verification():
    """Extracts actual verified flows from the dataset and tests the predictor."""
    print("=" * 70)
    print("RUNNING INFERENCE PIPELINE VERIFICATION")
    print("=" * 70)

    predictor = NetworkFlowPredictor(model_name="best_model.joblib")

    if not os.path.exists(PROCESSED_DATA_PATH):
        print("Processed dataset not found for sample extraction.")
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    sample_benign = df[df["Is_Malicious"] == 0].iloc[0].to_dict()
    sample_malicious = df[df["Is_Malicious"] == 1].iloc[0].to_dict()

    print("\n--- Test Vector 1: Ground Truth BENIGN Flow ---")
    res1 = predictor.predict_flow(sample_benign)
    print(json.dumps(res1, indent=2))

    print("\n--- Test Vector 2: Ground Truth MALICIOUS Flow ---")
    res2 = predictor.predict_flow(sample_malicious)
    print(json.dumps(res2, indent=2))

    print("\n--- Test Vector 3: SVM Predictor Test ---")
    svm_predictor = NetworkFlowPredictor(model_name="svm.joblib")
    res_svm = svm_predictor.predict_flow(sample_malicious)
    print(json.dumps(res_svm, indent=2))

    print("\nAll predictor tests executed with 100% real ML models!")


if __name__ == "__main__":
    run_benchmark_verification()
