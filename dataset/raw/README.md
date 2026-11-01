# CIC-IDS2017 Raw Dataset

This directory holds the 8 raw network traffic flow CSV files from the Canadian Institute for Cybersecurity (CIC-IDS2017) benchmark:

1. `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` (~77 MB)
2. `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` (~76 MB)
3. `Friday-WorkingHours-Morning.pcap_ISCX.csv` (~58 MB)
4. `Monday-WorkingHours.pcap_ISCX.csv` (~176 MB)
5. `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv` (~83 MB)
6. `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` (~52 MB)
7. `Tuesday-WorkingHours.pcap_ISCX.csv` (~135 MB)
8. `Wednesday-workingHours.pcap_ISCX.csv` (~225 MB)

> **Note:** Raw CSV files are excluded from Git version control because individual file sizes (up to 225 MB) exceed GitHub's 100 MB per-file upload limit.

### Data Acquisition
To acquire or update the raw files, download the CIC-IDS2017 dataset from the official University of New Brunswick (UNB) website:
https://www.unb.ca/cic/datasets/ids-2017.html

Place the downloaded CSV files in this directory (`dataset/raw/`), then run:
```bash
python backend/preprocess.py
```
This produces the cleaned stratified benchmark dataset in `dataset/processed/cicids2017_cleaned_sample.csv`.
