"""
Arquivo original: Others/renameToOldId.py

Propósito: converte os exports ROI_SubjectNNN_SessionNNN.mat da numeração
sequencial (new_id) de volta para o id original do OpenNeuro (old_id) usando
id_mapping.csv. Útil para cruzar com os metadados originais do ID1000.
"""

import os
import csv
import re

# --- CONFIGURE HERE ---
csv_path = r".\Others\id_mapping.csv"
folder_path = r".\Others\ROIs\full"
new_folder_path = r".\Others\ROIs\fullRenamed"
# ----------------------

# Load new_id → old_id map from CSV
id_map = {}
with open(csv_path, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Extract numbers: "sub-0001" → "0001"
        new_num = row["new_id"].replace("sub-", "")
        old_num = row["old_id"].replace("sub-", "")
        id_map[new_num] = old_num

# Pattern to match file names like: ROI_Subject001_Session001.mat
pattern = re.compile(r"(ROI_Subject)(\d{3})(_Session\d{3}\.mat)")

for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        prefix, subj_num, suffix = match.groups()

        # Convert SubjectXXX number to 4-digit (0001 style)
        subj_num_4d = subj_num.zfill(4)

        if subj_num_4d in id_map:
            old_id_4d = id_map[subj_num_4d]

            # Convert from "0001" → "001" for the filename format
            old_id_3d = old_id_4d[-3:]

            new_filename = f"{prefix}{old_id_3d}{suffix}"

            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(new_folder_path, new_filename)

            print(f"Renaming: {filename} → {new_filename}")
            os.rename(old_path, new_path)
