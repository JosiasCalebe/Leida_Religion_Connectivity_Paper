"""
Arquivo original: DeleteTimeSeriesByMetadata.py

Propósito: (cópia do script de 03_Participants_Selection) apaga de time_series/ as pastas
de sujeitos ausentes no metadata.csv, para montar a entrada do PyLEiDA de uma subamostra.
"""

import os
import shutil
import pandas as pd

# ================================
# CONFIG
# ================================
ROOT_DIR = './ArquivosNew/GlasserEducationFiltered'              # Folder that contains metadata.csv and time_series/
CSV_FILE = "metadata.csv"
TIME_SERIES_DIR = "time_series"

DRY_RUN = False   # ← Set to False to actually delete folders
# ================================

# Load CSV
csv_path = os.path.join(ROOT_DIR, CSV_FILE)
ts_path = os.path.join(ROOT_DIR, TIME_SERIES_DIR)

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"metadata.csv not found at {csv_path}")

if not os.path.exists(ts_path):
    raise FileNotFoundError(f"time_series folder not found at {ts_path}")

print("Reading metadata.csv...")
df = pd.read_csv(csv_path)

if "subject_id" not in df.columns:
    raise ValueError("CSV does not contain a 'subject_id' column")

# Normalize IDs as strings
valid_subjects = set(df["subject_id"].astype(str))

print(f"Found {len(valid_subjects)} valid subject IDs in CSV")

# Scan time_series folders
folders = [
    f for f in os.listdir(ts_path)
    if os.path.isdir(os.path.join(ts_path, f))
]

print(f"Found {len(folders)} folders in time_series")

to_delete = []

for folder in folders:
    if folder not in valid_subjects:
        to_delete.append(folder)

print("\nFolders to be removed:")
for f in to_delete:
    print("  ", f)

if DRY_RUN:
    print("\n🛑 DRY RUN — Nothing was deleted")
    print("Set DRY_RUN = False to apply changes")
else:
    print("\n🔥 Deleting folders...")
    for f in to_delete:
        full_path = os.path.join(ts_path, f)
        shutil.rmtree(full_path)
        print("Deleted:", f)

    print("\n✅ Cleanup complete")
