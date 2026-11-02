"""
Arquivo original: renames.py

Propósito: os exports do CONN (ROI_SubjectNNN_SessionNNN.mat) foram gerados em
lotes (001-200, 201-400, 401-507). Este script soma 400 ao número do sujeito do
lote 401-507 e move os arquivos para a pasta full/ para unificar a numeração.
"""

import os
import re

# Define the directory containing the files (change if needed)
directory = r".\Others\ROIs\401-507"
newDirectory = r".\Others\ROIs\full"

# Regular expression pattern to match the filename format
pattern = re.compile(r'ROI_Subject(\d{3})_Session(\d{3})\.mat')

for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        # Extract subject number and session number
        subject_num = int(match.group(1))
        session_num = match.group(2)
        
        if 1 <= subject_num <= 200:
            new_subject_num = subject_num + 400

            # Format new subject number with leading zeros
            new_subject_str = f"{new_subject_num:03d}"
            
            # Create new filename
            new_filename = f"ROI_Subject{new_subject_str}_Session{session_num}.mat"
            
            # Rename the file
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(newDirectory, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")