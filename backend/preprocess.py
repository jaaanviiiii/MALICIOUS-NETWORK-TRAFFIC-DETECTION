import os
import glob
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "dataset", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "dataset", "processed")
OUTPUT_CSV = os.path.join(PROCESSED_DIR, "cicids2017_cleaned_sample.csv")
SUMMARY_JSON = os.path.join(PROCESSED_DIR, "preprocessing_summary.json")

# Sample limits per file to handle class imbalance
SAMPLE_LIMITS = {
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv": {"attack": 12000, "benign": 10000},
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv": {"attack": 12000, "benign": 10000},
    "Friday-WorkingHours-Morning.pcap_ISCX.csv": {"attack": None, "benign": 6000},
    "Monday-WorkingHours.pcap_ISCX.csv": {"attack": None, "benign": 15000},
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv": {"attack": None, "benign": 6000},
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv": {"attack": None, "benign": 6000},
    "Tuesday-WorkingHours.pcap_ISCX.csv": {"attack": None, "benign": 8000},
    "Wednesday-workingHours.pcap_ISCX.csv": {"attack": 16000, "benign": 10000}
}


def clean_label(label):
    text = str(label).strip()
    upper = text.upper()
    if "BENIGN" in upper:
        return "BENIGN"
    elif "DDOS" in upper:
        return "DDoS"
    elif "PORTSCAN" in upper:
        return "PortScan"
    elif "BOT" in upper:
        return "Bot"
    elif "INFILTRATION" in upper:
        return "Infiltration"
    elif "WEB ATTACK" in upper:
        return "Web Attack"
    elif "PATATOR" in upper:
        return "Brute Force"
    elif "DOS" in upper or "HEARTBLEED" in upper:
        return "DoS"
    return "Other Attack"


def process_dataset():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    if not raw_files:
        print("No CSV files found in dataset/raw folder.")
        return

    sampled_dfs = []

    for file_path in raw_files:
        name = os.path.basename(file_path)
        print(f"Reading {name}...")
        df = pd.read_csv(file_path, encoding="cp1252", low_memory=False)
        df.columns = df.columns.str.strip()

        label_col = [c for c in df.columns if "label" in c.lower()][0]
        df["Attack_Category"] = df[label_col].apply(clean_label)
        df["Clean_Label"] = df["Attack_Category"]
        df["Is_Malicious"] = (df["Attack_Category"] != "BENIGN").astype(int)

        benign = df[df["Is_Malicious"] == 0]
        attack = df[df["Is_Malicious"] == 1]

        rule = SAMPLE_LIMITS.get(name, {"attack": 10000, "benign": 10000})

        # Sample benign traffic
        if rule["benign"] and len(benign) > rule["benign"]:
            benign = benign.sample(n=rule["benign"], random_state=42)

        # Sample attack traffic
        if rule["attack"] and len(attack) > rule["attack"]:
            attack = attack.sample(n=rule["attack"], random_state=42)

        sampled_dfs.append(pd.concat([benign, attack], ignore_index=True))

    data = pd.concat(sampled_dfs, ignore_index=True)

    # Drop duplicate or redundant columns
    if "Fwd Header Length.1" in data.columns:
        data = data.drop(columns=["Fwd Header Length.1"])

    cols_to_drop = [c for c in data.columns if "label" in c.lower() and c not in ["Clean_Label"]]
    if cols_to_drop:
        data = data.drop(columns=cols_to_drop)

    # Replace infinite values and handle missing values with median
    data = data.replace([np.inf, -np.inf], np.nan)
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if data[col].isna().sum() > 0:
            data[col] = data[col].fillna(data[col].median())

    # Drop constant columns (zero variance)
    features = [c for c in numeric_cols if c not in ["Is_Malicious"]]
    zero_std = [c for c in features if data[c].std() == 0]
    if zero_std:
        data = data.drop(columns=zero_std)

    # Shuffle dataset
    data = data.sample(frac=1.0, random_state=42).reset_index(drop=True)

    # Save cleaned dataset
    data.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved cleaned dataset: {OUTPUT_CSV} ({len(data)} rows)")

    summary = {
        "total_records": len(data),
        "total_features": len(data.columns) - 3,
        "feature_names": [c for c in data.columns if c not in ["Clean_Label", "Attack_Category", "Is_Malicious"]],
        "binary_distribution": data["Is_Malicious"].value_counts().to_dict(),
        "attack_category_distribution": data["Attack_Category"].value_counts().to_dict()
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=4)


if __name__ == "__main__":
    process_dataset()
