# Brain Connectivity Patterns in Religious and Non-Religious Individuals

Código, metadados e resultados da pesquisa **"Differences in Dynamic Functional Connectivity
Patterns Between Religious and Non-Religious Individuals"** (Costa, Gonçalves, Grafman &
Biazoli Jr., UFABC / INCT-SANI), aplicando LEiDA (Leading Eigenvector Dynamics Analysis)
aos dados de fMRI do dataset **ID1000 / AOMIC** (881 participantes).

## Resumo do pipeline

```
OpenNeuro ID1000 (ds003097)            01_OpenNeuro_Data
        │  renumeração sub-0001.., checagem anat/func
        ▼
CONN toolbox (pré-proc. + denoising)   02_CONN_Exports
        │  export ROI_SubjectNNN.mat -> tseries.csv (Gordon 333 / Glasser 360 ROIs)
        ▼
Seleção / pareamento de participantes  03_Participants_Selection
        │  metadata.csv (subject_id, condition) por análise
        ▼
Controle de qualidade de movimento     04_Motion_Artifacts
        │  RPs, DVARS, FD; exclusão de sujeitos com movimento excessivo
        ▼
PyLEiDA (fit_predict, K = 2..20)       05_LEiDA_Preprocessing
        │
        ▼
Resultados por atlas / amostra         06_LEiDA_Results
        │  occupancies, dwell times, transições, state_rois, relatórios HTML
        ▼
Figuras e análises do paper            07_Paper_Results
        (grids de estados, conectividade tradicional nilearn, ISC)
```

## Estrutura das pastas

| Pasta | Conteúdo |
|---|---|
| `01_OpenNeuro_Data/` | Como obter o ID1000, scripts de reorganização/renumeração dos sujeitos, `id_mapping.csv` (id novo -> id original) |
| `02_CONN_Exports/` | Script R que converte os exports do CONN em `tseries.csv`, rótulos e coordenadas das ROIs (Gordon e Glasser), atlas em MNI |
| `03_Participants_Selection/` | Notebooks de pareamento (case-control), planilhas dos participantes selecionados, `participants_*.csv` com a condição de cada sujeito |
| `04_Motion_Artifacts/` | Scripts e tabelas de movimento (parâmetros de realinhamento, DVARS, FD) e exclusão de sujeitos |
| `05_LEiDA_Preprocessing/` | Notebook-modelo do PyLEiDA, formato de entrada, arquivos por atlas |
| `06_LEiDA_Results/` | Resultados de cada análise: `files_per_atlas/<Gordon|Glasser>/<All_participants|Filtered>/<variável>/` |
| `07_Paper_Results/` | Manuscrito, figuras, conectividade tradicional (nilearn), ISC |

## Variáveis analisadas

| Nome na pasta | Grupos | N (All_participants) | N (Filtered / pareado) |
|---|---|---|---|
| `Religion` | religious x nonreligious | 881 (187 religiosos) | 374 (187 x 187); 334 após exclusão por movimento |
| `Gender` | female x male | 881 | 760 |
| `Education` | high x medium x low (paper: high x low) | 881 | 255 |
| `Religious_upbringing` | criação religiosa yes x no | 881 | 334 |
| `Non_religious_upbringing` | **só não religiosos**, criação religiosa yes x no | 694 | 282 (141 x 141) |

Cada análise foi rodada com os dois atlas (Gordon 333 ROIs e Glasser/HCP-MMP1 360 ROIs),
TR = 2,2 s, K-means com K = 2 a 20 e testes t por permutação (5 000 permutações).

## O que NÃO está no repositório

Os dados pesados não estão nesse repositório e podem ser regerados com os scripts daqui:

| Item | Tamanho | Como obter / regerar |
|---|---|---|
| NIfTI brutos do ID1000 | ~88 GB | [OpenNeuro ds003097](https://openneuro.org/datasets/ds003097) |
| Exports `.mat` do CONN | ~1 GB | CONN toolbox (ver `02_CONN_Exports/README.md`) |
| `time_series/sub-XXXX/tseries.csv` | ~1,5 GB por atlas | `02_CONN_Exports/scripts/mat_to_pyleida_timeseries.R` |
| `eigenvectors.csv`, `predictions.csv`, `models/*.pkl` | ~1,8 GB por análise | rodar `leida_run.ipynb` da análise |
| `transitions_probabilities.csv` para K ≠ 4 | ~20 MB por análise | idem (mantido só K = 4, usado na Figura 3) |
| HTMLs de `plot_states_nodes` (um por K) | ~3 GB | `06_LEiDA_Results/scripts/LeidaNodes_template_k05.ipynb` |

## Ambiente

```bash
pip install -r requirements.txt
```

Os notebooks usam `pyleida` (PyLEiDA), `nilearn`, `pandas`, `numpy`, `matplotlib`, `seaborn`,
`scipy`, `statsmodels`, `openpyxl`. Os scripts R usam `R.matlab`, `data.table`, `corrplot`,
`lme4`, `nlme`, `performance`, `ggplot2`.

> **Caminhos:** os scripts e notebooks usam caminhos **relativos à pasta local de dados do
> projeto** (a pasta que contém `ArquivosNew/`, `ID1000Files/`, `Atlas/`, `Religion/` etc.,
> que não está no repositório), por exemplo `./ArquivosNew/GordonReligious`. Execute-os a
> partir dessa pasta ou ajuste as variáveis de caminho no topo de cada script. Cada script
> tem um cabeçalho explicando propósito, entradas e saídas. Nos outputs dos notebooks e
> relatórios HTML, caminhos do ambiente Python aparecem abreviados como `~`.
