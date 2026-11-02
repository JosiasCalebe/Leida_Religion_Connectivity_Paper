"""
Arquivo original: Derivatives/DerivativesScript.py

Propósito: percorre derivatives/fmriprep/sub-*/func/*desc-confounds_regressors.tsv
(derivativos do OpenNeuro) e monta um CSV com uma coluna por sujeito contendo a série
temporal de dvars (trocar a coluna para std_dvars / framewise_displacement conforme o caso).
Obs.: o script testa a existência de "std_dvars" mas extrai "dvars"; ajuste se necessário.
"""

import os
import pandas as pd
from glob import glob

# Caminho base onde estão os diretórios dos sujeitos fMRIPrep
base_dir = r".\Derivatives\derivatives\fmriprep"

# Encontrar todos os arquivos TSV dos sujeitos dentro de fmriprep
tsv_files = glob(os.path.join(base_dir, "sub-*", "func", "*desc-confounds_regressors.tsv"))

data = {}

for file_path in tsv_files:
    # Extrair o ID do sujeito (ex: sub-0001)
    sub_id = os.path.basename(file_path).split("_")[0]

    # Ler o arquivo TSV
    df = pd.read_csv(file_path, sep='\t')

    # Verificar se a coluna existe
    if "std_dvars" in df.columns:
        data[sub_id] = df["dvars"].values
    else:
        print(f"Aviso: coluna não encontrada em {file_path}")

# Converter o dicionário em DataFrame
df_out = pd.DataFrame(data)

# Caminho de saída
output_path = os.path.join(base_dir, "dvars_all.csv")

# Salvar o CSV
df_out.to_csv(output_path, index=False)

print(f"Arquivo salvo em: {output_path}")
print(f"Total de sujeitos processados: {len(data)}")
