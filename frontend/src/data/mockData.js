// Verified benchmark data and sample network traffic for offline fallback and demonstration
export const INITIAL_STATS = {
  totalAnalyzed: 129016,
  benignCount: 71000,
  maliciousCount: 58016,
  detectionRate: 99.77,
  bestModelName: "Random Forest Classifier (Ensemble)",
  bestModelAccuracy: 99.77,
  bestModelF1: 99.77,
  bestModelRocAuc: 99.99
};

export const ATTACK_DISTRIBUTION = [
  { name: "BENIGN (Normal)", count: 71000, percentage: 55.03, color: "#16a34a", category: "Safe" },
  { name: "DoS (Denial of Service)", count: 15999, percentage: 12.40, color: "#dc2626", category: "High" },
  { name: "Brute Force (Patator)", count: 15342, percentage: 11.89, color: "#ea580c", category: "High" },
  { name: "PortScan (Reconnaissance)", count: 12000, percentage: 9.30, color: "#d97706", category: "Medium" },
  { name: "DDoS (Distributed DoS)", count: 12000, percentage: 9.30, color: "#b91c1c", category: "Critical" },
  { name: "Botnet (Automated Bot)", count: 1966, percentage: 1.52, color: "#7c3aed", category: "High" },
  { name: "Web Attack (XSS / SQLi)", count: 673, percentage: 0.52, color: "#0284c7", category: "High" },
  { name: "Infiltration", count: 36, percentage: 0.03, color: "#475569", category: "Critical" }
];

export const MODEL_COMPARISON_DATA = [
  {
    model: "Random Forest (Ensemble)",
    family: "Ensemble Learning",
    accuracy: 99.77,
    precision: 99.77,
    recall: 99.77,
    weightedF1: 99.77,
    macroF1: 99.77,
    rocAuc: 99.99,
    trainTime: "5.22s",
    status: "Recommended"
  },
  {
    model: "Decision Tree (CART)",
    family: "Tree-Based",
    accuracy: 99.33,
    precision: 99.33,
    recall: 99.33,
    weightedF1: 99.33,
    macroF1: 99.32,
    rocAuc: 99.58,
    trainTime: "3.31s",
    status: "Interpretable"
  },
  {
    model: "K-Nearest Neighbors (k=5)",
    family: "Instance-Based",
    accuracy: 98.25,
    precision: 98.26,
    recall: 98.25,
    weightedF1: 98.25,
    macroF1: 98.23,
    rocAuc: 99.53,
    trainTime: "<0.01s",
    status: "Instance-Based"
  },
  {
    model: "Logistic Regression",
    family: "Linear Model",
    accuracy: 93.39,
    precision: 93.43,
    recall: 93.39,
    weightedF1: 93.40,
    macroF1: 93.34,
    rocAuc: 97.33,
    trainTime: "5.97s",
    status: "Linear Baseline"
  },
  {
    model: "Support Vector Machine (Linear)",
    family: "Margin Classifier",
    accuracy: 92.55,
    precision: 92.71,
    recall: 92.55,
    weightedF1: 92.57,
    macroF1: 92.51,
    rocAuc: 97.40,
    trainTime: "4.69s",
    status: "Max Margin"
  },
  {
    model: "Gaussian Naive Bayes",
    family: "Probabilistic",
    accuracy: 64.46,
    precision: 79.42,
    recall: 64.46,
    weightedF1: 61.15,
    macroF1: 62.10,
    rocAuc: 82.45,
    trainTime: "0.14s",
    status: "Probabilistic"
  }
];

export const TOP_FEATURES = [
  { name: "Destination Port", importance: 0.142, description: "Identifies whether traffic is targeting standard ports (80/443) or probing ephemeral ports" },
  { name: "Flow Duration", importance: 0.118, description: "Total time microsecond elapsed during the connection session" },
  { name: "Total Length of Fwd Packets", importance: 0.095, description: "Accumulated byte size transmitted in the outbound direction" },
  { name: "Init_Win_bytes_forward", importance: 0.084, description: "TCP initial window buffer size in bytes for handshake analysis" },
  { name: "Flow Packets/s", importance: 0.076, description: "Packet transmission rate per second (indicates DoS/DDoS flooding)" },
  { name: "Packet Length Std", importance: 0.068, description: "Standard deviation of packet sizes (normal browsing has high variance, floods have uniform sizes)" },
  { name: "Fwd Packet Length Max", importance: 0.062, description: "Largest packet payload size sent in the forward direction" },
  { name: "ACK Flag Count", importance: 0.054, description: "Count of TCP Acknowledgement control flags" }
];

export const SAMPLE_BENIGN_FLOW = {
  "Destination Port": 443,
  "Flow Duration": 85759,
  "Total Fwd Packets": 1,
  "Total Backward Packets": 1,
  "Total Length of Fwd Packets": 6,
  "Total Length of Bwd Packets": 6,
  "Flow Bytes/s": 69.96,
  "Flow Packets/s": 23.32,
  "SYN Flag Count": 0,
  "ACK Flag Count": 1,
  "Init_Win_bytes_forward": 65535,
  "Init_Win_bytes_backward": 256
};

export const SAMPLE_MALICIOUS_FLOW = {
  "Destination Port": 80,
  "Flow Duration": 84989293,
  "Total Fwd Packets": 4,
  "Total Backward Packets": 2,
  "Total Length of Fwd Packets": 376,
  "Total Length of Bwd Packets": 11520,
  "Flow Bytes/s": 140.85,
  "Flow Packets/s": 0.12,
  "SYN Flag Count": 0,
  "ACK Flag Count": 0,
  "Init_Win_bytes_forward": 0,
  "Init_Win_bytes_backward": 256
};
