import os
import json
import time
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "processed", "cicids2017_cleaned_sample.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH)
    y = df["Is_Malicious"].values

    drop_cols = ["Clean_Label", "Attack_Category", "Is_Malicious"]
    feature_cols = [c for c in df.columns if c not in drop_cols]
    X = df[feature_cols]

    # Save feature names list for prediction
    with open(os.path.join(MODELS_DIR, "selected_features.json"), "w") as f:
        json.dump(feature_cols, f, indent=4)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.joblib"))

    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols


def train_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols):
    models = {
        "Random Forest": {
            "model": RandomForestClassifier(n_estimators=100, max_depth=18, min_samples_split=8, n_jobs=-1, random_state=42),
            "scaled": False,
            "filename": "random_forest.joblib"
        },
        "Decision Tree": {
            "model": DecisionTreeClassifier(max_depth=15, min_samples_split=10, random_state=42),
            "scaled": False,
            "filename": "decision_tree.joblib"
        },
        "K-Nearest Neighbors": {
            "model": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            "scaled": True,
            "filename": "knn.joblib",
            "subsample": 20000
        },
        "Logistic Regression": {
            "model": LogisticRegression(max_iter=1000, random_state=42),
            "scaled": True,
            "filename": "logistic_regression.joblib"
        },
        "Support Vector Machine": {
            "model": LinearSVC(C=1.0, max_iter=2000, random_state=42, dual=False),
            "scaled": True,
            "filename": "svm.joblib",
            "subsample": 25000
        },
        "Gaussian Naive Bayes": {
            "model": GaussianNB(),
            "scaled": True,
            "filename": "naive_bayes.joblib"
        }
    }

    results = []
    best_f1 = 0
    best_clf = None
    best_name = None
    best_preds = None

    for name, cfg in models.items():
        print(f"Training {name}...")
        clf = cfg["model"]
        X_tr = X_train_scaled if cfg["scaled"] else X_train
        X_te = X_test_scaled if cfg["scaled"] else X_test

        # Subsample for computationally expensive models
        if "subsample" in cfg:
            idx = np.random.RandomState(42).choice(len(X_tr), size=cfg["subsample"], replace=False)
            X_tr_fit = X_tr[idx] if isinstance(X_tr, np.ndarray) else X_tr.iloc[idx]
            y_tr_fit = y_train[idx]
        else:
            X_tr_fit = X_tr
            y_tr_fit = y_train

        start = time.time()
        clf.fit(X_tr_fit, y_tr_fit)
        train_time = time.time() - start

        inf_start = time.time()
        y_pred = clf.predict(X_te)
        inf_time = time.time() - inf_start

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)

        # ROC-AUC calculation
        try:
            if hasattr(clf, "predict_proba"):
                auc = roc_auc_score(y_test, clf.predict_proba(X_te)[:, 1])
            else:
                auc = roc_auc_score(y_test, clf.decision_function(X_te))
        except Exception:
            auc = 0.5

        # Save model
        joblib.dump(clf, os.path.join(MODELS_DIR, cfg["filename"]))

        results.append({
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "Weighted_F1": round(f1, 4),
            "ROC_AUC": round(auc, 4),
            "Train_Time_Sec": round(train_time, 2),
            "Inference_Time_Sec": round(inf_time, 4),
            "Artifact": cfg["filename"]
        })

        if f1 > best_f1:
            best_f1 = f1
            best_clf = clf
            best_name = name
            best_preds = y_pred

    # Save best model
    joblib.dump(best_clf, os.path.join(MODELS_DIR, "best_model.joblib"))
    print(f"Best model: {best_name} (F1: {best_f1 * 100:.2f}%)")

    # Save metrics
    df_results = pd.DataFrame(results)
    df_results.to_csv(os.path.join(REPORTS_DIR, "model_comparison.csv"), index=False)

    with open(os.path.join(REPORTS_DIR, "evaluation_metrics.json"), "w") as f:
        json.dump({
            "comparison": results,
            "best_model": best_name,
            "best_f1": best_f1
        }, f, indent=4)

    # Generate charts
    plot_results(df_results, best_preds, y_test, best_clf, feature_cols)


def train_multiclass(feature_cols):
    print("Training Multiclass Random Forest (Attack Categories)...")
    df = pd.read_csv(DATA_PATH)
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(df["Attack_Category"])
    joblib.dump(encoder, os.path.join(MODELS_DIR, "label_encoder.joblib"))

    X_tr, X_te, y_tr, y_te = train_test_split(
        df[feature_cols], y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    clf = RandomForestClassifier(n_estimators=100, max_depth=18, min_samples_split=8, n_jobs=-1, random_state=42)
    clf.fit(X_tr, y_tr)
    y_pred = clf.predict(X_te)

    report = classification_report(y_te, y_pred, target_names=encoder.classes_, digits=4)
    with open(os.path.join(REPORTS_DIR, "multiclass_classification_report.txt"), "w") as f:
        f.write(report)

    joblib.dump(clf, os.path.join(MODELS_DIR, "multiclass_rf.joblib"))
    print(f"Multiclass Accuracy: {accuracy_score(y_te, y_pred) * 100:.2f}%")


def plot_results(df_results, best_preds, y_test, best_clf, feature_cols):
    # 1. Comparison Bar Chart
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_results, x="Model", y="Accuracy", palette="Blues_r")
    plt.title("Model Accuracy Comparison", fontsize=12, fontweight="bold")
    plt.ylim(0.6, 1.02)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "model_comparison_bar.png"), dpi=300)
    plt.close()

    # 2. Confusion Matrix
    cm = confusion_matrix(y_test, best_preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Benign", "Malicious"], yticklabels=["Benign", "Malicious"])
    plt.title("Confusion Matrix - Random Forest", fontsize=12, fontweight="bold")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "confusion_matrix.png"), dpi=300)
    plt.close()

    # 3. Top Feature Importances
    if hasattr(best_clf, "feature_importances_"):
        imp = best_clf.feature_importances_
        idx = np.argsort(imp)[::-1][:15]
        plt.figure(figsize=(9, 5))
        sns.barplot(x=imp[idx], y=[feature_cols[i] for i in idx], palette="viridis")
        plt.title("Top 15 Most Important Features", fontsize=12, fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, "feature_importances.png"), dpi=300)
        plt.close()


if __name__ == "__main__":
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols = load_data()
    train_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols)
    train_multiclass(feature_cols)
