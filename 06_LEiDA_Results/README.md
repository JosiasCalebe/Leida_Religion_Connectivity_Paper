# 06 - Resultados do LEiDA

## Organização

```
files_per_atlas/
  Gordon/
    All_participants/
      Religion/                    881: religious x nonreligious
      Gender/                      881: female x male
      Education/                   881: high x medium x low (+ metadata_high_vs_low_only.csv)
      Religious_upbringing/        881: criação religiosa yes x no
      Non_religious_upbringing/    694 não religiosos: criação religiosa yes x no
    Filtered/
      Religion/
        matched_374/                     pareados 187 x 187
        matched_374_motion_filtered_334/ pareados sem sujeitos com movimento excessivo
        matched_374_denoising_variant/   pareados, export do CONN com outra configuração de denoising
      Gender/                      760 pareados
      Education/                   255 pareados (high x low)
      Religious_upbringing/        334 pareados
      Non_religious_upbringing/    282 pareados (141 x 141) - Figura 4 do paper
  Glasser/
    (mesma estrutura)
```

## Conteúdo de cada pasta de análise

| Arquivo | Descrição |
|---|---|
| `metadata.csv` | sujeitos e condição usados na análise |
| `rois_labels.txt`, `rois_coordinates.csv` | ROIs do atlas (quando presentes na origem) |
| `state_rois.csv` | ROIs com contribuição positiva em cada estado (K = 5 ou K escolhido no notebook) |
| `clustering/clustering_performance.csv/.png` | métricas de qualidade do K-means por K |
| `dynamics_metrics/k_{2..20}/occupancies.csv` | fractional occupancy por sujeito e estado |
| `dynamics_metrics/k_{2..20}/dwell_times.csv` | dwell time (s) por sujeito e estado |
| `dynamics_metrics/k_{2..20}/*_stats.csv` | `k, variable, group_1, group_2, statistic, p-value, effect_size, alpha_Bonferroni, reject_null` |
| `dynamics_metrics/k_4/transitions_probabilities.csv` | probabilidades de transição (só K = 4; os demais K ficaram fora por tamanho, regeráveis a partir de `predictions.csv`) |
| `dynamics_metrics/*.png` | pirâmides de occupancy/dwell time e scatter de p-valores por K |
| `leida_run.ipynb` | notebook que rodou `fit_predict` e as explorações (outputs removidos) |
| `report_*.html` | o mesmo notebook renderizado com todos os outputs (~20 MB) |
| `figures/` | figuras geradas na pasta (grids de estados K = 4 e K = 10 etc.) |
| `per_k_extracts/` (só subamostra pareada de religião) | `dwell_times{K}.csv`, `occupancies{K}.csv`, `state_rois_k{K}.csv` extraídos por K |
| `report_group_transitions_state_matrices.html` (idem) | `group_transitions` e `plot_states_matrices` para K = 2..20 |

Não incluídos (ver `MANIFEST.md`): `time_series/`, `eigenvectors.csv`, `predictions.csv`,
`models/*.pkl`.

## Scripts (`scripts/`)

| Notebook | Uso |
|---|---|
| `leida_plots_paper_figures.ipynb` | Carrega as análises Gordon (religião, sexo, escolaridade, criação religiosa) com `DataLoader` e gera as figuras do paper: `plot_states_grid` (centroides, connectome, boxplots de occupancy e dwell time coloridos por significância), `plot_same_state_across_Ks`, `plot_states_with_connectome`, `plot_selected_states_with_connectome`; depois lista `significant_states` e `state_rois` por K. Com outputs |
| `load_leida_plots_religious_gordon.ipynb` | Exploração da análise de religião (Gordon): pirâmides, `state_rois`, `load_centroids`, `plot_states_on_surf2` (usa `02_CONN_Exports/atlas/gordon333MNI.nii.gz`), `explore_state`, `plot_states_nodes` para K = 4 e 10. HTML com outputs em `.../Gordon/All_participants/Religion/report_load_leida_plots_religious_gordon.html` |
| `load_leida_plots_gender_gordon.ipynb`, `load_leida_plots_education_gordon.ipynb` | Idem para sexo e escolaridade |
| `group_transitions_and_state_matrices.ipynb` | `group_transitions(k)` e `plot_states_matrices(k)` para K = 2..20 |
| `LeidaNodes_template_k05.ipynb` | `plot_states_nodes` para cada estado de um K; existia uma cópia por K (2..20) em cada análise pareada |

Para reutilizar, aponte `DataLoader(<pasta da análise>, <pasta>/LEiDA_results)` para uma pasta
local que contenha os arquivos pesados.

## Principais achados

* **Religião**: religiosos têm maior occupancy do **Estado 1** (globalmente sincronizado) em
  K = 3..10 (Gordon, 881; K = 4: 0,526 x 0,484, p = 0,013, d = 0,21), sobrevivendo a Bonferroni
  em K = 3 e 4; replicado no Glasser e nas subamostras pareadas. Sem diferenças em transições.
* **Sexo**: homens com maior occupancy do Estado 2 (visual/atenção).
* **Escolaridade**: maior escolaridade com maior occupancy do estado sensório-motor.
* **Criação religiosa (só não religiosos, 141 x 141)**: maior dwell time num estado posterior
  (visual/motor) em quem foi criado em ambiente religioso; K = 14, p = 0,0008, d = 0,39.
