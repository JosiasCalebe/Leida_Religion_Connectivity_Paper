"""
Arquivo original: Derivatives/DerivativesMeanStdsScript.py

Propósito: a partir do CSV gerado por fmriprep_confounds_extract.py, calcula média e
desvio-padrão por sujeito e grava *_summary.csv.
"""

import os
import pandas as pd

# Caminho do CSV gerado anteriormente
input_path = r".\Derivatives\derivatives\fmriprep\dvars_all.csv"

# Ler o CSV com os valores de std_dvars
df = pd.read_csv(input_path)

# Calcular média e desvio padrão por coluna (sujeito)
summary_df = pd.DataFrame({
    'subject': df.columns,
    'mean_dvars': df.mean(),
    'std_dvars': df.std()
}).reset_index(drop=True)

# Caminho de saída
output_path = os.path.join(os.path.dirname(input_path), "dvars_all_summary.csv")

# Salvar o resultado
summary_df.to_csv(output_path, index=False)

print(f"Arquivo salvo em: {output_path}")
print(summary_df.head())
