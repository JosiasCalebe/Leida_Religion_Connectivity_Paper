"""
Arquivo original: selectParticipantsFilter.py

Propósito: extrai de nao_religiosos.xlsx apenas participant_id e religious_upbringing,
gerando o metadata.csv para a análise "Non_religious_upbringing" (não religiosos divididos
por criação religiosa sim/não).
"""

import pandas as pd

INPUT_FILE = r".\nao_religiosos.xlsx"
OUTPUT_FILE = r".\metadata.csv"

def main():
    # Read the Excel file
    df = pd.read_excel(INPUT_FILE)

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Keep only the required columns
    result = df[["participant_id", "religious_upbringing"]]

    # Save to CSV
    result.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {len(result)} rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
