"""
Arquivo original: Others/renameRPs.py

Propósito: remove o prefixo duplicado "sub-XXXX_" dos arquivos de parâmetros de
realinhamento (rp_sub-0001_sub-0001_task-...txt -> rp_sub-0001_task-...txt).
"""

import os
import re

# Set your folder path here
folder_path = r".\Others\RPs"

# Regex to match the first sub-XXXX after the prefix
pattern = re.compile(r"(rp_)sub-\d+_(.*)")

for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        new_name = match.group(1) + match.group(2)  # keep rp_ + rest
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        print(f"Renaming: {filename} -> {new_name}")
        os.rename(old_path, new_path)

print("Done.")
