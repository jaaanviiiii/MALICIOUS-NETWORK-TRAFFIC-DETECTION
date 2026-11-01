# Malicious Network Traffic Detection System

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An end-to-end Machine Learning-powered Network Intrusion Detection System (NIDS) trained on the Canadian Institute for Cybersecurity **CIC-IDS2017** benchmark dataset. The system analyzes bidirectional network flows to detect malicious activity in real-time, categorize attack vectors, assess threat severity, and deliver actionable security insights through a clean, modern web interface.

---

## 🌟 Key Features

- **Multi-Class Threat Categorization**: Detects 8 distinct traffic classes:
  - `BENIGN` (Normal traffic)
  - `DDoS` (High-rate packet floods)
  - `PortScan` (Reconnaissance and port sweep attempts)
  - `DoS` (Hulk, GoldenEye, Slowloris, Slowhttptest)
  - `Brute Force` (FTP-Patator, SSH-Patator credential attacks)
  - `Web Attack` (SQL Injection, Cross-Site Scripting, Brute Force Web)
  - `Botnet` (ARES command-and-control communication)
  - `Infiltration` (Internal network exploitation)
- **High-Accuracy Classification Engine**:
  - Binary Classifier: **99.77% Accuracy** and **99.77% F1-Score** (Random Forest)
  - Multi-Class Classifier: **99.28% Accuracy** across 8 threat categories
  - Feature selection pipeline utilizing top discriminative flow statistical markers (`Destination Port`, `Init Win Bytes`, `Packet Length Std`, `Flow Packets/s`).
- **Real-Time Threat Severity Assessment**:
  - Classifies detections into `SAFE` (Benign), `SUSPICIOUS` (Low confidence / anomalous flow), and `CRITICAL THREAT` (Confirmed signature / high confidence attack).
- **Interactive Web Interface**:
  - Built with React 19, Vite, and custom light-theme styling (Navy Blue / Sky Blue palette).
  - **Dashboard**: High-level telemetry, KPI cards, attack distribution breakdown, and quick action launcher.
  - **Traffic Detection**: Live flow inspector and batch CSV log upload with multi-step validation and downloadable audit reports.
  - **Attack Analytics**: Interactive distribution charts, flow duration vs. packet count correlation, and attack taxonomy guide.
  - **Model Performance**: Visual confusion matrix (25,804 test flows), precision-recall metrics, and top-8 feature importance rankings.
  - **Model Comparison**: Benchmark table and radar/bar comparisons across 6 machine learning architectures.
  - **Detection History**: Persistent session log tracking all analyzed batches with per-session text audit downloads.
  - **About Project**: In-depth architectural documentation, methodology, dataset characteristics, and engineering considerations.
- **Robust REST API**:
  - Powered by FastAPI with automated OpenAPI/Swagger documentation (`/docs`).
  - Supports both single-flow and batch CSV flow inferences with NaN/Inf sanitization.

---

## 📊 Model Benchmark Summary

Evaluation conducted on a held-out stratified test set of **25,804 network flows** from CIC-IDS2017:

| Model Architecture | Accuracy | Precision | Recall | F1-Score | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Champion)** | **99.77%** | **99.88%** | **99.66%** | **99.77%** | **0.08 ms / flow** |
| **Decision Tree** | 99.33% | 99.31% | 99.35% | 99.33% | 0.02 ms / flow |
| **K-Nearest Neighbors (k=5)** | 98.71% | 98.65% | 98.78% | 98.71% | 2.15 ms / flow |
| **Logistic Regression** | 87.21% | 88.42% | 85.34% | 86.86% | 0.01 ms / flow |
| **Linear Support Vector Classifier** | 86.83% | 87.95% | 85.02% | 86.44% | 0.01 ms / flow |
| **Gaussian Naive Bayes** | 64.46% | 58.12% | 72.30% | 57.55% | 0.03 ms / flow |

---

## 🏗️ System Architecture

```
malicious-network-detection/
├── backend/
│   ├── main.py                     # FastAPI REST API application & endpoints
│   ├── predict.py                  # Single & batch inference engine with threat scoring
│   ├── preprocess.py               # CIC-IDS2017 cleaning & stratified sampling pipeline
│   ├── syllabus_demos.py           # Evaluation helper utilities
│   └── train.py                    # Multi-model training, benchmarking & serialization
├── dataset/
│   ├── processed/
│   │   ├── cicids2017_cleaned_sample.csv  # 129,016 cleaned, balanced benchmark flows
│   │   └── preprocessing_summary.json     # Preprocessing metadata and class counts
│   └── raw/
│       └── README.md               # Guide for acquiring the 8 raw CIC-IDS2017 CSV files
├── frontend/
│   ├── public/                     # Static assets & icons
│   ├── src/
│   │   ├── components/             # Reusable UI components (Header, Sidebar)
│   │   ├── data/                   # Pre-compiled benchmark metrics & mock sessions
│   │   ├── pages/                  # 7 core views (Dashboard, TrafficDetection, etc.)
│   │   ├── App.jsx                 # Main application layout and router state
│   │   ├── index.css               # Clean, custom light-theme design system
│   │   └── main.jsx                # React DOM root entry
│   ├── package.json
│   └── vite.config.js
├── models/
│   ├── best_model.joblib           # Optimized Binary Random Forest model (99.77% F1)
│   ├── multiclass_rf.joblib        # 8-Class Attack Classifier (99.28% Acc)
│   ├── decision_tree.joblib        # Decision Tree classifier
│   ├── knn.joblib                  # K-Nearest Neighbors classifier
│   ├── logistic_regression.joblib  # Logistic Regression baseline
│   ├── naive_bayes.joblib          # Gaussian Naive Bayes baseline
│   ├── svm.joblib                  # Linear Support Vector Classifier
│   ├── scaler.joblib               # StandardScaler fitted on training features
│   ├── label_encoder.joblib        # Multi-class attack label encoder
│   └── selected_features.json      # 69 verified network flow feature definitions
├── notebooks/
│   ├── 01_data_exploration_and_preprocessing.ipynb
│   └── 02_model_training_and_evaluation.ipynb
├── reports/
│   ├── figures/                    # Generated confusion matrices, feature importance plots
│   ├── academic_audit.md           # Technical audit on data leakage & cross-day evaluation
│   ├── evaluation_metrics.json     # Numerical metrics for all trained models
│   └── model_comparison.csv       # Formatted tabular comparison data
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+** (Tested on Python 3.11)
- **Node.js 18+** & **npm 9+**
- **Git**

---

### 1. Clone the Repository
```bash
git clone https://github.com/jaaanviiiii/MALICIOUS-NETWORK-TRAFFIC-DETECTION.git
cd MALICIOUS-NETWORK-TRAFFIC-DETECTION
```

---

### 2. Backend Setup
1. Create and activate a Python virtual environment:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the FastAPI backend server:
   ```bash
   uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```
   - **Backend API**: `http://127.0.0.1:8000`
   - **Interactive API Documentation (Swagger)**: `http://127.0.0.1:8000/docs`

---

### 3. Frontend Setup
1. Open a new terminal and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   - **Application Dashboard**: `http://127.0.0.1:5173`

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check & model status summary |
| `POST` | `/predict` | Predict binary status and multiclass attack category for a single flow |
| `POST` | `/predict/batch` | Upload a CSV file of flows for bulk classification & threat scoring |
| `GET` | `/models/metrics` | Retrieve evaluation metrics for all trained architectures |
| `GET` | `/models/features` | Return list of active features and Random Forest importance scores |
| `GET` | `/models/sample-vectors` | Retrieve pre-configured benign and attack test vectors for testing |

---

## 🔬 Dataset & Preprocessing

The model is trained on the **CIC-IDS2017** dataset generated by the Canadian Institute for Cybersecurity:
- **Zero-Variance Removal**: 8 constant features (e.g., `Bwd PSH Flags`, `Fwd URG Flags`, `CWE Flag Count`) eliminated to reduce dimensionality.
- **Sanitization**: Removed infinite values and corrupt rate measurements caused by zero-duration flows.
- **Sampling Strategy**: Preserved 100% of rare attacks (`Heartbleed`, `Infiltration`, `Web Attack - SQL Injection`) with stratified sampling for high-frequency classes.
- **Leakage Prevention**: Feature scaling (`StandardScaler`) is fitted strictly on the training partition ($N_{train} = 103,212$) and transformed on the test partition ($N_{test} = 25,804$).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors & Acknowledgments

- **Lead Developer**: Jaanvi Soni ([@jaaanviiiii](https://github.com/jaaanviiiii))
- **Dataset Reference**: Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB).
- **Research Citation**:
  > Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization", 4th International Conference on Information Systems Security and Privacy (ICISSP), Portugal, January 2018.
