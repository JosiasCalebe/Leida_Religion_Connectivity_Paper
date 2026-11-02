"""
Arquivo original: CreateMetadata.py

Propósito: gera o metadata.csv (subject_id, condition) exigido pelo PyLEiDA a partir
da planilha de participantes selecionados (selected_participants*.xlsx), excluindo os
sujeitos listados em no_func_ids.csv. A coluna usada como condition é definida no
mapeamento (no exemplo, education_level -> high/medium/low; trocar para
religious_now, sex, religious_upbringing conforme a análise).
"""

import pandas as pd

# === INPUT FILES ===
google_csv_url = r".\selected_participantsEducation.xlsx"
no_func_csv = r".\ID1000Files\raw\no_func_ids.csv"

# === OUTPUT FILE ===
output_csv = r".\ID1000Files\raw\metadata.csv"

# --- Read the Google Sheet CSV ---
df = pd.read_excel(google_csv_url)

# --- Read the list of subjects to exclude ---
df_exclude = pd.read_csv(no_func_csv)

# assuming the file has a column named "id" OR "participant_id"
exclude_ids = set(df_exclude.iloc[:, 0].astype(str))

# --- Filter out excluded participants ---
df["participant_id"] = df["participant_id"].astype(str)
df_filtered = df[~df["participant_id"].isin(exclude_ids)]

# --- Map religious_now → condition ---
df_filtered["condition"] = df_filtered["education_level"].str.lower().map({
    "high": "high",
    "medium": "medium",
    "low": "low"
})

# --- Keep only the required columns ---
metadata = df_filtered[["participant_id", "condition"]].rename(
    columns={"participant_id": "subject_id"}
)

metadata = metadata.sort_values(by="subject_id")

# --- Save metadata.csv ---
metadata.to_csv(output_csv, index=False)

print("metadata.csv created successfully.")
