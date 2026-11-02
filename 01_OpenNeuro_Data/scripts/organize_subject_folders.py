"""
Arquivo original: organizaPastas.py

Propósito: reorganiza as pastas sub-XXXX baixadas do OpenNeuro (ID1000, AOMIC).
  - Renumera os sujeitos sequencialmente (sub-0001, sub-0002, ...) e grava a
    correspondência new_id -> old_id em id_mapping.csv.
  - Copia os arquivos de func/ e anat/ para pastas planas (func_all2 / anat_all2)
    com o novo id como prefixo.
  - Sujeitos sem pasta func/ são movidos para no_func/.
Entradas : ID1000Files/raw/in_use/sub-*/  (estrutura BIDS do OpenNeuro)
Saídas   : anat_all2/, func_all2/, no_func/, id_mapping.csv
Obs.: caminhos absolutos da máquina original; ajuste base_dir antes de rodar.
"""

import os
import shutil
import csv

# Caminho para a pasta principal onde estão as sub-XXXX originais
base_dir = r".\ID1000Files\raw\in_use"

# Pastas de destino
anat_dest = os.path.join(base_dir, "anat_all2")
func_dest = os.path.join(base_dir, "func_all2")
no_func_dest = r".\ID1000Files\raw\no_func"
csv_path = os.path.join(base_dir, "id_mapping.csv")

# Cria as pastas de destino se não existirem
os.makedirs(anat_dest, exist_ok=True)
os.makedirs(func_dest, exist_ok=True)

# Lista todas as subpastas que começam com sub-
subfolders = [
    f for f in os.listdir(base_dir)
    if os.path.isdir(os.path.join(base_dir, f)) and f.startswith("sub-")
]
subfolders.sort()  # garante ordem fixa

with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["new_id", "old_id"])

# Loop com contador incremental
    for i, subfolder in enumerate(subfolders, start=1):
        subject_id = f"sub-{i:04d}"  # ex.: sub-0001, sub-0002
        old_id = subfolder

        writer.writerow([subject_id, old_id])

        sub_path = os.path.join(base_dir, subfolder)
        anat_path = os.path.join(sub_path, "anat")
        func_path = os.path.join(sub_path, "func")

        if not os.path.exists(func_path):
            print(f"⚠️ Pasta 'func' não encontrada para {subfolder}. Movendo para no_func...")
            dest_path = os.path.join(no_func_dest, subfolder)
            shutil.move(sub_path, dest_path)
            continue  # pula para o próximo sujeito

    # Copia arquivos da pasta func
        if os.path.exists(func_path):
            for file in os.listdir(func_path):
                src_file = os.path.join(func_path, file)
                if os.path.isfile(src_file):
                    new_name = f"{subject_id}_{file}"
                    shutil.copy2(src_file, os.path.join(func_dest, new_name))

    # Copia arquivos da pasta anat
        if os.path.exists(anat_path):
            for file in os.listdir(anat_path):
                src_file = os.path.join(anat_path, file)
                if os.path.isfile(src_file):
                    new_name = f"{subject_id}_{file}"
                    shutil.copy2(src_file, os.path.join(anat_dest, new_name))

print("✅ Arquivos reorganizados e renomeados com IDs sequenciais!")
