# 07 - Figuras e análises complementares

## `figures/`

| Pasta | Conteúdo |
|---|---|
| `state_grids_gordon/` | `religion_k4_all_states.png`, `religion_k10_*.png`, `gender_*`, `education_*` - grids gerados por `06_LEiDA_Results/scripts/leida_plots_paper_figures.ipynb` (Figuras 1 e 2) |
| `leida_plots_exports/` | HTML do notebook `leida_plots` em três versões (abr/2026, 27/04/2026, 12/06/2026) com todas as figuras renderizadas |

A Figura 3 (matrizes de transição K = 4) vem de
`06_LEiDA_Results/files_per_atlas/Gordon/All_participants/Religion/dynamics_metrics/k_4/transitions_probabilities.csv`.
A Figura 4 (dwell times, criação religiosa) vem de
`06_LEiDA_Results/files_per_atlas/Gordon/Filtered/Non_religious_upbringing/`.

## `traditional_connectivity_nilearn/`

Análise de conectividade funcional estática (seção 2.3): matriz de correlação de Pearson por
sujeito (`nilearn.connectome.ConnectivityMeasure`), teste t entre grupos em cada aresta,
correção FDR e `plot_connectome` das arestas com |t| acima do limiar.

| Arquivo | Conteúdo |
|---|---|
| `religion_connectivity_nilearn.ipynb` / `.html` | religiosos x não religiosos (Gordon, 881); sem diferenças após FDR |
| `religion_resultados_conectividade_FDR_final.csv` | t, p e p-FDR por aresta |
| `religion_mapa_conectividade_limpo.png`, `religion_mapa_limpo_final.png` | connectomes das diferenças |
| `gender_connectivity_nilearn.ipynb` / `.html`, `gender_mapa_conectividade_limpo.png` | idem para sexo |
| `education_connectivity_nilearn.ipynb`, `education_mapa_conectividade_limpo.png` | idem para escolaridade |

Os notebooks leem `time_series/`, `metadata.csv`, `rois_labels.txt` e `rois_coordinates.csv`
da pasta da análise (ver `05_`).

## `ISC_analysis/`

Correlação intersujeitos (ISC) por ROI, estática e em janela deslizante (30 volumes),
alinhada ao tempo do filme (TR = 2,2 s), religiosos x não religiosos (Gordon). Análise
exploratória com N reduzido (`ISC_Geral_N6`).

* `ISC_modelo_de_Analise.ipynb` (com outputs)
* `resultados_ISC_completo_Geral.csv` - ISC geral e por grupo, t, p e p-FDR por ROI
* `figures/` - top 20 ROIs, comparação entre grupos, glass brains

## `comparison_k5_gender_vs_religion/`

Estatísticas K = 5 (occupancies, dwell times, transições e `*_stats.csv`) das análises de sexo
e de religião lado a lado, com os respectivos `metadata_*.csv`.
