"""
Data Preprocessing Pipeline for CIC-IDS2017 Dataset
Machine Learning Syllabus - Unit 1: Data Preprocessing & Exploratory Analysis

Tasks Performed:
1. Load raw network flow captures from dataset/raw/
2. Clean column names (strip whitespace and fix encoding quirks)
3. Handle infinite (inf) and missing (NaN) values
4. Standardize attack labels (Binary: 0=Benign, 1=Malicious; Multiclass: 8 attack categories)
5. Preserve 100% of rare attacks while stratifying common classes to form a balanced ~125k sample
6. Remove redundant and zero-variance constant features
7. Save cleaned, ready-to-train dataset to dataset/processed/
"""

import os
import glob
import json
import numpy as np
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "dataset", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "dataset", "processed")
OUTPUT_CSV = os.path.join(PROCESSED_DIR, "cicids2017_cleaned_sample.csv")
STATS_JSON = os.path.join(PROCESSED_DIR, "preprocessing_summary.json")

# Target sampling allocation to preserve rare attacks while balancing Benign vs Attack
SAMPLING_STRATEGY = {
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv": {"attack": 12000, "benign": 10000},
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv": {"attack": 12000, "benign": 10000},
    "Friday-WorkingHours-Morning.pcap_ISCX.csv": {"attack": None, "benign": 6000},  # None = keep all rare
    "Monday-WorkingHours.pcap_ISCX.csv": {"attack": None, "benign": 15000},
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv": {"attack": None, "benign": 6000},  # keep all rare
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv": {"attack": None, "benign": 6000},  # keep all rare
    "Tuesday-WorkingHours.pcap_ISCX.csv": {"attack": None, "benign": 8000},  # keep all Patator
    "Wednesday-workingHours.pcap_ISCX.csv": {"attack": 16000, "benign": 10000}
}


def clean_label(raw_label: str) -> str:
    """Normalize raw label string to standard attack name."""
    s = str(raw_label).encode("ascii", "ignore").decode().strip()
    s_upper = s.upper()

    if "BENIGN" in s_upper:
        return "BENIGN"
    elif "DDOS" in s_upper:
        return "DDoS"
    elif "PORTSCAN" in s_upper:
        return "PortScan"
    elif "BOT" in s_upper:
        return "Bot"
    elif "INFILTRATION" in s_upper:
        return "Infiltration"
    elif "WEB ATTACK" in s_upper:
        if "SQL" in s_upper:
            return "Web Attack - SQL Injection"
        elif "XSS" in s_upper:
            return "Web Attack - XSS"
        else:
            return "Web Attack - Brute Force"
    elif "FTP-PATATOR" in s_upper:
        return "FTP-Patator"
    elif "SSH-PATATOR" in s_upper:
        return "SSH-Patator"
    elif "DOS HULK" in s_upper:
        return "DoS Hulk"
    elif "DOS GOLDENEYE" in s_upper:
        return "DoS GoldenEye"
    elif "DOS SLOWLORIS" in s_upper:
        return "DoS slowloris"
    elif "DOS SLOWHTTPTEST" in s_upper:
        return "DoS Slowhttptest"
    elif "HEARTBLEED" in s_upper:
        return "Heartbleed"
    return s


def map_category(cleaned_label: str) -> str:
    """Group granular attack names into 8 standard syllabus categories."""
    if cleaned_label == "BENIGN":
        return "BENIGN"
    elif cleaned_label == "DDoS":
        return "DDoS"
    elif cleaned_label == "PortScan":
        return "PortScan"
    elif cleaned_label in ["DoS Hulk", "DoS GoldenEye", "DoS slowloris", "DoS Slowhttptest", "Heartbleed"]:
        return "DoS"
    elif cleaned_label in ["FTP-Patator", "SSH-Patator", "Web Attack - Brute Force"]:
        return "Brute Force"
    elif cleaned_label in ["Web Attack - XSS", "Web Attack - SQL Injection"]:
        return "Web Attack"
    elif cleaned_label == "Bot":
        return "Botnet"
    elif cleaned_label == "Infiltration":
        return "Infiltration"
    return "Other Attack"


def process_dataset(random_seed: int = 42):
    """
    Reads all 8 raw CSVs, extracts representative stratified samples,
    cleans values, eliminates non-informative features, and saves the output.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    
    if not raw_files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DIR}")

    print("=" * 70)
    print("Starting CIC-IDS2017 Dataset Preprocessing Pipeline")
    print(f"Found {len(raw_files)} raw CSV files in {RAW_DIR}")
    print("=" * 70)

    sampled_dfs = []

    for file_path in raw_files:
        file_name = os.path.basename(file_path)
        print(f"\n[Processing] {file_name}...")

        # Read CSV with cp1252 encoding to avoid Windows character decoding errors
        df = pd.read_csv(file_path, encoding="cp1252", low_memory=False)
        
        # Clean column names by stripping leading/trailing whitespace
        df.columns = df.columns.str.strip()

        # Identify label column
        label_col = [col for col in df.columns if "label" in col.lower()][0]
        
        # Standardize labels
        df["Clean_Label"] = df[label_col].apply(clean_label)
        df["Attack_Category"] = df["Clean_Label"].apply(map_category)
        df["Is_Malicious"] = (df["Attack_Category"] != "BENIGN").astype(int)

        # Separate benign and attack subsets
        df_benign = df[df["Is_Malicious"] == 0]
        df_attack = df[df["Is_Malicious"] == 1]

        # Determine sampling limits
        rules = SAMPLING_STRATEGY.get(file_name, {"attack": 10000, "benign": 10000})
        
        # Sample benign flows
        benign_sample_count = rules["benign"]
        if benign_sample_count is not None and len(df_benign) > benign_sample_count:
            df_benign_sampled = df_benign.sample(n=benign_sample_count, random_state=random_seed)
        else:
            df_benign_sampled = df_benign

        # Sample attack flows (keeping 100% of rare attacks if rule is None)
        attack_sample_count = rules["attack"]
        if attack_sample_count is not None and len(df_attack) > attack_sample_count:
            # Stratified sample within attack subcategories if multiple exist
            attack_categories = df_attack["Clean_Label"].nunique()
            if attack_categories > 1:
                sampled_subsets = []
                for label_name, group in df_attack.groupby("Clean_Label"):
                    n_samples = min(len(group), max(1, int(attack_sample_count * len(group) / len(df_attack))))
                    sampled_subsets.append(group.sample(n=n_samples, random_state=random_seed))
                df_attack_sampled = pd.concat(sampled_subsets, ignore_index=True)
            else:
                df_attack_sampled = df_attack.sample(n=attack_sample_count, random_state=random_seed)
        else:
            df_attack_sampled = df_attack

        file_sample = pd.concat([df_benign_sampled, df_attack_sampled], ignore_index=True)
        print(f"  -> Selected {len(df_benign_sampled):,} Benign and {len(df_attack_sampled):,} Malicious flows.")
        sampled_dfs.append(file_sample)

    # Combine all samples
    print("\n[Merging] Combining all sampled subsets...")
    combined_df = pd.concat(sampled_dfs, ignore_index=True)
    print(f"Total merged records: {len(combined_df):,}")

    # Remove duplicate columns if any (e.g., Fwd Header Length.1)
    if "Fwd Header Length.1" in combined_df.columns:
        print("Dropping duplicate column: 'Fwd Header Length.1'")
        combined_df = combined_df.drop(columns=["Fwd Header Length.1"])

    # Drop original uncleaned label column
    label_cols_to_drop = [c for c in combined_df.columns if "label" in c.lower() and c not in ["Clean_Label"]]
    if label_cols_to_drop:
        combined_df = combined_df.drop(columns=label_cols_to_drop)

    # Handle Inf and -Inf values (classic CIC-IDS2017 artifact)
    print("[Cleaning] Replacing infinite values with NaN...")
    combined_df = combined_df.replace([np.inf, -np.inf], np.nan)

    # Check for NaN count and drop/impute
    nan_counts = combined_df.isna().sum()
    cols_with_nan = nan_counts[nan_counts > 0]
    if not cols_with_nan.empty:
        print(f"Features with missing/infinite values: {cols_with_nan.to_dict()}")
        # Impute with median for numerical columns
        for col in cols_with_nan.index:
            if col not in ["Clean_Label", "Attack_Category"]:
                median_val = combined_df[col].median()
                combined_df[col] = combined_df[col].fillna(median_val)
                print(f"  Imputed '{col}' NaNs with median: {median_val}")

    # Identify and drop constant columns (zero standard deviation)
    numeric_cols = combined_df.select_dtypes(include=[np.number]).columns
    feature_numeric_cols = [c for c in numeric_cols if c not in ["Is_Malicious"]]
    stds = combined_df[feature_numeric_cols].std()
    zero_var_cols = stds[stds == 0].index.tolist()
    
    if zero_var_cols:
        print(f"[Feature Selection] Dropping {len(zero_var_cols)} constant (zero-variance) features:")
        for c in zero_var_cols:
            print(f"  - {c}")
        combined_df = combined_df.drop(columns=zero_var_cols)

    # Shuffle the dataset
    combined_df = combined_df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)

    # Display final statistics
    print("\n" + "=" * 70)
    print("FINAL PREPROCESSED DATASET SUMMARY")
    print("=" * 70)
    print(f"Total Samples  : {len(combined_df):,}")
    print(f"Total Features : {len(combined_df.columns) - 3} numerical features (+ 3 target label columns)")
    print("\nBinary Target Distribution (Is_Malicious):")
    print(combined_df["Is_Malicious"].value_counts(normalize=True).mul(100).round(2).to_string())
    print("\nMulticlass Target Distribution (Attack_Category):")
    print(combined_df["Attack_Category"].value_counts().to_string())
    print("=" * 70)

    # Save to CSV
    print(f"\n[Saving] Writing cleaned dataset to: {OUTPUT_CSV}")
    combined_df.to_csv(OUTPUT_CSV, index=False)
    print("Clean dataset saved successfully!")

    # Save summary metadata
    summary = {
        "total_records": len(combined_df),
        "total_features": len(combined_df.columns) - 3,
        "feature_names": [c for c in combined_df.columns if c not in ["Clean_Label", "Attack_Category", "Is_Malicious"]],
        "binary_distribution": combined_df["Is_Malicious"].value_counts().to_dict(),
        "attack_category_distribution": combined_df["Attack_Category"].value_counts().to_dict(),
        "clean_label_distribution": combined_df["Clean_Label"].value_counts().to_dict(),
        "dropped_zero_variance_columns": zero_var_cols
    }
    with open(STATS_JSON, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"Metadata summary written to: {STATS_JSON}")

    return combined_df


if __name__ == "__main__":
    process_dataset()
