"""
Arquivo original: verifcaQuaisSemFunc.py

Propósito: mesma verificação de check_missing_func.py, mas sobre as pastas
planas anat_all2/ e func_all2/ geradas por organize_subject_folders.py.
Saída: impressão no console dos sub-XXXX presentes em anat e ausentes em func.
"""

import os
import re

# Paths to the folders
base_dir = r".\ID1000Files\raw\others"
anat_dir = os.path.join(base_dir, "anat_all2")
func_dir = os.path.join(base_dir, "func_all2")

# Function to extract subject ID like "sub-0009" from filename
def get_subject_id(filename):
    match = re.match(r"(sub-\d{4})", filename)
    return match.group(1) if match else None

# Get all subject IDs from anat_all
anat_subjects = {
    get_subject_id(f)
    for f in os.listdir(anat_dir)
    if os.path.isfile(os.path.join(anat_dir, f))
}
anat_subjects.discard(None)

# Get all subject IDs from func_all
func_subjects = {
    get_subject_id(f)
    for f in os.listdir(func_dir)
    if os.path.isfile(os.path.join(func_dir, f))
}
func_subjects.discard(None)

# Find subjects in anat but not in func
missing_in_func = anat_subjects - func_subjects

# Output
if missing_in_func:
    print("Subjects in anat_all but missing in func_all:")
    for subj in sorted(missing_in_func):
        print(subj)
else:
    print("✅ All subjects in anat_all have a matching entry in func_all!")