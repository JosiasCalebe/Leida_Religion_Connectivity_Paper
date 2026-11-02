"""
Arquivo original: checkFunc.py

Propósito: lista sujeitos (estrutura BIDS, pastas sub-XXXX) que possuem anat/
mas NÃO possuem func/ (sem fMRI funcional) para excluí-los da seleção.
Entrada : ID1000Files/raw/<dataset>/sub-*/{anat,func}
Saída   : impressão no console.
"""

import os

# Caminho base (agora é "raw")
base_dir = r".\ID1000Files\raw"

anat_only = []

# Percorre todas as pastas dentro de raw
for dataset in os.listdir(base_dir):
    dataset_dir = os.path.join(base_dir, dataset)
    if not os.path.isdir(dataset_dir):
        continue

    # Procura subpastas do tipo "sub-XXXX"
    subs = [d for d in os.listdir(dataset_dir) if d.startswith("sub-") and os.path.isdir(os.path.join(dataset_dir, d))]

    for subj in subs:
        subj_dir = os.path.join(dataset_dir, subj)
        anat_dir = os.path.join(subj_dir, "anat")
        func_dir = os.path.join(subj_dir, "func")

        # Verifica se existem arquivos dentro de anat e func
        has_anat = os.path.isdir(anat_dir) and any(os.path.isfile(os.path.join(anat_dir, f)) for f in os.listdir(anat_dir))
        has_func = os.path.isdir(func_dir) and any(os.path.isfile(os.path.join(func_dir, f)) for f in os.listdir(func_dir))

        if has_anat and not has_func:
            anat_only.append(f"{subj}")

# Saída
if anat_only:
    print("Subjects que possuem 'anat' mas não possuem 'func':")
    for subj in sorted(anat_only):
        print(subj)
else:
    print("✅ Todos os subjects com 'anat' também possuem 'func'.")
