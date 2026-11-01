"""
Model Training and Evaluation Pipeline
Machine Learning Syllabus - Units 1, 2, and 3 (Second-Year CSE)

Models Implemented:
1. Unit 1: Logistic Regression (Linear Classifier baseline)
2. Unit 2: Gaussian Naive Bayes (Probabilistic Classifier)
3. Unit 2: K-Nearest Neighbors (KNN, Instance-Based Classifier)
4. Unit 2: Decision Tree Classifier (CART / Gini Impurity)
5. Unit 2: Support Vector Machine (LinearSVC, Maximum Margin Classifier)
6. Unit 3: Random Forest Classifier (Bagging Ensemble of Trees)
7. Multiclass Classifier: Random Forest (8 Attack Categories)

Evaluation Metrics (Unit 3):
- Accuracy, Precision, Recall, F1-Score (Macro & Weighted), ROC-AUC
- Confusion Matrix (Normalized & Raw)
- Per-class Classification Report
- Feature Importance ranking
"""

import os
import json
import time
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server generation
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
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "dataset", "processed", "cicids2017_cleaned_sample.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)


def load_and_prepare_data(target_type: str = "binary", test_size: float = 0.2, random_state: int = 42):
    """
    Loads preprocessed dataset, separates features and target,
    scales numerical features with StandardScaler, and performs stratified split.
    
    target_type: 'binary' (0: Benign, 1: Malicious) or 'multiclass' (8 attack categories)
    """
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Cleaned dataset not found at {PROCESSED_DATA_PATH}. Run preprocess.py first.")

    print(f"Loading dataset from: {PROCESSED_DATA_PATH}")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    print(f"Loaded {len(df):,} records with {len(df.columns)} columns.")

    # Target selection
    if target_type == "binary":
        y = df["Is_Malicious"].values
        target_names = ["BENIGN", "MALICIOUS"]
        label_encoder = None
    else:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(df["Attack_Category"])
        target_names = label_encoder.classes_.tolist()
        joblib.dump(label_encoder, os.path.join(MODELS_DIR, "label_encoder.joblib"))
        print(f"Saved LabelEncoder for categories: {target_names}")

    # Features: drop non-feature target columns
    columns_to_drop = ["Clean_Label", "Attack_Category", "Is_Malicious"]
    feature_cols = [c for c in df.columns if c not in columns_to_drop]
    X = df[feature_cols].copy()

    # Save feature names list
    with open(os.path.join(MODELS_DIR, "selected_features.json"), "w") as f:
        json.dump(feature_cols, f, indent=4)
    print(f"Preserved {len(feature_cols)} features for training.")

    # Train/Test Split (Unit 1: 80% Train, 20% Test with Stratification)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"Train set: {len(X_train):,} samples | Test set: {len(X_test):,} samples")

    # Feature Scaling (Unit 1: StandardScaler fitted strictly on X_train)
    print("Fitting StandardScaler on training data...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save scaler artifact
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.joblib"))
    print("Saved Scaler to models/scaler.joblib")

    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols, target_names


def train_and_evaluate_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols, target_names):
    """
    Trains syllabus-compliant models from Units 1, 2, and 3:
    1. Logistic Regression (Unit 1)
    2. Gaussian Naive Bayes (Unit 2)
    3. Decision Tree (Unit 2)
    4. K-Nearest Neighbors (Unit 2)
    5. Support Vector Machine (Unit 2 - LinearSVC)
    6. Random Forest (Unit 3 - Ensemble)
    """
    print("\n" + "=" * 70)
    print("TRAINING & BENCHMARKING MODELS (UNITS 1, 2, AND 3)")
    print("=" * 70)

    # Models dictionary
    models = {
        "Logistic Regression (Unit 1)": {
            "model": LogisticRegression(max_iter=1000, random_state=42, solver="lbfgs"),
            "scaled": True,
            "artifact_name": "logistic_regression.joblib"
        },
        "Gaussian Naive Bayes (Unit 2)": {
            "model": GaussianNB(),
            "scaled": True,
            "artifact_name": "naive_bayes.joblib"
        },
        "Decision Tree (Unit 2)": {
            "model": DecisionTreeClassifier(max_depth=15, min_samples_split=10, random_state=42),
            "scaled": False,  # Tree models do not require scaling
            "artifact_name": "decision_tree.joblib"
        },
        "K-Nearest Neighbors (Unit 2)": {
            "model": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            "scaled": True,
            "artifact_name": "knn.joblib",
            "subsample_for_fit": 20000  # KNN O(N^2) distance constraint
        },
        "Support Vector Machine (Unit 2)": {
            "model": LinearSVC(C=1.0, max_iter=2000, random_state=42, dual=False),
            "scaled": True,
            "artifact_name": "svm.joblib",
            "subsample_for_fit": 25000  # LinearSVC calibrated subset
        },
        "Random Forest (Unit 3)": {
            "model": RandomForestClassifier(n_estimators=100, max_depth=18, min_samples_split=8, n_jobs=-1, random_state=42),
            "scaled": False,
            "artifact_name": "random_forest.joblib"
        }
    }

    results = []
    trained_estimators = {}

    for name, config in models.items():
        print(f"\n[Training] {name}...")
        clf = config["model"]
        is_scaled = config["scaled"]

        # Select scaled or raw features
        X_tr = X_train_scaled if is_scaled else X_train
        X_te = X_test_scaled if is_scaled else X_test
        y_tr = y_train
        y_te = y_test

        # If model has a subsample limit for fast training
        if config.get("subsample_for_fit"):
            n_sub = config["subsample_for_fit"]
            indices = np.random.RandomState(42).choice(len(X_tr), size=n_sub, replace=False)
            X_tr_fit = X_tr[indices] if isinstance(X_tr, np.ndarray) else X_tr.iloc[indices]
            y_tr_fit = y_tr[indices]
            print(f"  (Subsampled {n_sub:,} instances for training efficiency)")
        else:
            X_tr_fit = X_tr
            y_tr_fit = y_tr

        # Measure training time
        start_time = time.time()
        clf.fit(X_tr_fit, y_tr_fit)
        train_duration = time.time() - start_time

        # Measure inference time and predictions
        inf_start = time.time()
        y_pred = clf.predict(X_te)
        inf_duration = time.time() - inf_start

        # Calculate metrics
        acc = accuracy_score(y_te, y_pred)
        prec = precision_score(y_te, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_te, y_pred, average="weighted", zero_division=0)
        wf1 = f1_score(y_te, y_pred, average="weighted", zero_division=0)
        mf1 = f1_score(y_te, y_pred, average="macro", zero_division=0)

        # ROC-AUC calculation
        try:
            if hasattr(clf, "predict_proba"):
                y_prob = clf.predict_proba(X_te)[:, 1]
                auc = roc_auc_score(y_te, y_prob)
            elif hasattr(clf, "decision_function"):
                y_score = clf.decision_function(X_te)
                auc = roc_auc_score(y_te, y_score)
            else:
                auc = roc_auc_score(y_te, y_pred)
        except Exception:
            auc = 0.5

        print(f"  Training Time: {train_duration:.2f}s | Inference Time: {inf_duration:.2f}s")
        print(f"  Accuracy: {acc * 100:.2f}% | Weighted F1: {wf1 * 100:.2f}% | Macro F1: {mf1 * 100:.2f}% | ROC-AUC: {auc * 100:.2f}%")

        # Save individual model artifact
        artifact_path = os.path.join(MODELS_DIR, config["artifact_name"])
        joblib.dump(clf, artifact_path)

        results.append({
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "Weighted_F1": round(wf1, 4),
            "Macro_F1": round(mf1, 4),
            "ROC_AUC": round(auc, 4),
            "Train_Time_Sec": round(train_duration, 2),
            "Inference_Time_Sec": round(inf_duration, 4),
            "Artifact": config["artifact_name"]
        })
        trained_estimators[name] = {
            "model": clf,
            "y_pred": y_pred,
            "is_scaled": is_scaled
        }

    # Identify best model by Weighted F1-Score
    results_df = pd.DataFrame(results)
    best_row = results_df.sort_values(by="Weighted_F1", ascending=False).iloc[0]
    best_model_name = best_row["Model"]
    print("\n" + "=" * 70)
    print(f"BEST MODEL IDENTIFIED: {best_model_name} (F1-Score: {best_row['Weighted_F1'] * 100:.2f}%)")
    print("=" * 70)

    # Save copy as best_model.joblib
    best_clf = trained_estimators[best_model_name]["model"]
    best_model_path = os.path.join(MODELS_DIR, "best_model.joblib")
    joblib.dump(best_clf, best_model_path)
    print(f"Saved primary production model to: {best_model_path}")

    # Save comparison table
    results_csv_path = os.path.join(REPORTS_DIR, "model_comparison.csv")
    results_df.to_csv(results_csv_path, index=False)
    print(f"Model comparison saved to: {results_csv_path}")

    # Save detailed JSON summary
    summary_json_path = os.path.join(REPORTS_DIR, "evaluation_metrics.json")
    with open(summary_json_path, "w") as f:
        json.dump({
            "comparison": results,
            "best_model": best_model_name,
            "best_accuracy": best_row["Accuracy"],
            "best_f1": best_row["Weighted_F1"],
            "best_macro_f1": best_row["Macro_F1"],
            "best_roc_auc": best_row["ROC_AUC"]
        }, f, indent=4)

    # Train Multiclass Model
    train_multiclass_model(X_train, X_test, feature_cols)

    # Generate Visualizations (Unit 3)
    generate_evaluation_figures(results_df, trained_estimators[best_model_name]["y_pred"], y_test, target_names, best_clf, feature_cols)

    return results_df, best_model_name


def train_multiclass_model(X_train, X_test, feature_cols):
    """
    Trains dedicated Random Forest Multiclass Classifier (8 attack categories).
    Saves models/multiclass_rf.joblib and models/label_encoder.joblib.
    """
    print("\n" + "=" * 70)
    print("TRAINING MULTICLASS CLASSIFIER (8 ATTACK CATEGORIES)")
    print("=" * 70)

    df = pd.read_csv(PROCESSED_DATA_PATH)
    y_cat = df["Attack_Category"]
    
    label_encoder = LabelEncoder()
    y_cat_enc = label_encoder.fit_transform(y_cat)
    joblib.dump(label_encoder, os.path.join(MODELS_DIR, "label_encoder.joblib"))

    # Train/test split for multiclass
    X_tr, X_te, y_tr, y_te = train_test_split(
        df[feature_cols], y_cat_enc, test_size=0.2, random_state=42, stratify=y_cat_enc
    )

    clf_multi = RandomForestClassifier(n_estimators=100, max_depth=18, min_samples_split=8, n_jobs=-1, random_state=42)
    clf_multi.fit(X_tr, y_tr)
    y_pred = clf_multi.predict(X_te)

    acc = accuracy_score(y_te, y_pred)
    wf1 = f1_score(y_te, y_pred, average="weighted")
    mf1 = f1_score(y_te, y_pred, average="macro")

    print(f"Multiclass Model Accuracy: {acc * 100:.2f}% | Weighted F1: {wf1 * 100:.2f}% | Macro F1: {mf1 * 100:.2f}%")
    print("\nPer-Category Classification Report:")
    report_text = classification_report(y_te, y_pred, target_names=label_encoder.classes_, digits=4)
    print(report_text)

    # Save multiclass artifact
    multi_path = os.path.join(MODELS_DIR, "multiclass_rf.joblib")
    joblib.dump(clf_multi, multi_path)
    print(f"Saved multiclass model to: {multi_path}")

    # Save text report
    with open(os.path.join(REPORTS_DIR, "multiclass_classification_report.txt"), "w") as f:
        f.write(report_text)


def generate_evaluation_figures(results_df, y_pred_best, y_test, target_names, best_clf, feature_cols):
    """Generates and saves publication-quality evaluation charts."""
    print("\n[Visualizations] Generating evaluation charts...")

    # 1. Model Comparison Bar Chart
    plt.figure(figsize=(11, 6))
    plot_df = results_df.melt(id_vars=["Model"], value_vars=["Accuracy", "Weighted_F1", "Macro_F1", "ROC_AUC"], var_name="Metric", value_name="Score")
    palette = sns.color_palette("mako", 4)
    sns.barplot(data=plot_df, x="Model", y="Score", hue="Metric", palette=palette)
    plt.title("Model Performance Comparison (Units 1, 2, and 3 Algorithms)", fontsize=13, fontweight="bold", pad=15)
    plt.ylim(0.60, 1.02)
    plt.ylabel("Score", fontsize=11)
    plt.xlabel("")
    plt.xticks(rotation=20, ha="right", fontsize=9)
    plt.legend(loc="lower right", frameon=True)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    comp_fig_path = os.path.join(FIGURES_DIR, "model_comparison_bar.png")
    plt.savefig(comp_fig_path, dpi=300)
    plt.close()
    print(f"  -> Saved: {comp_fig_path}")

    # 2. Confusion Matrix of Best Model
    cm = confusion_matrix(y_test, y_pred_best)
    plt.figure(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=target_names, yticklabels=target_names, cbar=False,
                annot_kws={"size": 13, "weight": "bold"})
    plt.title(f"Confusion Matrix - Best Classifier (Random Forest)\n(Tested on {len(y_test):,} held-out flows)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11, labelpad=8)
    plt.ylabel("Actual True Label", fontsize=11, labelpad=8)
    plt.tight_layout()
    cm_fig_path = os.path.join(FIGURES_DIR, "confusion_matrix.png")
    plt.savefig(cm_fig_path, dpi=300)
    plt.close()
    print(f"  -> Saved: {cm_fig_path}")

    # 3. Top Feature Importances (Random Forest)
    if hasattr(best_clf, "feature_importances_"):
        importances = best_clf.feature_importances_
        indices = np.argsort(importances)[::-1][:15]  # Top 15 features
        top_features = [feature_cols[i] for i in indices]
        top_scores = importances[indices]

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_scores, y=top_features, hue=top_features, palette="viridis", legend=False)
        plt.title("Top 15 Most Discriminative Network Flow Features (Gini Importance)", fontsize=12, fontweight="bold", pad=12)
        plt.xlabel("Relative Feature Importance Score", fontsize=11)
        plt.ylabel("")
        plt.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        fi_fig_path = os.path.join(FIGURES_DIR, "feature_importances.png")
        plt.savefig(fi_fig_path, dpi=300)
        plt.close()
        print(f"  -> Saved: {fi_fig_path}")

    print("All evaluation plots generated successfully!")


if __name__ == "__main__":
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols, target_names = load_and_prepare_data(target_type="binary")
    train_and_evaluate_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols, target_names)
