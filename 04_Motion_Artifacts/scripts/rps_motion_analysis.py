"""
Arquivo original: AnaliseArtefatosMovimento/RPsAnalysis.py

Propósito: lê os parâmetros de realinhamento do CONN (rp_sub-XXXX_task-moviewatching_bold.txt,
6 colunas: 3 translações em mm e 3 rotações em rad) e calcula, por sujeito, médias brutas
e absolutas, desvios-padrão, máximos e flags de qualidade
(bad_subject: máx > 0.3 mm ou > 3 graus; bad_subject_mean: média abs > limiares).
Faz merge com o CSV de condição e grava motion_religion.csv na pasta dos RPs.
"""

import os
import numpy as np
import pandas as pd

def analyze_motion_folder(folder_path, condition_csv, output_csv="motion_religion.csv"):
    results = []

    # Thresholds
    translation_thresh = 0.3  # mm
    rotation_thresh = 3.0     # degrees

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            data = np.loadtxt(file_path)
            
            # Extract subject ID
            sub_id = file_name.split("_")[1]
            
            # Calculate BOTH raw means and absolute means
            raw_means = np.mean(data, axis=0)
            abs_means = np.mean(np.abs(data), axis=0)
            stds = np.std(data, axis=0)
            
            # Max values (using absolute since we care about magnitude)
            max_translation = np.max(np.abs(data[:, :3]))
            max_rotation = np.max(np.abs(data[:, 3:])) * (180 / np.pi)
            
            # Check thresholds - use ABSOLUTE values for threshold checking
            bad_subject = (max_translation > translation_thresh) or (max_rotation > rotation_thresh)
            
            # For mean threshold checking, use absolute means
            mean_rot_deg = abs_means[3:] * (180 / np.pi)  # Use abs_means instead of raw_means
            bad_translation = np.any(abs_means[:3] > translation_thresh)  # Use abs_means
            bad_rotation = np.any(mean_rot_deg > rotation_thresh)
            bad_subject_mean = bad_translation or bad_rotation

            # Store results - include BOTH raw and absolute means
            results.append({
                "subject": sub_id,
                # Raw means (can be negative)
                "raw_mean_x_trans": raw_means[0],
                "raw_mean_y_trans": raw_means[1],
                "raw_mean_z_trans": raw_means[2],
                "raw_mean_x_rot": raw_means[3],
                "raw_mean_y_rot": raw_means[4],
                "raw_mean_z_rot": raw_means[5],
                # Absolute means (always positive)
                "abs_mean_x_trans": abs_means[0],
                "abs_mean_y_trans": abs_means[1],
                "abs_mean_z_trans": abs_means[2],
                "abs_mean_x_rot": abs_means[3],
                "abs_mean_y_rot": abs_means[4],
                "abs_mean_z_rot": abs_means[5],
                # Standard deviations
                "std_x_trans": stds[0],
                "std_y_trans": stds[1],
                "std_z_trans": stds[2],
                "std_x_rot": stds[3],
                "std_y_rot": stds[4],
                "std_z_rot": stds[5],
                # Maximum values
                "max_translation_mm": max_translation,
                "max_rotation_deg": max_rotation,
                # Quality flags
                "bad_subject": bad_subject,
                "bad_subject_mean": bad_subject_mean,
            })

    # Convert to dataframe
    summary_df = pd.DataFrame(results)

    condition_df = pd.read_csv(condition_csv)
    merged = summary_df.merge(condition_df, left_on="subject", right_on="subject_id", how="inner")

    # Save to CSV
    output_path = os.path.join(folder_path, output_csv)
    merged.to_csv(output_path, index=False)

    print(f"✅ Summary saved to: {output_path}")
    return merged


# Example usage:
folder = r".\AnaliseArtefatosMovimento\RPs"  
condition_csv = r".\AnaliseArtefatosMovimento\Csvs Religion Filtered\religion.csv"
df = analyze_motion_folder(folder, condition_csv)
print(df.head())
