# 04 - Controle de qualidade de movimento

Duas fontes de métricas:

1. **Parâmetros de realinhamento (RPs) do CONN** - `rp_sub-XXXX_task-moviewatching_bold.txt`,
   6 colunas por volume (x, y, z em mm; pitch, roll, yaw em rad).
2. **Confounds do fMRIPrep (OpenNeuro derivatives)** - `dvars`, `std_dvars`,
   `framewise_displacement` por volume.

## Scripts (`scripts/`)

| Script | O que faz |
|---|---|
| `rps_motion_analysis.py` | Para cada RP: médias brutas e absolutas, DP, máximos; flags `bad_subject` (máx > 0,3 mm ou > 3°) e `bad_subject_mean` (média abs acima dos limiares). Faz merge com a condição e salva `motion_*.csv` |
| `bad_subjects_by_condition.py` | Cruza `motion_summary.csv` com `metadata.csv`, lista os `bad_subject_mean` por condição, salva médias por condição e **remove** esses sujeitos do `metadata.csv` e de `time_series/` (gera as versões `motion_filtered`) |
| `fmriprep_confounds_extract.py` | Varre `derivatives/fmriprep/sub-*/func/*confounds_regressors.tsv` e monta um CSV (coluna por sujeito) com a série de DVARS/FD |
| `fmriprep_confounds_summary.py` | Média e DP por sujeito do CSV anterior (`*_summary.csv`) |
| `merge_motion_files.py` | Junta condição + dvars + std_dvars + FD + occupancies + dwell_times + motion num único CSV (`;`) por análise, para testar se movimento explica as diferenças entre grupos |

## Dados

| Pasta / arquivo | Conteúdo |
|---|---|
| `realignment_parameters/RPs_all_subjects/` | 881 RPs (id sequencial) |
| `realignment_parameters/RPs_matched_374/` | RPs da subamostra pareada; nome `rp_<id_novo>_<id_original>_...` e `motion_summary.csv` |
| `motion_data_csv/motion_summary_all_subjects.csv` | Saída de `rps_motion_analysis.py`, 881 sujeitos |
| `motion_data_csv/motion_summary_matched374*.csv` | Idem para a subamostra pareada, médias por condição e tabela mesclada |
| `motion_data_csv/Csvs_All_Subjects/` | Por sujeito: `religion/gender/education.csv`, `dvars.csv`, `std_dvars.csv`, `framewise_displacement.csv`, `motion.csv`, `occupancies.csv`, `dwell_times.csv` e subpastas `k4/`, `k10/` |
| `motion_data_csv/Csvs_<Variável>_Filtered/` | Mesmos arquivos para as subamostras pareadas |
| `motion_data_csv/merged/merged_<variável>_k{4,10}.csv` | Tabelas finais mescladas (entrada para regressões/correlações movimento x métricas LEiDA) |
| `fmriprep_confounds/all_subjects/` | `dvars_all.csv`, `std_dvars_all.csv`, `framewise_displacement_all.csv` (série por sujeito) e `*_summary.csv` |
| `fmriprep_confounds/matched_374/` | Idem para a subamostra pareada (`*_por_sujeito_selecionados.csv`, `*_summary.csv`) |

Os sujeitos excluídos por movimento reduziram a subamostra pareada de religião de 374 para 334
(`06_LEiDA_Results/.../Filtered/Religion/matched_374_motion_filtered_334`).
