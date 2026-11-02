"""
Arquivo original: Religion/TestesIniciais/Arquivos/BadSubjectCondition.py

Propósito: cruza motion_summary.csv com metadata.csv, lista os sujeitos marcados como
bad_subject_mean por condição, grava as médias de movimento por condição
(motion_summary_merged.csv) e, em seguida, REMOVE esses sujeitos do metadata.csv e
apaga suas pastas em time_series/ (gera as versões "FilteredMovementArtifacts").
ATENÇÃO: modifica/apaga arquivos no diretório configurado em base_data_dir.
"""

import os
import shutil
import pandas as pd

def list_bad_subjects_by_condition(motion_csv, condition_csv):
    """
    Merge motion data with condition data and list bad subjects per condition.
    
    Parameters
    ----------
    motion_csv : str
        Path to the motion summary CSV (from our analysis script).
    condition_csv : str
        Path to the CSV containing subject_id and condition columns.
    
    Returns
    -------
    bad_by_condition : dict
        Dictionary mapping each condition to a list of bad subject IDs.
    """

    # Load both CSVs
    motion_df = pd.read_csv(motion_csv)
    condition_df = pd.read_csv(condition_csv)

    # Merge on subject ID
    merged = motion_df.merge(condition_df, left_on="subject", right_on="subject_id", how="inner")

    # Filter bad subjects
    bad_df = merged[merged["bad_subject_mean"] == True]

    # Group by condition
    bad_by_condition = bad_df.groupby("condition")["subject"].apply(list).to_dict()

    return bad_by_condition, merged


motion_csv = "./17-09/motion_summary.csv"      # from our motion analysis
condition_csv = "./Arquivos17-09/GordonFiltered/metadata.csv"     # must have subject_id, condition

motion_df = pd.read_csv(motion_csv)
condition_df = pd.read_csv(condition_csv)

    # Merge on subject ID
merged = motion_df.merge(condition_df, left_on="subject", right_on="subject_id", how="inner")

condition_means = merged.groupby("condition").mean(numeric_only=True)
condition_means.to_csv("./17-09/motion_summary_merged.csv", index=False)

bad_by_condition, merged_df = list_bad_subjects_by_condition(motion_csv, condition_csv)

for cond, subs in bad_by_condition.items():
        print(f"{cond}: {subs}")


# IMPORTANT: Change this path to the main directory where your 'sub-...' folders
# and 'metadata.csv' are located.
base_data_dir = "./Arquivos17-09/GordonFiltered"
metadata_file_path = base_data_dir + "/metadata.csv"
time_series_path = base_data_dir + "/time_series"
# --- You don't need to change anything below this line ---

# 2. --- PREPARE DATA ---
# Combine all subject IDs from the dictionary into a single flat list.
all_subs_list = [sub for sub_list in bad_by_condition.values() for sub in sub_list]
print(f"Found {len(all_subs_list)} total subjects to remove.")

# Construct the full path to the metadata file.


# 3. --- UPDATE METADATA.CSV ---
try:
    # Read the CSV file into a pandas DataFrame.
    print(f"\nReading metadata from: {metadata_file_path}")
    df = pd.read_csv(metadata_file_path)
    initial_rows = len(df)
    print(f"Initial rows in metadata.csv: {initial_rows}")

    # Keep only the rows where the 'subject_id' is NOT in our list of subjects to remove.
    # The '~' symbol acts as a "NOT" operator here.
    df_filtered = df[~df['subject_id'].isin(all_subs_list)]
    final_rows = len(df_filtered)

    # Save the filtered DataFrame back to the same CSV file, overwriting it.
    # index=False prevents pandas from writing a new index column.
    df_filtered.to_csv(metadata_file_path, index=False)
    
    print(f"✅ Successfully updated metadata.csv. Removed {initial_rows - final_rows} rows.")

except FileNotFoundError:
    print(f"⚠️ Warning: Could not find {metadata_file_path}. Skipping CSV update.")
except KeyError:
    print(f"⚠️ Warning: 'subject_id' column not found in {metadata_file_path}. Skipping CSV update.")


# 4. --- DELETE FOLDERS ---
print("\nNow processing folders for deletion...")
deleted_count = 0
skipped_count = 0

for sub_id in all_subs_list:
    # Create the full path to the subject's folder.
    folder_path = time_series_path+ "/" + sub_id
    
    # Check if the path exists and is a directory before trying to delete.
    if os.path.isdir(folder_path):
        try:
            # shutil.rmtree() deletes a directory and all its contents.
            shutil.rmtree(folder_path)
            print(f"🗑️ Deleted folder: {folder_path}")
            deleted_count += 1
        except OSError as e:
            print(f"❌ Error deleting {folder_path}: {e}")
    else:
        print(f"🔍 Folder not found, skipping: {folder_path}")
        skipped_count += 1

print(f"\nScript finished. Deleted {deleted_count} folders and skipped {skipped_count} that were not found.")


