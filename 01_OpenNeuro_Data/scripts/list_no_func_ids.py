"""
Arquivo original: noFuncIds.py

Propósito: gera no_func_ids.csv com os ids dos sujeitos movidos para no_func/
(sem dados funcionais). Esse CSV é usado por create_metadata_from_selection.py
para excluir esses participantes dos metadados.
"""

import os
import csv

base_dir = r".\ID1000Files\raw\no_func"
output_csv = r".\ID1000Files\raw\no_func_ids.csv"

# List only folders
folders = [name for name in os.listdir(base_dir)
           if os.path.isdir(os.path.join(base_dir, name))]

# Write CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id"])  # header
    for folder in folders:
        writer.writerow([folder])

print("CSV created at:", output_csv)
 