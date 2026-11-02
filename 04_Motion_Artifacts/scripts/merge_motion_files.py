"""
Arquivo original: AnaliseArtefatosMovimento/MergeFiles.py

Propósito: junta em um único CSV (separador ;) os arquivos por sujeito de
condição (religion/gender/education), dvars, std_dvars, framewise_displacement,
occupancies, dwell_times e motion, prefixando as colunas pela origem.
Gera os merged_*.csv usados para checar se movimento explica as diferenças entre grupos.
"""

import pandas as pd
import glob
import os

# --- CONFIG ---
folder_path = r".\AnaliseArtefatosMovimento\Csvs Gender Filtered"
possible_keys = ["subject_id", "subject"]
standard_key = "subject_id"
output_file = r".\AnaliseArtefatosMovimento\merged_gender_k10.csv"

def read_flexible_csv(file):
    return pd.read_csv(file, sep=None, engine="python")

def standardize_key_column(df):
    for col in possible_keys:
        if col in df.columns:
            df = df.rename(columns={col: standard_key})
            df[standard_key] = df[standard_key].astype(str).str.strip().str.lstrip("0")
            return df
    raise ValueError("No valid key column found")

def add_prefix(df, file):
    """Add prefix to all columns except the key."""
    filename = os.path.basename(file).lower()

    if "occupancies" in filename:
        prefix = "occ_"
    elif "dwell" in filename:
        prefix = "dwell_"
    else:
        prefix = os.path.splitext(filename)[0] + "_"

    new_cols = {
        col: prefix + col for col in df.columns if col != standard_key
    }
    return df.rename(columns=new_cols)

# --- LOAD FILES ---

csv_files = [
    #os.path.join(folder_path, "religion.csv"),
    os.path.join(folder_path, "gender.csv"),
    #os.path.join(folder_path, "education.csv"),
    os.path.join(folder_path, "dvars.csv"),
    os.path.join(folder_path, "std_dvars.csv"),
    os.path.join(folder_path, "framewise_displacement.csv"),
    os.path.join(folder_path, "occupancies.csv"),
    os.path.join(folder_path, "dwell_times.csv"),
    os.path.join(folder_path, "motion.csv")
]

# --- FIRST FILE ---
merged_df = read_flexible_csv(csv_files[0])
merged_df = standardize_key_column(merged_df)
merged_df = add_prefix(merged_df, csv_files[0])

# --- MERGE LOOP ---
for file in csv_files[1:]:
    df = read_flexible_csv(file)
    
    try:
        df = standardize_key_column(df)
    except ValueError:
        print(f"Skipping {file} (no key column)")
        continue

    df = add_prefix(df, file)

    merged_df = pd.merge(
        merged_df,
        df,
        on=standard_key,
        how="inner"
    )
    
merged_df = merged_df.T.drop_duplicates().T
# --- SAVE ---
merged_df.to_csv(output_file, sep=";", index=False)

print(f"Merged file saved as: {output_file}")