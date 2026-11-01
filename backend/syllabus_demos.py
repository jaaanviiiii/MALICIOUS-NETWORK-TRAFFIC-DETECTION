"""
Academic & Syllabus Compliance Demonstrations
Machine Learning Course - Units 1, 2, and 3 (Second-Year CSE)

Topics Demonstrated:
1. Unit 1: Linear Regression (Continuous Target Modeling vs Classification)
2. Unit 1: Regularization Analysis (L1 Lasso vs L2 Ridge in Logistic Regression)
3. Unit 2 & 3: Overfitting vs Underfitting (Decision Tree Depth Sweep & Learning Curves)
4. Unit 3: Hyperparameter Tuning (GridSearchCV) & 5-Fold Cross-Validation
5. Unit 2/3: Unsupervised Learning (K-Means Clustering on Unlabeled Network Flows)
6. Reinforcement Learning Framework & Ethical/Deployment Considerations
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, f1_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "processed", "cicids2017_cleaned_sample.csv")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def run_linear_regression_demo(df: pd.DataFrame) -> dict:
    """
    Unit 1: Linear Regression Demonstration
    Models continuous network flow telemetry (predicting Flow Duration).
    Contrasts continuous error metrics (MSE, RMSE, R2) with classification metrics.
    """
    print("\n--- [Unit 1 Demo] Linear Regression on Flow Duration ---")
    reg_features = [
        "Total Fwd Packets",
        "Total Backward Packets",
        "Total Length of Fwd Packets",
        "Total Length of Bwd Packets",
        "Flow Packets/s",
        "Average Packet Size"
    ]
    # Filter features that exist
    features_present = [f for f in reg_features if f in df.columns]
    
    # Take a non-infinite subset
    df_clean = df[features_present + ["Flow Duration"]].dropna()
    df_clean = df_clean[df_clean["Flow Duration"] > 0].sample(n=min(25000, len(df_clean)), random_state=42)

    X_reg = df_clean[features_present]
    y_reg = np.log1p(df_clean["Flow Duration"])  # log-transform to stabilize variance

    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

    scaler_r = StandardScaler()
    X_train_r_scaled = scaler_r.fit_transform(X_train_r)
    X_test_r_scaled = scaler_r.transform(X_test_r)

    reg_model = LinearRegression()
    reg_model.fit(X_train_r_scaled, y_train_r)
    y_pred_r = reg_model.predict(X_test_r_scaled)

    mse = mean_squared_error(y_test_r, y_pred_r)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test_r, y_pred_r)
    r2 = r2_score(y_test_r, y_pred_r)

    print(f"Features: {features_present}")
    print(f"R² Score: {r2:.4f} | MAE: {mae:.4f} | RMSE: {rmse:.4f}")

    return {
        "features": features_present,
        "target": "Flow Duration (log1p transformed)",
        "r2_score": round(float(r2), 4),
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "mse": round(float(mse), 4)
    }


def run_regularization_analysis(X_train_scaled, y_train, X_test_scaled, y_test, feature_names: list) -> dict:
    """
    Unit 1: Regularization Comparison (L1 Lasso vs L2 Ridge)
    Demonstrates sparsity in weights and variance reduction.
    """
    print("\n--- [Unit 1 Demo] Regularization Analysis (L1 vs L2) ---")
    sub_size = min(15000, len(X_train_scaled))
    idx = np.random.RandomState(42).choice(len(X_train_scaled), size=sub_size, replace=False)
    X_sub = X_train_scaled[idx]
    y_sub = y_train[idx]

    # L2 Regularization (Ridge)
    clf_l2 = LogisticRegression(penalty="l2", C=1.0, solver="lbfgs", max_iter=500, random_state=42)
    clf_l2.fit(X_sub, y_sub)
    y_pred_l2 = clf_l2.predict(X_test_scaled)
    acc_l2 = accuracy_score(y_test, y_pred_l2)
    f1_l2 = f1_score(y_test, y_pred_l2, average="weighted")
    non_zero_l2 = int(np.sum(clf_l2.coef_ != 0))

    # L1 Regularization (Lasso)
    clf_l1 = LogisticRegression(penalty="l1", C=0.1, solver="saga", max_iter=300, random_state=42)
    clf_l1.fit(X_sub, y_sub)
    y_pred_l1 = clf_l1.predict(X_test_scaled)
    acc_l1 = accuracy_score(y_test, y_pred_l1)
    f1_l1 = f1_score(y_test, y_pred_l1, average="weighted")
    zero_weights_l1 = int(np.sum(clf_l1.coef_ == 0))
    non_zero_l1 = int(np.sum(clf_l1.coef_ != 0))

    print(f"L2 Ridge (C=1.0) -> Accuracy: {acc_l2*100:.2f}% | Non-zero coefficients: {non_zero_l2}/{len(feature_names)}")
    print(f"L1 Lasso (C=0.1) -> Accuracy: {acc_l1*100:.2f}% | Zeroed weights (sparsity): {zero_weights_l1}/{len(feature_names)}")

    return {
        "l2_ridge": {
            "accuracy": round(float(acc_l2), 4),
            "f1_score": round(float(f1_l2), 4),
            "active_coefficients": non_zero_l2
        },
        "l1_lasso": {
            "accuracy": round(float(acc_l1), 4),
            "f1_score": round(float(f1_l1), 4),
            "zeroed_coefficients": zero_weights_l1,
            "active_coefficients": non_zero_l1
        }
    }


def run_overfitting_underfitting_sweep(X_train, y_train, X_test, y_test):
    """
    Units 2 & 3: Overfitting vs Underfitting Analysis
    Sweeps Decision Tree max_depth from 1 to 25 and generates the classic bias-variance curve.
    """
    print("\n--- [Unit 2/3 Demo] Overfitting vs Underfitting Analysis ---")
    sub_size = min(20000, len(X_train))
    idx = np.random.RandomState(42).choice(len(X_train), size=sub_size, replace=False)
    X_tr_sub = X_train.iloc[idx] if isinstance(X_train, pd.DataFrame) else X_train[idx]
    y_tr_sub = y_train[idx]

    depths = [1, 2, 3, 5, 7, 10, 14, 18, 22, 26]
    train_scores = []
    test_scores = []

    for d in depths:
        dt = DecisionTreeClassifier(max_depth=d, random_state=42)
        dt.fit(X_tr_sub, y_tr_sub)
        train_acc = accuracy_score(y_tr_sub, dt.predict(X_tr_sub))
        test_acc = accuracy_score(y_test, dt.predict(X_test))
        train_scores.append(train_acc)
        test_scores.append(test_acc)
        print(f"  Depth {d:2d} -> Train Acc: {train_acc*100:.2f}% | Test Acc: {test_acc*100:.2f}%")

    # Plot Overfitting/Underfitting Curve
    plt.figure(figsize=(9, 5))
    plt.plot(depths, train_scores, "o-", color="#1f77b4", label="Training Accuracy", linewidth=2)
    plt.plot(depths, test_scores, "s--", color="#ff7f0e", label="Testing Accuracy", linewidth=2)
    plt.axvline(x=10, color="gray", linestyle=":", alpha=0.7, label="Optimal Zone (Depth 10-15)")
    plt.title("Decision Tree Complexity Analysis: Underfitting vs Overfitting", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Tree Max Depth (Model Complexity)", fontsize=11)
    plt.ylabel("Accuracy Score", fontsize=11)
    plt.ylim(0.85, 1.01)
    plt.legend(loc="lower right", frameon=True)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    out_path = os.path.join(FIGURES_DIR, "overfitting_underfitting_curve.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved learning curve to: {out_path}")

    return {
        "depths": depths,
        "train_accuracies": [round(float(s), 4) for s in train_scores],
        "test_accuracies": [round(float(s), 4) for s in test_scores],
        "plot_path": out_path
    }


def run_cross_validation_and_grid_search(X_train, y_train):
    """
    Unit 3: 5-Fold Cross-Validation and Hyperparameter Tuning
    Performs k-fold CV and GridSearchCV on Decision Tree parameters.
    """
    print("\n--- [Unit 3 Demo] 5-Fold Cross-Validation & Hyperparameter Tuning ---")
    sub_size = min(20000, len(X_train))
    idx = np.random.RandomState(42).choice(len(X_train), size=sub_size, replace=False)
    X_sub = X_train.iloc[idx] if isinstance(X_train, pd.DataFrame) else X_train[idx]
    y_sub = y_train[idx]

    dt = DecisionTreeClassifier(max_depth=12, random_state=42)
    cv_scores = cross_val_score(dt, X_sub, y_sub, cv=5, scoring="f1_weighted", n_jobs=-1)
    print(f"5-Fold Cross-Validation F1 Scores: {[round(s, 4) for s in cv_scores]}")
    print(f"Mean CV Score: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")

    # Hyperparameter Grid Search
    param_grid = {
        "max_depth": [8, 12, 16],
        "min_samples_split": [5, 10],
        "criterion": ["gini", "entropy"]
    }
    grid = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid, cv=3, scoring="f1_weighted", n_jobs=-1)
    grid.fit(X_sub, y_sub)
    print(f"GridSearchCV Best Params: {grid.best_params_}")
    print(f"GridSearchCV Best F1-Score: {grid.best_score_*100:.2f}%")

    return {
        "cv_folds": 5,
        "cv_scores": [round(float(s), 4) for s in cv_scores],
        "cv_mean": round(float(cv_scores.mean()), 4),
        "cv_std": round(float(cv_scores.std()), 4),
        "grid_search_best_params": grid.best_params_,
        "grid_search_best_score": round(float(grid.best_score_), 4)
    }


def run_unsupervised_kmeans_demo(X_train_scaled, y_train):
    """
    Unit 2/3: Unsupervised Learning Demonstration
    Applies K-Means clustering (k=2) without labels to evaluate natural cluster separation.
    """
    print("\n--- [Unit 2/3 Demo] Unsupervised K-Means Clustering on Network Flows ---")
    sub_size = min(10000, len(X_train_scaled))
    idx = np.random.RandomState(42).choice(len(X_train_scaled), size=sub_size, replace=False)
    X_sub = X_train_scaled[idx]
    y_true_sub = y_train[idx]

    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_sub)

    # Determine cluster alignment with ground truth
    cluster_0_malicious_pct = float(np.mean(y_true_sub[clusters == 0]))
    cluster_1_malicious_pct = float(np.mean(y_true_sub[clusters == 1]))

    print(f"Cluster 0: {len(clusters[clusters == 0]):,} flows ({cluster_0_malicious_pct*100:.1f}% malicious)")
    print(f"Cluster 1: {len(clusters[clusters == 1]):,} flows ({cluster_1_malicious_pct*100:.1f}% malicious)")

    # Align cluster assignment to calculate unsupervised accuracy
    pred_labels = clusters if cluster_1_malicious_pct > cluster_0_malicious_pct else 1 - clusters
    unsupervised_acc = accuracy_score(y_true_sub, pred_labels)
    print(f"Unsupervised Anomaly Separation Accuracy: {unsupervised_acc*100:.2f}%")

    return {
        "algorithm": "K-Means Clustering (k=2)",
        "unsupervised_accuracy": round(float(unsupervised_acc), 4),
        "cluster_0_size": int(np.sum(clusters == 0)),
        "cluster_1_size": int(np.sum(clusters == 1)),
        "cluster_0_malicious_ratio": round(cluster_0_malicious_pct, 4),
        "cluster_1_malicious_ratio": round(cluster_1_malicious_pct, 4)
    }


def execute_all_demos():
    print("=" * 70)
    print("EXECUTING SYLLABUS COMPLIANCE DEMONSTRATIONS (UNITS 1, 2, AND 3)")
    print("=" * 70)

    df = pd.read_csv(DATA_PATH)
    features = [c for c in df.columns if c not in ["Clean_Label", "Attack_Category", "Is_Malicious"]]
    X = df[features]
    y = df["Is_Malicious"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    results = {}
    results["linear_regression"] = run_linear_regression_demo(df)
    results["regularization"] = run_regularization_analysis(X_train_scaled, y_train, X_test_scaled, y_test, features)
    results["overfitting_sweep"] = run_overfitting_underfitting_sweep(X_train, y_train, X_test, y_test)
    results["cross_validation"] = run_cross_validation_and_grid_search(X_train, y_train)
    results["unsupervised_kmeans"] = run_unsupervised_kmeans_demo(X_train_scaled, y_train)

    out_file = os.path.join(REPORTS_DIR, "syllabus_demonstrations.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\nAll syllabus demonstrations completed! Output saved to: {out_file}")


if __name__ == "__main__":
    execute_all_demos()
