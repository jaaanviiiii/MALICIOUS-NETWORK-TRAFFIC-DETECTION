import os
import json
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")


class NetworkFlowPredictor:
    def __init__(self, model_name: str = "best_model.joblib"):
        self.model_name = model_name
        self.model_path = os.path.join(MODELS_DIR, model_name)
        self.scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
        self.features_path = os.path.join(MODELS_DIR, "selected_features.json")
        self.multiclass_path = os.path.join(MODELS_DIR, "multiclass_rf.joblib")
        self.encoder_path = os.path.join(MODELS_DIR, "label_encoder.joblib")

        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        with open(self.features_path, "r") as f:
            self.feature_names = json.load(f)

        self.multiclass_model = None
        self.label_encoder = None
        if os.path.exists(self.multiclass_path) and os.path.exists(self.encoder_path):
            try:
                self.multiclass_model = joblib.load(self.multiclass_path)
                self.label_encoder = joblib.load(self.encoder_path)
            except Exception:
                pass

        self.requires_scaling = any(k in model_name.lower() for k in ["logistic", "naive", "knn", "svm"])

    def _prepare_input(self, flow_dict):
        row = {}
        for feature in self.feature_names:
            val = flow_dict.get(feature, flow_dict.get(feature.strip(), 0.0))
            try:
                fval = float(val) if val is not None else 0.0
                if np.isnan(fval) or np.isinf(fval):
                    fval = 0.0
                row[feature] = fval
            except (ValueError, TypeError):
                row[feature] = 0.0
        return pd.DataFrame([row], columns=self.feature_names)

    def predict_flow(self, flow_data):
        df_input = self._prepare_input(flow_data)
        X_input = self.scaler.transform(df_input) if self.requires_scaling else df_input

        pred = int(self.model.predict(X_input)[0])
        label = "MALICIOUS" if pred == 1 else "BENIGN"

        # Calculate probability
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_input)[0]
            prob_malicious = float(probs[1]) if len(probs) > 1 else float(1.0 - probs[0])
        elif hasattr(self.model, "decision_function"):
            score = float(self.model.decision_function(X_input)[0])
            prob_malicious = float(1.0 / (1.0 + np.exp(-score)))
        else:
            prob_malicious = 1.0 if pred == 1 else 0.0

        prob_benign = round(1.0 - prob_malicious, 4)
        prob_malicious = round(prob_malicious, 4)

        # Threat severity
        if prob_malicious < 0.20:
            threat_level, severity = "SAFE", "Low"
        elif prob_malicious < 0.60:
            threat_level, severity = "SUSPICIOUS", "Medium"
        elif prob_malicious < 0.85:
            threat_level, severity = "MALICIOUS", "High"
        else:
            threat_level, severity = "CRITICAL THREAT", "Critical"

        # Multiclass category for attacks
        attack_category = "BENIGN"
        if pred == 1 and self.multiclass_model and self.label_encoder:
            try:
                cat_idx = int(self.multiclass_model.predict(df_input)[0])
                predicted_cat = self.label_encoder.classes_[cat_idx]
                attack_category = predicted_cat if predicted_cat != "BENIGN" else "Malicious Flow"
            except Exception:
                attack_category = "Malicious Flow"

        # Key signals for explanation
        key_signals = ["Destination Port", "Flow Duration", "Total Fwd Packets", "Flow Bytes/s", "Flow Packets/s"]
        indicators = {k: df_input[k].iloc[0] for k in key_signals if k in df_input.columns}

        return {
            "prediction": label,
            "is_malicious": bool(pred == 1),
            "attack_category": attack_category,
            "threat_level": threat_level,
            "severity": severity,
            "confidence_score": prob_malicious if pred == 1 else prob_benign,
            "probability_malicious": prob_malicious,
            "probability_benign": prob_benign,
            "key_flow_indicators": indicators,
            "model_used": self.model_name
        }

    def predict_batch(self, df_or_csv, max_rows=300):
        if isinstance(df_or_csv, str):
            df = pd.read_csv(df_or_csv, nrows=max_rows)
        else:
            df = df_or_csv.head(max_rows).copy()

        df.columns = df.columns.str.strip()
        rows = [self._prepare_input(row.to_dict()).iloc[0] for _, row in df.iterrows()]
        X_df = pd.DataFrame(rows, columns=self.feature_names)
        X = self.scaler.transform(X_df) if self.requires_scaling else X_df

        preds = self.model.predict(X)
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)[:, 1]
        else:
            probs = (preds == 1).astype(float)

        results = []
        for i in range(len(preds)):
            results.append({
                "index": i,
                "prediction": "MALICIOUS" if preds[i] == 1 else "BENIGN",
                "is_malicious": bool(preds[i] == 1),
                "malicious_probability": round(float(probs[i]), 4)
            })

        return {
            "total_evaluated": len(preds),
            "total_benign": int((preds == 0).sum()),
            "total_malicious": int((preds == 1).sum()),
            "malicious_ratio_percent": round(float((preds == 1).mean() * 100), 2),
            "results_sample": results[:10]
        }
